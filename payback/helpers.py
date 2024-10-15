import os
import threading

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from sendgrid import EventWebhook, EventWebhookHeader


class EmailThread(threading.Thread):
    def __init__(self, subject: str, text_filepath: str, context: dict, recipient_list: list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.text_filepath = text_filepath
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        text_content = render_to_string(self.text_filepath, context=self.context)

        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.recipient_list
        )
        html_filepath = self.text_filepath.replace(".txt", ".html")
        if os.path.exists(os.path.join(settings.BASE_DIR, "payback", "templates", html_filepath)):
            html_content = render_to_string(html_filepath, context=self.context)
            msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_async_mail(**kwargs):
    EmailThread(**kwargs).start()


def send_registration_email(payback_user):
    send_async_mail(
        subject="Welcome to Payback!",
        text_filepath="snippets/email-registration.txt",
        context={
            "site": Site.objects.get_current().domain,
            "place_in_line": payback_user.place_in_line,
            "handle": payback_user.handle,
            "user_id": payback_user.user_id},
        recipient_list=[payback_user.email])


def send_declined_email(payback_user):
    send_async_mail(
        subject="Your PayBack registration was declined",
        text_filepath="snippets/email-declined.txt",
        context={},
        recipient_list=[payback_user.email])


def verify_sendgrid_webhook(request):
    event_webhook = EventWebhook()
    key = settings.SENDGRID_WEBHOOK_VERIFICATION_KEY

    ec_public_key = event_webhook.convert_public_key_to_ecdsa(key)

    return event_webhook.verify_signature(
        request.body.decode('latin-1'),
        request.headers[EventWebhookHeader.SIGNATURE],
        request.headers[EventWebhookHeader.TIMESTAMP],
        ec_public_key
    )

