from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from jungle import settings

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
  url('', include('jungleapp.urls')),
)

urlpatterns += patterns('',
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)