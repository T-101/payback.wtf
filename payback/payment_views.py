import stripe
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_API_KEY


@csrf_exempt
def create_checkout_session(req):
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
            mode='payment',
            success_url='https://dev.payback.wtf' + reverse('payback:stripe-success'),
            cancel_url='https://dev.payback.wtf' + reverse('payback:stripe-cancel'),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


def stripe_success(request):
    return render(request, 'stripe/success.html')


def stripe_cancel(request):
    return render(request, 'stripe/cancel.html')


@csrf_exempt
def stripe_payment_webhook(request):
    print("REQ BODY", request.body)
