from django.urls import path, re_path
from . import views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/upload/', views.upload),
    path('api/run_model/', views.run_model),
]