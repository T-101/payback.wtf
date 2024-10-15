from django.contrib import admin

from .models import PaybackUser, Questionnaire, Settings
from .helpers import send_registration_email, send_declined_email


class InlineQuestionnaire(admin.TabularInline):
    model = Questionnaire
    extra = 0


@admin.register(PaybackUser)
class PaybackUserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'handle', 'email', 'place_in_line',
        'name_visible_icon', 'visitor_accepted_icon', 'payment_status_icon', 'initial_email_sent_icon', 'created'
    ]
    list_filter = ['visitor_accepted', 'payment_status', 'initial_email_sent',
                   'name_visible', 'created', 'modified']
    search_fields = ['handle', 'group', 'email', 'user_id']
    readonly_fields = ['user_id']
    inlines = [InlineQuestionnaire]

    @staticmethod
    def _create_icon_method(field_name, short_description):
        def icon_method(self, obj):
            return getattr(obj, field_name)

        icon_method.boolean = True
        icon_method.short_description = short_description
        icon_method.admin_order_field = field_name
        return icon_method

    name_visible_icon = _create_icon_method('name_visible', 'Visible')
    visitor_accepted_icon = _create_icon_method('visitor_accepted', 'Accepted')
    payment_status_icon = _create_icon_method('payment_status', 'Payment')
    initial_email_sent_icon = _create_icon_method('initial_email_sent', 'Initial email')

    actions = ['send_registration_email', 'send_declined_email', 'regenerate_user_id']

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

    def regenerate_user_id(self, request, queryset):
        for user in queryset:
            user.regenerate_user_id()
        self.message_user(request, f"{len(queryset)} User IDs regenerated.")


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'modified', 'user', 'wants_food']
    list_filter = ['created', 'modified', 'user', 'wants_food']
    autocomplete_fields = ['user']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'registration_start']
    list_filter = ['registration_start']
