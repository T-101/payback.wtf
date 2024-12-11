import os
import threading

from django.contrib.sites.models import Site
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from sendgrid import EventWebhook, EventWebhookHeader


class EmailThread(threading.Thread):
    def __init__(self, subject: str, recipient_list: list, body: str = "", context=None, connection=None,
                 text_filepath: str = ""):
        if context is None:
            context = {}
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.text_filepath = text_filepath
        self.context = context
        self.connection = connection
        threading.Thread.__init__(self)

    def run(self):
        if self.text_filepath:
            text_content = render_to_string(self.text_filepath, context=self.context)
        else:
            text_content = self.body

        msg = mail.EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.recipient_list,
            connection=self.connection
        )
        if self.text_filepath:
            html_filepath = self.text_filepath.replace(".txt", ".html")
            if os.path.exists(os.path.join(settings.BASE_DIR, "payback", "templates", html_filepath)):
                html_content = render_to_string(html_filepath, context=self.context)
                msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_async_mail(**kwargs):
    EmailThread(**kwargs).start()


def send_registration_email(payback_user):
    email_be = mail.get_connection()
    if payback_user.use_alternate_email_backend:
        email_be.host = settings.EMAIL_HOST_ALTERNATE
        email_be.username = settings.EMAIL_HOST_USER_ALTERNATE
        email_be.password = settings.EMAIL_HOST_PASSWORD_ALTERNATE
    send_async_mail(
        subject="Welcome to Payback!",
        text_filepath="snippets/email-registration.txt",
        context={
            "site": Site.objects.get_current().domain,
            "place_in_line": payback_user.place_in_line,
            "handle": payback_user.handle,
            "user_id": payback_user.user_id},
        recipient_list=[payback_user.email],
        connection=email_be)


def send_payment_email(payback_user):
    email_be = mail.get_connection()
    if payback_user.use_alternate_email_backend:
        email_be.host = settings.EMAIL_HOST_ALTERNATE
        email_be.username = settings.EMAIL_HOST_USER_ALTERNATE
        email_be.password = settings.EMAIL_HOST_PASSWORD_ALTERNATE
    send_async_mail(
        subject="Payback ticket payment",
        text_filepath="snippets/email-payment.txt",
        context={
            "site": Site.objects.get_current().domain,
            "handle": payback_user.handle,
            "user_id": payback_user.user_id},
        recipient_list=[payback_user.email],
        connection=email_be)


def send_payment_reminder_email(payback_user):
    email_be = mail.get_connection()
    if payback_user.use_alternate_email_backend:
        email_be.host = settings.EMAIL_HOST_ALTERNATE
        email_be.username = settings.EMAIL_HOST_USER_ALTERNATE
        email_be.password = settings.EMAIL_HOST_PASSWORD_ALTERNATE
    send_async_mail(
        subject="Payback ticket payment reminder",
        text_filepath="snippets/email-payment-reminder.txt",
        context={
            "site": Site.objects.get_current().domain,
            "handle": payback_user.handle,
            "user_id": payback_user.user_id},
        recipient_list=[payback_user.email],
        connection=email_be)


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
