from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from .views import company_dashboard

app_name = 'company_dashboard'

urlpatterns = [
    url(r'yay', company_dashboard.index),

]