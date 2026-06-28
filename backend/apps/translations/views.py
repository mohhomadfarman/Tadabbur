import re
from datetime import datetime, timezone

from django.conf import settings as django_settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from .models import TranslationSettings, Language


def _slug(text):
    return re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')


def _mask(key):
    """Never reveal the stored key — only a harmless hint that one is set."""
    key = (key or '').strip()
    if not key:
        return ''
    return '••••' + key[-4:] if len(key) >= 4 else '••••'


def _public_language(lang):
    return {
        'code': lang.code,
        'name': lang.name,
        'native_name': lang.native_name or '',
        'rtl': bool(lang.rtl),
    }


def _admin_language(lang):
    return {**_public_language(lang), 'enabled': bool(lang.enabled)}


def _settings_payload(s):
    has_db_key = bool((s.gemini_api_key or '').strip())
    has_env_key = bool(getattr(django_settings, 'GEMINI_API_KEY', ''))
    return {
        'model': s.model,
        'system_instruction': s.system_instruction or '',
        'languages': [_admin_language(l) for l in (s.languages or [])],
        # Key is NEVER returned in full — only whether one exists + a masked hint.
        'has_key': has_db_key or has_env_key,
        'key_hint': _mask(s.gemini_api_key),
        'key_source': 'admin' if has_db_key else ('env' if has_env_key else 'none'),
        'updated_at': s.updated_at.isoformat() if s.updated_at else None,
    }


def _parse_languages(raw_list):
    """Validate + dedupe an incoming languages list. Returns (languages, error)."""
    languages, seen = [], set()
    for i, item in enumerate(raw_list):
        if not isinstance(item, dict):
            return None, f'Language at index {i} is not an object.'
        name = (item.get('name') or '').strip()
        if not name:
            return None, f'Language at index {i} is missing a name.'
        code = _slug(item.get('code') or '') or _slug(name)
        if not code:
            return None, f'Language "{name}" produces an empty code.'
        if code in seen:
            continue  # keep first occurrence
        seen.add(code)
        languages.append(Language(
            code=code,
            name=name,
            native_name=(item.get('native_name') or '').strip(),
            rtl=bool(item.get('rtl', False)),
            enabled=bool(item.get('enabled', True)),
        ))
    return languages, None


class PublicLanguagesView(APIView):
    """Public: the enabled languages a learner can choose from (no key, no config)."""
    permission_classes = [AllowAny]

    def get(self, request):
        s = TranslationSettings.get_solo()
        return Response([_public_language(l) for l in s.enabled_languages()])


class TranslationSettingsView(APIView):
    """Admin: manage offered languages + Gemini config. Requires 'translations'."""
    permission_classes = [section_required('translations')]

    def get(self, request):
        return Response(_settings_payload(TranslationSettings.get_solo()))

    def patch(self, request):
        s = TranslationSettings.get_solo()
        data = request.data

        if isinstance(data.get('model'), str) and data['model'].strip():
            s.model = data['model'].strip()

        if isinstance(data.get('system_instruction'), str):
            s.system_instruction = data['system_instruction'].strip()

        if 'languages' in data:
            if not isinstance(data['languages'], list):
                return Response({'languages': 'Must be a list.'}, status=status.HTTP_400_BAD_REQUEST)
            languages, error = _parse_languages(data['languages'])
            if error:
                return Response({'languages': error}, status=status.HTTP_400_BAD_REQUEST)
            s.languages = languages

        # Key handling: an explicit clear wins; otherwise update only when a
        # non-empty value is supplied (a blank value leaves the stored key intact).
        if data.get('clear_key') is True:
            s.gemini_api_key = ''
        elif isinstance(data.get('gemini_api_key'), str) and data['gemini_api_key'].strip():
            s.gemini_api_key = data['gemini_api_key'].strip()

        s.updated_at = datetime.now(timezone.utc)
        s.save()
        return Response(_settings_payload(s))
