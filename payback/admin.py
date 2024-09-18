from django.contrib import admin

from .models import PaybackUser, Questionnaire, Settings


@admin.register(PaybackUser)
class PaybackUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'handle',
        'group',
        'email',
        'user_id',
        'name_visible',
        'visitor_accepted',
        'payment_status',
    )
    list_filter = (
        'created',
        'modified',
        'name_visible',
        'visitor_accepted',
        'payment_status',
    )
    search_fields = ('handle', 'group', 'email')
    readonly_fields = ['user_id']


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'user', 'wants_food')
    list_filter = ('created', 'modified', 'user', 'wants_food')


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'registration_start')
    list_filter = ('registration_start',)
