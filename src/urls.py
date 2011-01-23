from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('main.urls', 'main')),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )