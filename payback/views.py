import json

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, FormView, ListView, UpdateView

from payback.forms import PaybackUserForm
from payback.models import PaybackUser, Settings
from payback.helpers import verify_sendgrid_webhook


class LandingPageView(TemplateView):
    template_name = 'landing-page.html'


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = PaybackUserForm
    success_url = reverse_lazy('payback:visitors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.load()
        context['registration_open'] = context['settings'].registration_open()
        context['registration_start'] = context['settings'].registration_start
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class InformationView(TemplateView):
    template_name = 'information.html'


class VisitorListView(ListView):
    template_name = 'visitors.html'
    model = PaybackUser
    queryset = (PaybackUser.objects
                .annotate(paid_count=Count('id', filter=Q(payment_status=True)))
                .filter(visitor_accepted=True)
                )


class VisitorDetailView(UpdateView):
    template_name = 'visitor-detail.html'
    form_class = PaybackUserForm

    def get_object(self, queryset=None):
        return PaybackUser.objects.get(user_id=self.kwargs['user_id'])

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'User updated successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payback:visitor-detail', kwargs={'user_id': self.object.user_id})


@csrf_exempt
@require_http_methods(["POST"])
def sendgrid_delivery_webhook(request):
    try:
        post_data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400, content='Invalid JSON body')

    try:
        if not verify_sendgrid_webhook(request):
            return HttpResponse(status=403, content='Invalid webhook signature')
    except KeyError:
        return HttpResponse(status=403, content='Invalid webhook signature')

    emails = []

    for item in post_data:
        email = item['email']
        if email:
            emails.append(email)

    PaybackUser.objects.filter(email__in=emails).update(initial_email_sent=True)
    return HttpResponse(status=200)
