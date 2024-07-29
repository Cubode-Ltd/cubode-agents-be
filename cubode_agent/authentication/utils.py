from django.template.loader import render_to_string
from django.conf import settings

from django.core.mail import EmailMessage


def send_template_email(template_name, to, subject, context, sender=None):
    if sender is None:
        sender = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(template_name, context)
    send_email(to, subject, message, sender)


def send_email(receiver_email, subject_email, body_email, sender=None):
    if sender is None:
        sender = getattr(settings, 'EMAIL_SENDER', getattr(settings, 'DEFAULT_FROM_EMAIL', 'cubode@support.com'))

    email = EmailMessage(
        subject=subject_email,
        body=body_email,
        from_email=sender,
        to=[receiver_email],
    )
    email.content_subtype = "html"  # This is critical for sending HTML emails
    email.send()
