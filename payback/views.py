from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DetailView

from payback.forms import PaybackUserForm
from payback.models import PaybackUser, Settings


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


class VisitorDetailView(FormView):
    template_name = 'visitor-detail.html'
    form_class = PaybackUserForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = PaybackUser.objects.get(user_id=self.kwargs['user_id'])
        return kwargs
