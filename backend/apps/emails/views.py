from datetime import datetime, timezone

from django.http import HttpResponse
from django.utils.html import escape
from mongoengine.errors import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from .models import EmailTemplate, EmailCampaign, Unsubscribe, EmailSettings
from .segments import segment_options, resolve_segment, read_unsub_token
from .tasks import send_campaign, deliver_message


def _iso(dt):
    return dt.isoformat() if dt else None


def _mask(value):
    """Never reveal the stored password — only a harmless hint that one is set."""
    value = (value or '').strip()
    if not value:
        return ''
    return '••••' + value[-2:] if len(value) >= 2 else '••••'


def _settings_payload(s):
    return {
        'host': s.host,
        'port': s.port,
        'username': s.username,
        'use_tls': bool(s.use_tls),
        'use_ssl': bool(s.use_ssl),
        'from_email': s.from_email,
        # Password is NEVER returned in full — only whether one exists + a hint.
        'has_password': bool((s.password or '').strip()),
        'password_hint': _mask(s.password),
        'configured': s.is_configured(),
        'updated_at': _iso(s.updated_at),
    }


def _parse_dt(val):
    if not val or not isinstance(val, str):
        return None
    try:
        return datetime.fromisoformat(val.replace('Z', '+00:00'))
    except ValueError:
        return None


def _template_row(t, with_body=False):
    data = {
        'id': str(t.id),
        'name': t.name,
        'subject': t.subject,
        'created_at': _iso(t.created_at),
        'updated_at': _iso(t.updated_at),
    }
    if with_body:
        data['html_body'] = t.html_body
    return data


def _campaign_row(c, with_body=False):
    data = {
        'id': str(c.id),
        'name': c.name,
        'subject': c.subject,
        'segment': c.segment,
        'status': c.status,
        'template_id': str(c.template.id) if c.template else None,
        'scheduled_at': _iso(c.scheduled_at),
        'sent_at': _iso(c.sent_at),
        'stats': c.stats or {},
        'created_at': _iso(c.created_at),
        'updated_at': _iso(c.updated_at),
    }
    if with_body:
        data['html_body'] = c.html_body
    return data


def _get(model, _id):
    try:
        return model.objects(id=_id).first()
    except (ValidationError, Exception):
        return None


# ── SMTP settings ────────────────────────────────────────────────────────────

class AdminEmailSettingsView(APIView):
    """Manage the SMTP config from the admin panel. Password is write-only (masked
    on read; only updated when a non-empty value is supplied)."""
    permission_classes = [section_required('email')]

    def get(self, request):
        return Response(_settings_payload(EmailSettings.get_solo()))

    def patch(self, request):
        s = EmailSettings.get_solo()
        d = request.data
        if 'host' in d:
            s.host = (d['host'] or '').strip()
        if 'port' in d:
            try:
                s.port = int(d['port'])
            except (TypeError, ValueError):
                return Response({'port': 'Must be a number.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'username' in d:
            s.username = (d['username'] or '').strip()
        if 'use_tls' in d:
            s.use_tls = bool(d['use_tls'])
        if 'use_ssl' in d:
            s.use_ssl = bool(d['use_ssl'])
        if 'from_email' in d:
            s.from_email = (d['from_email'] or '').strip()
        # Password: an explicit clear wins; otherwise update only when a non-empty
        # value is supplied (a blank value leaves the stored password intact).
        if d.get('clear_password') is True:
            s.password = ''
        elif isinstance(d.get('password'), str) and d['password'].strip():
            s.password = d['password']
        s.updated_at = datetime.now(timezone.utc)
        s.save()
        return Response(_settings_payload(s))


class AdminTestSendView(APIView):
    """Send a single test email synchronously with arbitrary subject/body (e.g. the
    content currently in the template or campaign editor). Returns the real SMTP
    error so the admin can debug their settings."""
    permission_classes = [section_required('email')]

    def post(self, request):
        email = (request.data.get('email') or '').strip()
        if not email:
            return Response({'email': 'A test recipient email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        subject = (request.data.get('subject') or '').strip()
        html_body = request.data.get('html_body') or ''
        try:
            from .tasks import deliver_message
            deliver_message(subject or '(no subject)', html_body, email)
        except Exception as e:
            return Response({'detail': f'Send failed: {e}'}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({'sent': True})


# ── Templates ────────────────────────────────────────────────────────────────

class AdminEmailTemplateListView(APIView):
    permission_classes = [section_required('email')]

    def get(self, request):
        return Response([_template_row(t) for t in EmailTemplate.objects.order_by('-created_at')])

    def post(self, request):
        name = (request.data.get('name') or '').strip()
        if not name:
            return Response({'name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        now = datetime.now(timezone.utc)
        t = EmailTemplate(
            name=name,
            subject=(request.data.get('subject') or '').strip(),
            html_body=request.data.get('html_body') or '',
            created_at=now, updated_at=now,
        )
        t.save()
        return Response(_template_row(t, with_body=True), status=status.HTTP_201_CREATED)


class AdminEmailTemplateDetailView(APIView):
    permission_classes = [section_required('email')]

    def get(self, request, template_id):
        t = _get(EmailTemplate, template_id)
        if not t:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_template_row(t, with_body=True))

    def patch(self, request, template_id):
        t = _get(EmailTemplate, template_id)
        if not t:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        if 'name' in request.data:
            t.name = (request.data['name'] or '').strip()
        if 'subject' in request.data:
            t.subject = (request.data['subject'] or '').strip()
        if 'html_body' in request.data:
            t.html_body = request.data['html_body'] or ''
        t.updated_at = datetime.now(timezone.utc)
        t.save()
        return Response(_template_row(t, with_body=True))

    def delete(self, request, template_id):
        t = _get(EmailTemplate, template_id)
        if not t:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        t.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Campaigns ────────────────────────────────────────────────────────────────

class AdminEmailCampaignListView(APIView):
    permission_classes = [section_required('email')]

    def get(self, request):
        return Response([_campaign_row(c) for c in EmailCampaign.objects.order_by('-created_at')])

    def post(self, request):
        name = (request.data.get('name') or '').strip()
        if not name:
            return Response({'name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        template = None
        tpl_id = request.data.get('template_id')
        if tpl_id:
            template = _get(EmailTemplate, tpl_id)

        # Seed subject/body from the chosen template when not supplied inline.
        subject = request.data.get('subject')
        html_body = request.data.get('html_body')
        if subject is None and template:
            subject = template.subject
        if html_body is None and template:
            html_body = template.html_body

        now = datetime.now(timezone.utc)
        c = EmailCampaign(
            name=name,
            template=template,
            subject=(subject or '').strip(),
            html_body=html_body or '',
            segment=(request.data.get('segment') or 'all_users').strip(),
            status='draft',
            created_at=now, updated_at=now,
        )
        c.save()
        return Response(_campaign_row(c, with_body=True), status=status.HTTP_201_CREATED)


class AdminEmailCampaignDetailView(APIView):
    permission_classes = [section_required('email')]

    def get(self, request, campaign_id):
        c = _get(EmailCampaign, campaign_id)
        if not c:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_campaign_row(c, with_body=True))

    def patch(self, request, campaign_id):
        c = _get(EmailCampaign, campaign_id)
        if not c:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        if c.status in ('sending', 'sent'):
            return Response({'detail': 'A sent or sending campaign cannot be edited.'}, status=status.HTTP_400_BAD_REQUEST)
        d = request.data
        if 'name' in d:
            c.name = (d['name'] or '').strip()
        if 'subject' in d:
            c.subject = (d['subject'] or '').strip()
        if 'html_body' in d:
            c.html_body = d['html_body'] or ''
        if 'segment' in d:
            c.segment = (d['segment'] or 'all_users').strip()
        if 'template_id' in d:
            c.template = _get(EmailTemplate, d['template_id']) if d['template_id'] else None
        c.updated_at = datetime.now(timezone.utc)
        c.save()
        return Response(_campaign_row(c, with_body=True))

    def delete(self, request, campaign_id):
        c = _get(EmailCampaign, campaign_id)
        if not c:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        c.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendCampaignView(APIView):
    """Send now, or schedule for a future time if `scheduled_at` is provided."""
    permission_classes = [section_required('email')]

    def post(self, request, campaign_id):
        c = _get(EmailCampaign, campaign_id)
        if not c:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        if c.status in ('sending', 'sent'):
            return Response({'detail': 'This campaign has already been sent.'}, status=status.HTTP_400_BAD_REQUEST)
        if c.status not in ('draft', 'scheduled', 'paused', 'failed'):
            return Response({'detail': f'Cannot send a campaign with status "{c.status}".'}, status=status.HTTP_400_BAD_REQUEST)
        if not c.subject or not c.html_body:
            return Response({'detail': 'Add a subject and body before sending.'}, status=status.HTTP_400_BAD_REQUEST)

        eta = _parse_dt(request.data.get('scheduled_at'))
        now = datetime.now(timezone.utc)
        if eta and eta > now:
            c.scheduled_at = eta
            c.status = 'scheduled'
            c.updated_at = now
            c.save()
            send_campaign.apply_async(args=[str(c.id)], eta=eta)
            return Response({'scheduled': True, 'scheduled_at': _iso(eta)})

        c.status = 'sending'
        c.updated_at = now
        c.save()
        send_campaign.delay(str(c.id))
        return Response({'sending': True})


class PauseCampaignView(APIView):
    """Toggle a scheduled campaign between paused and scheduled.
    - scheduled → paused  (the queued Celery task will bail on status check)
    - paused → scheduled  (re-queues with the original scheduled_at if still future,
                           otherwise moves back to draft so admin can re-schedule)"""
    permission_classes = [section_required('email')]

    def post(self, request, campaign_id):
        c = _get(EmailCampaign, campaign_id)
        if not c:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        now = datetime.now(timezone.utc)

        if c.status == 'scheduled':
            c.status = 'paused'
            c.updated_at = now
            c.save()
            return Response(_campaign_row(c))

        if c.status == 'paused':
            if c.scheduled_at and c.scheduled_at > now:
                c.status = 'scheduled'
                c.updated_at = now
                c.save()
                send_campaign.apply_async(args=[str(c.id)], eta=c.scheduled_at)
                return Response(_campaign_row(c))
            else:
                # Scheduled time has passed — move to draft so admin re-schedules.
                c.status = 'draft'
                c.scheduled_at = None
                c.updated_at = now
                c.save()
                return Response({**_campaign_row(c), 'info': 'Scheduled time has passed — campaign moved back to draft. Set a new send time.'})

        return Response({'detail': f'Cannot pause/resume a campaign with status "{c.status}".'}, status=status.HTTP_400_BAD_REQUEST)


class TestSendView(APIView):
    """Send a campaign test email synchronously (like the template test-send) so
    it surfaces the real SMTP error and never depends on the Celery worker."""
    permission_classes = [section_required('email')]

    def post(self, request, campaign_id):
        c = _get(EmailCampaign, campaign_id)
        if not c:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        email = (request.data.get('email') or '').strip()
        if not email:
            return Response({'email': 'A test recipient email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            deliver_message(c.subject or '(no subject)', c.html_body, email)
        except Exception as e:
            return Response({'detail': f'Send failed: {e}'}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({'sent': True})


class AdminSegmentsView(APIView):
    """Segment options + a recipient-count preview for the campaign editor."""
    permission_classes = [section_required('email')]

    def get(self, request):
        opts = segment_options()
        preview = request.query_params.get('segment')
        if preview:
            return Response({'segment': preview, 'count': len(resolve_segment(preview))})
        return Response(opts)


# ── Public unsubscribe ───────────────────────────────────────────────────────

class UnsubscribeView(APIView):
    """One-click unsubscribe target embedded in every campaign email."""
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token', '')
        email = read_unsub_token(token)
        if not email:
            return HttpResponse(_html_page('This unsubscribe link is invalid or has expired.'), status=400)
        if not Unsubscribe.objects(email=email).first():
            try:
                Unsubscribe(email=email).save()
            except Exception:
                pass  # already unsubscribed (unique-index race)
        return HttpResponse(_html_page(f'{escape(email)} has been unsubscribed. You will no longer receive marketing emails.'))


def _html_page(message):
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Unsubscribe — Tadabbur</title></head>'
        '<body style="font-family:system-ui,sans-serif;background:#f7f7f8;margin:0;padding:48px 16px;text-align:center">'
        '<div style="max-width:440px;margin:0 auto;background:#fff;border:1px solid #eee;border-radius:16px;padding:32px">'
        '<h1 style="font-size:18px;color:#111;margin:0 0 8px">Tadabbur</h1>'
        f'<p style="font-size:14px;color:#555;margin:0">{message}</p>'
        '</div></body></html>'
    )
