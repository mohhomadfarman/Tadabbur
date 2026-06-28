# Import the Celery app on Django startup so that @shared_task (e.g. in
# apps.emails.tasks) binds to *this* app — and its Redis broker from settings —
# instead of Celery's default amqp broker. Without this, calling .delay() from
# the web process tries to reach RabbitMQ on localhost and fails with a 500.
from celery_app import app as celery_app  # noqa: F401

__all__ = ('celery_app',)
