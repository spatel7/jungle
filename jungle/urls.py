from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
  url('', include('jungleapp.urls')),
)

urlpatterns += staticfiles_urlpatterns()