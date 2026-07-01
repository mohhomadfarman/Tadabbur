from datetime import datetime, timezone

from mongoengine.errors import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.common.permissions import section_required
from apps.emails.models import EmailTemplate
from .models import EmailWorkflow, WorkflowSend, TRIGGER_EVENTS

# track_slug is required for these — "any track" is semantically odd for a
# per-track start/completion trigger. lesson_completed may reasonably fire on
# any lesson in any track, so it stays optional there.
TRACK_REQUIRED_TRIGGERS = ('track_started', 'track_completed')


def _iso(dt):
    return dt.isoformat() if dt else None


def _get(model, _id):
    try:
        return model.objects(id=_id).first()
    except (ValidationError, Exception):
        return None


def _workflow_row(w, with_body=False):
    data = {
        'id': str(w.id),
        'name': w.name,
        'trigger_event': w.trigger_event,
        'track_slug': w.track_slug,
        'delay_hours': w.delay_hours,
        'recheck_condition': w.recheck_condition,
        'template_id': str(w.template.id) if w.template else None,
        'subject': w.subject,
        'is_active': w.is_active,
        'audience': w.audience,
        'allowed_user_ids': w.allowed_user_ids or [],
        'created_at': _iso(w.created_at),
        'updated_at': _iso(w.updated_at),
    }
    if with_body:
        data['html_body'] = w.html_body
    return data


class AdminWorkflowListView(APIView):
    permission_classes = [section_required('automations')]

    def get(self, request):
        return Response([_workflow_row(w) for w in EmailWorkflow.objects.order_by('-created_at')])

    def post(self, request):
        d = request.data
        name = (d.get('name') or '').strip()
        if not name:
            return Response({'name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        trigger_event = (d.get('trigger_event') or '').strip()
        if trigger_event not in TRIGGER_EVENTS:
            return Response({'trigger_event': f'Must be one of {TRIGGER_EVENTS}.'}, status=status.HTTP_400_BAD_REQUEST)

        track_slug = (d.get('track_slug') or '').strip()
        if trigger_event in TRACK_REQUIRED_TRIGGERS and not track_slug:
            return Response({'track_slug': 'Required for this trigger.'}, status=status.HTTP_400_BAD_REQUEST)

        template = None
        tpl_id = d.get('template_id')
        if tpl_id:
            template = _get(EmailTemplate, tpl_id)

        # Seed subject/body from the chosen template when not supplied inline,
        # then snapshot — future template edits never retroactively change this rule.
        subject = d.get('subject')
        html_body = d.get('html_body')
        if subject is None and template:
            subject = template.subject
        if html_body is None and template:
            html_body = template.html_body

        try:
            delay_hours = max(0, int(d.get('delay_hours') or 0))
        except (TypeError, ValueError):
            return Response({'delay_hours': 'Must be a whole number.'}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now(timezone.utc)
        w = EmailWorkflow(
            name=name,
            trigger_event=trigger_event,
            track_slug=track_slug,
            delay_hours=delay_hours,
            recheck_condition=bool(d.get('recheck_condition', True)),
            template=template,
            subject=(subject or '').strip(),
            html_body=html_body or '',
            is_active=bool(d.get('is_active', True)),
            audience=(d.get('audience') or 'all').strip(),
            allowed_user_ids=d.get('allowed_user_ids') or [],
            created_at=now, updated_at=now,
        )
        w.save()
        return Response(_workflow_row(w, with_body=True), status=status.HTTP_201_CREATED)


class AdminWorkflowDetailView(APIView):
    permission_classes = [section_required('automations')]

    def get(self, request, workflow_id):
        w = _get(EmailWorkflow, workflow_id)
        if not w:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_workflow_row(w, with_body=True))

    def patch(self, request, workflow_id):
        w = _get(EmailWorkflow, workflow_id)
        if not w:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        d = request.data

        if 'name' in d:
            w.name = (d['name'] or '').strip()
        if 'trigger_event' in d:
            if d['trigger_event'] not in TRIGGER_EVENTS:
                return Response({'trigger_event': f'Must be one of {TRIGGER_EVENTS}.'}, status=status.HTTP_400_BAD_REQUEST)
            w.trigger_event = d['trigger_event']
        if 'track_slug' in d:
            w.track_slug = (d['track_slug'] or '').strip()
        if w.trigger_event in TRACK_REQUIRED_TRIGGERS and not w.track_slug:
            return Response({'track_slug': 'Required for this trigger.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'delay_hours' in d:
            try:
                w.delay_hours = max(0, int(d['delay_hours'] or 0))
            except (TypeError, ValueError):
                return Response({'delay_hours': 'Must be a whole number.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'recheck_condition' in d:
            w.recheck_condition = bool(d['recheck_condition'])
        if 'subject' in d:
            w.subject = (d['subject'] or '').strip()
        if 'html_body' in d:
            w.html_body = d['html_body'] or ''
        if 'template_id' in d:
            w.template = _get(EmailTemplate, d['template_id']) if d['template_id'] else None
        if 'is_active' in d:
            w.is_active = bool(d['is_active'])
        if 'audience' in d:
            w.audience = (d['audience'] or 'all').strip()
        if 'allowed_user_ids' in d:
            w.allowed_user_ids = d['allowed_user_ids'] or []

        w.updated_at = datetime.now(timezone.utc)
        w.save()
        return Response(_workflow_row(w, with_body=True))

    def delete(self, request, workflow_id):
        w = _get(EmailWorkflow, workflow_id)
        if not w:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Cascades WorkflowSend rows (reverse_delete_rule=CASCADE); any Celery
        # task already scheduled against this rule re-fetches by id at fire
        # time and safely no-ops once EmailWorkflow.objects(id=...) is empty.
        w.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminWorkflowSendsView(APIView):
    """Audit trail: recent sent/scheduled/skipped/failed sends for one rule."""
    permission_classes = [section_required('automations')]

    def get(self, request, workflow_id):
        w = _get(EmailWorkflow, workflow_id)
        if not w:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        rows = []
        for s in WorkflowSend.objects(workflow=w).order_by('-created_at').limit(200):
            try:
                email = s.user.email
            except Exception:
                email = ''
            rows.append({
                'id': str(s.id),
                'user_email': email,
                'track_slug': s.track_slug,
                'status': s.status,
                'scheduled_for': _iso(s.scheduled_for),
                'sent_at': _iso(s.sent_at),
                'created_at': _iso(s.created_at),
            })
        return Response(rows)
