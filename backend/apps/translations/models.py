from datetime import datetime, timezone

from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentListField,
    StringField, BooleanField, DateTimeField,
)

# Default system prompt that guides Gemini when translating Islamic content. Admins
# can override it from the admin panel (Admin → Languages → Gemini settings).
DEFAULT_GLOSSARY = (
    "You are an expert translator of Islamic educational content (Seerah, Qurʾan, "
    "Hadith, Fiqh). Translate naturally and accurately into the requested target "
    "language so a learner reads it fluently.\n"
    "Rules:\n"
    "- Preserve Arabic script exactly (e.g. Qurʾanic verses) — do not transliterate "
    "or translate Arabic-script text.\n"
    "- Keep the honorific ﷺ and characters like ʿ / ʾ exactly where they appear.\n"
    "- Keep proper nouns — names of people, places, books — and core Islamic terms "
    "(e.g. Seerah, Daʿwah, Maghāzī, Sahābah, Tawheed, Ummah) recognizable; "
    "transliterate them rather than translating them away.\n"
    "- Keep the meaning faithful; do not add, omit, or editorialize.\n"
    "- Preserve tone and formatting."
)


class Language(EmbeddedDocument):
    """An offered translation language, managed by admins."""
    code = StringField(required=True)        # storage key + slug, e.g. 'hinglish'
    name = StringField(required=True)        # used in the Gemini prompt, e.g. 'Hinglish'
    native_name = StringField(default='')    # shown to learners, e.g. 'हिंग्लिश'
    rtl = BooleanField(default=False)
    enabled = BooleanField(default=True)


class TranslationSettings(Document):
    """Singleton holding the offered languages and Gemini configuration."""
    key = StringField(default='translation', unique=True)
    # Stored server-side only; never returned in full by the API (see views).
    gemini_api_key = StringField(default='')
    model = StringField(default='gemini-flash-lite-latest')
    languages = EmbeddedDocumentListField(Language)
    system_instruction = StringField(default=DEFAULT_GLOSSARY)
    updated_at = DateTimeField()

    meta = {'collection': 'translation_settings'}

    @classmethod
    def get_solo(cls):
        obj = cls.objects(key='translation').first()
        if not obj:
            obj = cls(key='translation', system_instruction=DEFAULT_GLOSSARY)
            obj.save()
        return obj

    def enabled_languages(self):
        return [lang for lang in (self.languages or []) if lang.enabled]

    def find_language(self, code):
        return next((lang for lang in (self.languages or []) if lang.code == code), None)
