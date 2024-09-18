import sendgrid

from django.conf import settings


def sendgrid_email(to, subject, content):
    sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    from_email = sendgrid.Email(settings.SENDGRID_FROM_EMAIL)
    mail = sendgrid.Mail(from_email, sendgrid.Email(to), subject, sendgrid.Content("text/plain", content))
    response = sg.client.mail.send.post(request_body=mail.get())
    return response
