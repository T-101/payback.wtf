from django.urls import path

from payback.views import LandingPageView, RegistrationView, VisitorListView, InformationView, VisitorDetailView

app_name = 'payback'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('visitors/', VisitorListView.as_view(), name='visitors'),
    path('information/', InformationView.as_view(), name='information'),
    path('visitor/<str:user_id>/', VisitorDetailView.as_view(), name='visitor-detail'),
]
