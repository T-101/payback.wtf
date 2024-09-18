from django.contrib import admin

from .models import PaybackUser, Questionnaire, Settings


@admin.register(PaybackUser)
class PaybackUserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'handle', 'group', 'email',
        'name_visible', 'visitor_accepted', 'payment_status', 'created'
    ]
    list_filter = ['created', 'modified', 'name_visible', 'visitor_accepted', 'payment_status']
    search_fields = ['handle', 'group', 'email', 'user_id']
    readonly_fields = ['user_id']


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'modified', 'user', 'wants_food']
    list_filter = ['created', 'modified', 'user', 'wants_food']
    autocomplete_fields = ['user']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'registration_start']
    list_filter = ['registration_start']
