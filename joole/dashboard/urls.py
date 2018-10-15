__author__ = 'xavier'
from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.ClientFormView.as_view(), name='client-form'),
    url(r'^results/(?P<client_id>.+)$', views.results, name='results'),
    url(r'^api/client/(?P<client_id>.+)$', views.api, name='api')
]