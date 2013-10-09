from django.conf.urls import patterns, url

from teams import views

urlpatterns = patterns('',
    url(r'^$', views.team_manager, name='team_manager'),
)
