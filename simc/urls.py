from django.conf.urls import url

from . import views

app_name = 'simc'

urlpatterns = [
    url(r'^talents/(?P<class_slug>[-a-z]+)/(?P<spec>[-a-z]+)$', views.get_talents, name='talents'),
    url(r'^talents/$', views.get_select_spec, name='select-spec'),
]
