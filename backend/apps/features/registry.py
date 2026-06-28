"""The registry of known feature-flag keys — the source of truth for *which*
features exist and their defaults. The DB (FeatureFlag documents) holds the
mutable admin-set state; this list defines the contract.

To add a new gateable feature: append one spec here, then run
`python manage.py seed_feature_flags` so a FeatureFlag row is materialized.

`default_enabled` policy (agreed with the project owner):
  - Retrofits of already-live features start enabled=True (so nothing breaks).
  - Net-new features start enabled=False (beta-first) — turn them on, or scope
    them to selected users, from Admin → Feature Flags when ready.

`owner_section` ties the feature to the admin section that manages it (one of
apps.common.permissions.SECTIONS), purely for grouping/display in the admin UI.
"""

FEATURE_REGISTRY = [
    {
        'key': 'ai_translation',
        'label': 'AI Lesson Translation',
        'description': 'Gemini-powered per-track lesson translation for learners.',
        'default_enabled': True,   # retrofit: already live
        'owner_section': 'translations',
    },
    {
        'key': 'announcement_modals',
        'label': 'Announcement Modals',
        'description': 'Admin-authored pop-up modals shown to logged-in users.',
        'default_enabled': True,   # retrofit: already live
        'owner_section': 'announcements',
    },
    {
        'key': 'track_feedback',
        'label': 'Track Completion Feedback',
        'description': 'Prompt learners to rate a track after they complete it.',
        'default_enabled': False,  # net-new: beta-first
        'owner_section': 'feedback',
    },
    {
        'key': 'badges',
        'label': 'Badges & Rewards',
        'description': 'Award badges on milestones with a celebration popup.',
        'default_enabled': False,  # net-new: beta-first
        'owner_section': 'badges',
    },
    {
        'key': 'email_marketing',
        'label': 'Email Marketing',
        'description': 'Email templates + campaigns sent to recipient segments.',
        'default_enabled': False,  # net-new: beta-first
        'owner_section': 'email',
    },
]

_BY_KEY = {spec['key']: spec for spec in FEATURE_REGISTRY}


def register_feature(key, label, description='', default_enabled=False, owner_section=''):
    """Programmatic registration (e.g. from an app's apps.py ready()). Idempotent —
    a later call with the same key updates the existing spec."""
    spec = {
        'key': key,
        'label': label,
        'description': description,
        'default_enabled': bool(default_enabled),
        'owner_section': owner_section,
    }
    if key in _BY_KEY:
        _BY_KEY[key].update(spec)
    else:
        FEATURE_REGISTRY.append(spec)
        _BY_KEY[key] = spec
    return spec


def known_keys():
    return [spec['key'] for spec in FEATURE_REGISTRY]


def get_spec(key):
    return _BY_KEY.get(key)
