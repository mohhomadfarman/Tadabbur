"""Server-side feature gating. Import these anywhere a view needs to honor a flag —
never rely on the frontend hiding a feature as the only gate.

    from apps.features.service import feature_enabled
    if not feature_enabled('badges', request.user):
        return Response(..., status=403)
"""
from .models import FeatureFlag
from .registry import FEATURE_REGISTRY, get_spec


def feature_enabled(key, user):
    """True if `key` is enabled for `user` (or anonymous). Falls back to the
    registry's default_enabled when no FeatureFlag row exists yet — so a freshly
    added key behaves per its declared default even before seed_feature_flags runs."""
    flag = FeatureFlag.objects(key=key).first()
    if not flag:
        spec = get_spec(key)
        return bool(spec and spec.get('default_enabled', False))
    return flag.is_enabled_for(user)


def effective_flags(user):
    """The resolved {key: bool} map for `user` across every registry key. This is
    what the learner-facing endpoint returns — it never exposes allowed_user_ids."""
    rows = {f.key: f for f in FeatureFlag.objects()}
    result = {}
    for spec in FEATURE_REGISTRY:
        key = spec['key']
        flag = rows.get(key)
        if flag is not None:
            result[key] = flag.is_enabled_for(user)
        else:
            result[key] = bool(spec.get('default_enabled', False))
    return result
