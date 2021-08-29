from django.urls import path

from .views import sign_up , verify , verify_success

app_name = 'users'

urlpatterns = [
    path('sign_up/', sign_up, name='sign-up'),
    path('verify/', verify, name='verify'),
    path('verify_success/', verify_success, name='verify-success'),
]
