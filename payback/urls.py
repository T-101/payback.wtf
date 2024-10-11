from django.urls import path

from payback.payment_views import create_checkout_session
from payback.views import (LandingPageView, RegistrationView, VisitorListView, InformationView, TimetableView,
                           VisitorDetailView, sendgrid_delivery_webhook)
from payback.payment_views import stripe_success, stripe_cancel, stripe_payment_webhook

app_name = 'payback'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('visitors/', VisitorListView.as_view(), name='visitors'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('information/', InformationView.as_view(), name='information'),
    path('visitor/<str:user_id>/', VisitorDetailView.as_view(), name='visitor-detail'),
    # Stripe urls
    path('stripe/create-checkout-session/<str:user_id>/', create_checkout_session,
         name='stripe-create-checkout-session'),
    path('stripe/success.html', stripe_success, name='stripe-success'),
    path('stripe/cancel.html', stripe_cancel, name='stripe-cancel'),
    path('stripe/webhook/', stripe_payment_webhook, name='stripe-webhook'),
    # Sendgrid webhook
    path('sendgrid/webhook/', sendgrid_delivery_webhook, name='sendgrid-delivery-webhook'),
]
