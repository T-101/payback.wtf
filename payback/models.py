from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import TimeStampedModel
from singleton_models.models import SingletonModel

from payback.helpers import send_registration_email


class PaybackUser(TimeStampedModel):
    handle = models.CharField(max_length=100)
    group = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_id = RandomCharField(length=32, unique=True, lowercase=True, include_digits=True)

    initial_email_sent = models.BooleanField(default=False)

    name_visible = models.BooleanField(default=True)
    visitor_accepted = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=False)

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

    @classmethod
    def registration_open(cls):
        instance = cls.load()
        return instance.registration_start < timezone.localtime()

    @staticmethod
    def load():
        return Settings.objects.first()

    def __str__(self):
        return "Settings"


@receiver(pre_save, sender=PaybackUser)
def send_email(sender, instance, **kwargs):
    try:
        old_instance = PaybackUser.objects.get(pk=instance.pk)
    except PaybackUser.DoesNotExist:
        if PaybackUser.objects.count() <= 100:
            return send_registration_email(instance)
        else:
            return

    if old_instance.email != instance.email:
        return send_registration_email(instance)
