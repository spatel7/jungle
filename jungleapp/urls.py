from django.conf.urls import patterns, include, url
from jungleapp import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^index/$', views.index, name='index'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login/$', views.user_login, name='user_login'),
  url(r'^logout/$', views.user_logout, name='user_logout'),
  url(r'^home/', views.home, name='home'),
  url(r'^jungles/(?P<jungle_id_url>\w+)/$', views.jungle, name='jungle'),
  url(r'^jungles/(?P<jungle_id_url>\w+)/add_user/$', views.add_user, name='add_user'),
  url(r'^jungles/(?P<jungle_id_url>\w+)/write_post/$', views.write_post, name='write_post'),
  url(r'^jungles/(?P<jungle_id_url>\w+)/leave_jungle/$', views.leave_jungle, name='leave_jungle'),
  url(r'^add_jungle/$', views.add_jungle, name='add_jungle'),
)