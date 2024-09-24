import json

import stripe
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.crypto import get_random_string

from payback.models import PaybackUser

stripe.api_key = settings.STRIPE_API_KEY


@csrf_exempt
def create_checkout_session(request, user_id):
    if not PaybackUser.objects.filter(user_id=user_id).exists():
        messages.add_message(request, messages.ERROR, 'Malformed request')
        return redirect('payback:visitor-detail', user_id=user_id)

    if settings.DEBUG:
        domain_url = 'http://localhost:8000'
    else:
        domain_url = f'https://{Site.objects.get_current().domain}'

    stripe_session = get_random_string(length=128)
    request.session['stripe_session'] = stripe_session

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': settings.STRIPE_TICKET,
                    'quantity': 1,
                },
                # {
                #     # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                #     'price': settings.STRIPE_TICKET_FOOD,
                #     'quantity': 1,
                # },
            ],
            payment_intent_data={
                'metadata': {'user_id': user_id,
                             'stripe_session': stripe_session}
            },
            mode='payment',
            success_url=domain_url + reverse('payback:stripe-success'),
            cancel_url=domain_url + reverse('payback:stripe-cancel'),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


def stripe_success(request):
    return render(request, 'stripe/success.html')


def stripe_cancel(request):
    return render(request, 'stripe/cancel.html')


@csrf_exempt
@require_http_methods(["POST"])
def stripe_payment_webhook(request):
    try:
        event = stripe.Webhook.construct_event(request.body, request.headers.get('Stripe-Signature'),
                                               settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        print(f'Error parsing payload: {e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f'Error verifying webhook signature: {e}')
        return HttpResponse(status=400)

    try:
        user_id = event.data.object.metadata.get('user_id')
        stripe_session = event.data.object.metadata.get('stripe_session')
    except KeyError:
        return HttpResponse(status=400)

    for session in Session.objects.iterator():
        if session.get_decoded().get("stripe_session") == stripe_session:
            PaybackUser.objects.filter(user_id=user_id).update(payment_status=True)
            return HttpResponse(status=200)

    return HttpResponse(status=400)
