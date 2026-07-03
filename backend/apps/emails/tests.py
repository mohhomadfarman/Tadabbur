import pytest

from .block_render import normalize_email_blocks, render_blocks_to_html
from .personalize import render_merge_tags
from .system_templates import send_system_email


class TestNormalizeEmailBlocks:

    def test_valid_blocks_pass_through(self):
        blocks, error = normalize_email_blocks([
            {'type': 'text', 'body': {'text': 'hi'}},
            {'type': 'button', 'body': {'url': 'https://x', 'label': 'Go'}},
        ])
        assert error is None
        assert [b['type'] for b in blocks] == ['text', 'button']
        assert [b['order'] for b in blocks] == [0, 1]

    def test_invalid_type_rejected(self):
        blocks, error = normalize_email_blocks([{'type': 'quiz', 'body': {}}])
        assert blocks is None
        assert 'quiz' in error

    def test_empty_list_ok(self):
        blocks, error = normalize_email_blocks([])
        assert blocks == []
        assert error is None


class TestRenderBlocksToHtml:

    def test_empty_blocks_render_empty_string(self):
        assert render_blocks_to_html([]) == ''

    def test_text_block_has_inline_style_and_no_flex_grid(self):
        html = render_blocks_to_html([{'type': 'text', 'order': 0, 'body': {'text': 'hello'}}])
        assert 'style=' in html
        assert 'hello' in html
        assert 'flex' not in html and 'grid' not in html

    def test_text_block_escapes_content(self):
        html = render_blocks_to_html([{'type': 'text', 'order': 0, 'body': {'text': '<script>x</script>'}}])
        assert '<script>' not in html
        assert '&lt;script&gt;' in html

    def test_button_block_renders_link(self):
        html = render_blocks_to_html([{'type': 'button', 'order': 0, 'body': {'url': 'https://x.com', 'label': 'Go'}}])
        assert 'href="https://x.com"' in html
        assert 'Go' in html

    def test_button_block_without_url_or_label_renders_nothing(self):
        html = render_blocks_to_html([{'type': 'button', 'order': 0, 'body': {'label': 'Go'}}])
        assert 'href=' not in html

    def test_divider_and_spacer_render(self):
        html = render_blocks_to_html([
            {'type': 'divider', 'order': 0, 'body': {}},
            {'type': 'spacer', 'order': 1, 'body': {'height': 40}},
        ])
        assert '<hr' in html
        assert 'height:40px' in html

    def test_blocks_render_in_order(self):
        html = render_blocks_to_html([
            {'type': 'text', 'order': 1, 'body': {'text': 'second'}},
            {'type': 'text', 'order': 0, 'body': {'text': 'first'}},
        ])
        assert html.index('first') < html.index('second')


class TestRenderMergeTags:

    def test_substitutes_known_tag(self):
        assert render_merge_tags('Hi {{full_name}}', {'full_name': 'Aisha'}) == 'Hi Aisha'

    def test_leaves_unknown_tag_literal(self):
        assert render_merge_tags('Hi {{nickname}}', {'full_name': 'Aisha'}) == 'Hi {{nickname}}'

    def test_escapes_html_in_value(self):
        result = render_merge_tags('Hi {{full_name}}', {'full_name': '<b>Aisha</b>'})
        assert '<b>' not in result
        assert '&lt;b&gt;' in result

    def test_none_value_becomes_empty_string(self):
        assert render_merge_tags('R: {{badge_reward}}', {'badge_reward': None}) == 'R: '

    def test_no_context_leaves_all_tags(self):
        assert render_merge_tags('Hi {{full_name}}', {}) == 'Hi {{full_name}}'


@pytest.mark.django_db
class TestSendSystemEmail:

    @pytest.fixture(autouse=True)
    def capture_sends(self, monkeypatch):
        calls = []
        monkeypatch.setattr('apps.emails.system_templates.send_transactional_email.delay',
                             lambda *a, **k: calls.append(a))
        self.calls = calls
        return calls

    def _cleanup(self):
        from .models import EmailTemplate
        EmailTemplate.objects(slug='test_slug').delete()

    def test_falls_back_when_no_template(self):
        self._cleanup()
        send_system_email('test_slug', 'user@example.com', {}, 'Fallback subject', '<p>fallback</p>')
        assert len(self.calls) == 1
        assert self.calls[0] == ('Fallback subject', '<p>fallback</p>', 'user@example.com')

    def test_falls_back_when_template_inactive(self):
        from .models import EmailTemplate
        self._cleanup()
        EmailTemplate(name='t', slug='test_slug', subject='S', html_body='<p>tpl</p>', is_active=False).save()
        try:
            send_system_email('test_slug', 'user@example.com', {}, 'Fallback subject', '<p>fallback</p>')
            assert self.calls[0][1] == '<p>fallback</p>'
        finally:
            self._cleanup()

    def test_uses_template_when_active(self):
        from .models import EmailTemplate
        self._cleanup()
        EmailTemplate(name='t', slug='test_slug', subject='Hi {{full_name}}', html_body='<p>Hi {{full_name}}</p>',
                       is_active=True).save()
        try:
            send_system_email('test_slug', 'user@example.com', {'full_name': 'Aisha'},
                               'Fallback subject', '<p>fallback</p>')
            subject, html, to = self.calls[0]
            assert subject == 'Hi Aisha'
            assert 'Aisha' in html
            assert to == 'user@example.com'
        finally:
            self._cleanup()

    def test_falls_back_when_rendered_body_empty(self):
        from .models import EmailTemplate
        self._cleanup()
        EmailTemplate(name='t', slug='test_slug', subject='S', html_body='', is_active=True).save()
        try:
            send_system_email('test_slug', 'user@example.com', {}, 'Fallback subject', '<p>fallback</p>')
            assert self.calls[0][1] == '<p>fallback</p>'
        finally:
            self._cleanup()
