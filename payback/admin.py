from django.contrib import admin

from .models import PaybackUser, Questionnaire, Settings
from .helpers import send_registration_email, send_declined_email


class InlineQuestionnaire(admin.TabularInline):
    model = Questionnaire
    extra = 0


@admin.register(PaybackUser)
class PaybackUserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'handle', 'group', 'email',
        'name_visible', 'visitor_accepted', 'payment_status', 'created'
    ]
    list_filter = ['created', 'modified', 'name_visible', 'visitor_accepted', 'payment_status']
    search_fields = ['handle', 'group', 'email', 'user_id']
    readonly_fields = ['user_id']
    inlines = [InlineQuestionnaire]

    actions = ['send_registration_email', 'send_declined_email']

    def send_registration_email(self, request, queryset):
        for user in queryset:
            send_registration_email(user)
        self.message_user(request, f"{len(queryset)} Registration emails sent.")

    send_registration_email.short_description = "Send registration email"

    def send_declined_email(self, request, queryset):
        queryset.update(visitor_accepted=False)
        for user in queryset:
            send_declined_email(user)
        self.message_user(request, f"{len(queryset)} Declined emails sent.")

    send_declined_email.short_description = "Decline user and send email"


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'modified', 'user', 'wants_food']
    list_filter = ['created', 'modified', 'user', 'wants_food']
    autocomplete_fields = ['user']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'registration_start']
    list_filter = ['registration_start']
