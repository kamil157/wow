from django.conf.urls import url

from . import views

app_name = 'simc'

urlpatterns = [
    url(r'^talents/$', views.TalentsView.as_view(), name='talents'),
]
