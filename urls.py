from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^create$', views.create, name='create'),
    url(r'^place$', views.place, name='place'),
]