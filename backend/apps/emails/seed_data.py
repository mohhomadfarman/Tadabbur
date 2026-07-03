"""Default content_blocks for the 3 system EmailTemplate rows, matching the
copy in apps.emails.transactional's hardcoded fallback generators. Used only by
the seed_email_templates management command."""

SYSTEM_TEMPLATE_SEEDS = [
    {
        'slug': 'verification',
        'name': 'Verify email (system)',
        'subject': 'Verify your Tadabbur email',
        'content_blocks': [
            {'type': 'text', 'order': 0, 'body': {'text': 'Assalamu alaikum,'}},
            {'type': 'text', 'order': 1, 'body': {
                'text': 'Please confirm your email address to finish setting up your Tadabbur account.'}},
            {'type': 'button', 'order': 2, 'body': {'url': '{{verify_url}}', 'label': 'Verify email'}},
            {'type': 'text', 'order': 3, 'body': {
                'text': "This link expires in 24 hours. If you didn't create this account, you can ignore this email."}},
        ],
    },
    {
        'slug': 'password_reset',
        'name': 'Reset password (system)',
        'subject': 'Reset your Tadabbur password',
        'content_blocks': [
            {'type': 'text', 'order': 0, 'body': {'text': 'Assalamu alaikum,'}},
            {'type': 'text', 'order': 1, 'body': {'text': 'We received a request to reset your Tadabbur password.'}},
            {'type': 'button', 'order': 2, 'body': {'url': '{{reset_url}}', 'label': 'Reset password'}},
            {'type': 'text', 'order': 3, 'body': {
                'text': "This link expires in 30 minutes. If you didn't request this, you can safely ignore this email."}},
        ],
    },
    {
        'slug': 'badge_earned',
        'name': 'Badge earned (system)',
        'subject': 'You earned a badge: {{badge_name}}',
        'content_blocks': [
            {'type': 'text', 'order': 0, 'body': {'text': 'Assalamu alaikum,'}},
            {'type': 'text', 'order': 1, 'body': {'text': 'You just earned the {{badge_name}} badge on Tadabbur!'}},
            {'type': 'text', 'order': 2, 'body': {'text': '{{badge_reward}}'}},
            {'type': 'text', 'order': 3, 'body': {'text': 'Log in to see it on your dashboard.'}},
        ],
    },
]
