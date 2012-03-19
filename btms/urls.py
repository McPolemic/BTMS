from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'btms.timetrack.views.index'),
    # url(r'^$', 'btms.views.home', name='home'),
    # url(r'^btms/', include('btms.foo.urls')),

    url(r'^$', 'timetrack.views.index'),
    url(r'^entry/$', 'timetrack.views.index'),
    url(r'^entry/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'timetrack.views.weekly'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
