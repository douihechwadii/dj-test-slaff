from django.contrib import admin
from django.urls import path
from dinar.views import run

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',run, name="dashboard" ),
]
