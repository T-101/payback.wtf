from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from payback.helpers import send_registration_email

from singleton_models.models import SingletonModel


class PaybackUser(TimeStampedModel):
    handle = models.CharField(max_length=100)
    group = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_id = RandomCharField(length=32, unique=True, lowercase=True, include_digits=True)
    place_in_line = models.IntegerField(default=0)

    initial_email_sent = models.BooleanField(default=False)
    use_alternate_email_backend = models.BooleanField(default=False)

    name_visible = models.BooleanField(default=True)
    visitor_accepted = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=False)

    def regenerate_user_id(self):
        self.user_id = ""
        self.save()

    def __str__(self):
        return self.handle


class Questionnaire(TimeStampedModel):
    user = models.OneToOneField(PaybackUser, on_delete=models.CASCADE, related_name='questionnaire')
    wants_food = models.BooleanField(default=True)

    def __str__(self):
        return self.user.handle


class Settings(SingletonModel):
    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    registration_start = models.DateTimeField()

    def registration_open(self):
        return self.registration_start < timezone.localtime()

    @staticmethod
    def load():
        return Settings.objects.first()

    def __str__(self):
        return "Settings"


@receiver(pre_save, sender=PaybackUser)
def send_email_if_email_changed(sender, instance, **kwargs):

    if instance.place_in_line == 0:
        last_position = PaybackUser.objects.order_by("place_in_line").last().place_in_line
        instance.place_in_line = last_position + 1

    if not settings.SEND_EMAILS:
        return

    try:
        old_instance = PaybackUser.objects.get(pk=instance.pk)
    except PaybackUser.DoesNotExist:
        return

    if old_instance.email != instance.email:
        return send_registration_email(instance)


@receiver(post_save, sender=PaybackUser)
def send_initial_email(sender, instance, created, **kwargs):
    if created and settings.SEND_EMAILS and instance.place_in_line <= 100:
        return send_registration_email(instance)
