from django.conf.urls import url

from . import views

app_name = 'simc'

urlpatterns = [
    url(r'^talents/(?P<class_id>[0-9]{1,2})/(?P<spec>[0-3])$', views.get_talents, name='talents'),
    url(r'^character/$', views.CharacterView.as_view(), name='character'),
]
