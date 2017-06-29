from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^pokes$', views.pokes),
    url(r'^logout$', views.logout),
    url(r'^addpoke/(?P<id>\d+)$', views.addpoke),
]