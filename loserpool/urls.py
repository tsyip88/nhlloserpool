from django.conf.urls import patterns, include, url
from django.contrib import admin
from loserpool import views
import django.contrib.auth.views
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teams/', include('teams.urls', namespace="teams")),
    url(r'^matchups/', include('matchups.urls', namespace="matchups")),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user_options/$', views.user_options, name='user_options'),
    url(r'^change_password/$', django.contrib.auth.views.password_change, {'template_name':'change_password.html'}, name='password_change'),
    url(r'^password_changed/$', django.contrib.auth.views.password_change_done, {'template_name':'password_changed.html'}),
    url(r'^admin_actions/$', views.admin_actions, name='admin_actions'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)