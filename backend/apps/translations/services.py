"""Gemini-backed lesson translation.

The flow is deliberately structure-preserving: we extract only the translatable
*string values* from a lesson into a flat ``{key: text}`` map, ask Gemini to return
the same keys with translated values, then merge those back onto a copy of the
original blocks. Non-translatable fields (Arabic, ayah numbers, the quiz correct
index, media URLs, block type/order) are never sent and never altered.
"""

import copy
import json
import time

from django.conf import settings as django_settings

from .models import TranslationSettings


class GeminiNotConfigured(Exception):
    """No API key configured (DB or env)."""


class GeminiError(Exception):
    """Gemini call failed or returned something unusable."""


# Per block type: which keys inside `body` hold translatable text. Quiz `options`
# (a list) are handled separately. Anything not listed here is preserved as-is.
TRANSLATABLE_BLOCK_FIELDS = {
    'text':   ['text'],
    'verse':  ['translation'],
    'hadith': ['text', 'source', 'narrator'],
    'image':  ['caption'],
    'video':  ['caption'],
    'quiz':   ['question', 'explanation'],
}

# Lesson-level translatable fields.
TRANSLATABLE_LESSON_FIELDS = ['title', 'summary', 'meta_title', 'meta_description']


def _sorted_blocks(lesson):
    return sorted(lesson.content_blocks, key=lambda b: b.order)


def extract_segments(lesson):
    """Flat map of every translatable string in the lesson, keyed by a stable path."""
    segments = {}
    for field in TRANSLATABLE_LESSON_FIELDS:
        val = getattr(lesson, field, '') or ''
        if isinstance(val, str) and val.strip():
            segments[field] = val

    for i, block in enumerate(_sorted_blocks(lesson)):
        body = block.body or {}
        for field in TRANSLATABLE_BLOCK_FIELDS.get(block.type, []):
            val = body.get(field)
            if isinstance(val, str) and val.strip():
                segments[f'b{i}.{field}'] = val
        if block.type == 'quiz':
            for oi, opt in enumerate(body.get('options') or []):
                if isinstance(opt, str) and opt.strip():
                    segments[f'b{i}.option{oi}'] = opt
    return segments


def merge_segments(lesson, translated):
    """Rebuild a translated lesson payload from the translated segment map.

    Falls back to the original value for any segment Gemini omitted, so a partial
    response degrades gracefully rather than dropping content.
    """
    def pick(key, original):
        val = translated.get(key)
        return val if isinstance(val, str) and val.strip() else original

    result = {field: pick(field, getattr(lesson, field, '') or '') for field in TRANSLATABLE_LESSON_FIELDS}

    blocks = []
    for i, block in enumerate(_sorted_blocks(lesson)):
        body = copy.deepcopy(block.body or {})
        for field in TRANSLATABLE_BLOCK_FIELDS.get(block.type, []):
            if field in body and isinstance(body[field], str) and body[field].strip():
                body[field] = pick(f'b{i}.{field}', body[field])
        if block.type == 'quiz' and isinstance(body.get('options'), list):
            body['options'] = [
                pick(f'b{i}.option{oi}', opt) if isinstance(opt, str) else opt
                for oi, opt in enumerate(body['options'])
            ]
        blocks.append({'type': block.type, 'order': block.order, 'body': body})

    result['content_blocks'] = blocks
    return result


def _resolve_api_key(settings_doc):
    key = (settings_doc.gemini_api_key or '').strip()
    return key or getattr(django_settings, 'GEMINI_API_KEY', '')


REQUEST_TIMEOUT_MS = 60_000  # cap each Gemini call so a stalled connection fails fast


def _get_client(api_key):
    # Imported lazily so the app still loads if the package isn't installed yet.
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:  # pragma: no cover - environment/dependency issue
        raise GeminiError('google-genai package is not installed.') from exc
    return genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=REQUEST_TIMEOUT_MS))


def _build_config(system_instruction):
    from google.genai import types
    kwargs = dict(
        system_instruction=system_instruction,
        response_mime_type='application/json',
        temperature=0.3,
    )
    # Minimal thinking (matches the desired fast/cheap profile). Wrapped because
    # the field name has shifted across SDK versions / models.
    try:
        kwargs['thinking_config'] = types.ThinkingConfig(thinking_budget=0)
    except Exception:  # pragma: no cover
        pass
    return types.GenerateContentConfig(**kwargs)


def _parse_json_object(raw):
    text = (raw or '').strip()
    start, end = text.find('{'), text.rfind('}')
    if start == -1 or end == -1 or end < start:
        raise GeminiError('Gemini did not return a JSON object.')
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        raise GeminiError('Could not parse Gemini JSON response.') from exc


def translate_lesson(lesson, language, settings_doc=None):
    """Generate (but do not persist) a translation candidate for ``lesson``.

    ``language`` is a Language embedded doc (uses ``.name`` in the prompt).
    Returns a dict: {title, summary, meta_title, meta_description, content_blocks}.
    """
    settings_doc = settings_doc or TranslationSettings.get_solo()
    api_key = _resolve_api_key(settings_doc)
    if not api_key:
        raise GeminiNotConfigured('Gemini API key is not configured.')

    segments = extract_segments(lesson)
    if not segments:
        # Nothing to translate — return the original shape unchanged.
        return merge_segments(lesson, {})

    system_instruction = (settings_doc.system_instruction or '').strip() or None
    model = (settings_doc.model or '').strip() or 'gemini-flash-lite-latest'

    user_text = (
        f'Translate the string VALUES in this JSON object into {language.name}. '
        f'Return ONLY a valid JSON object with the EXACT same keys, where each value '
        f'is the translation of the corresponding source value. Do not add, remove, '
        f'merge, or reorder keys.\n\n'
        f'{json.dumps(segments, ensure_ascii=False)}'
    )

    client = _get_client(api_key)
    config = _build_config(system_instruction)

    # The connection to the Gemini endpoint can be flaky from some networks —
    # SSL EOF / RemoteProtocolError / "Server disconnected" mid-request. Each
    # call is bounded by REQUEST_TIMEOUT_MS; retry a few times before failing.
    last_exc = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model, contents=user_text, config=config,
            )
            last_exc = None
            break
        except Exception as exc:
            last_exc = exc
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
    if last_exc is not None:
        raise GeminiError(f'Gemini request failed: {last_exc}') from last_exc

    translated = _parse_json_object(getattr(response, 'text', '') or '')
    if not isinstance(translated, dict):
        raise GeminiError('Gemini response was not a JSON object.')

    return merge_segments(lesson, translated)
