from django.conf.urls import url
from rest_framework.authtoken import views

from yt_dashboard.views import (

    account, index
)

app_name = 'yt_dashboard'

urlpatterns = [

    url(r'^api-token-auth', views.obtain_auth_token),
    url(r'logout', account.logout),

    # account
    url(r'^account/getall$', account.getAll, name='account_getall'),
    url(r'^account/update$', account.update, name='account_update'),
    url(r'^account/change_password$', account.change_password),
    url(r'^account/request_payout$', account.request_payout, name='account_request_payout'),
    # remove the $ so refreshing is not a problem
    url(r'^', index.index, name='yt_dashboard_main'),

]
