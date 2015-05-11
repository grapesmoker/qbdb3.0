from django.conf.urls import include, url
from django.contrib import admin

from qbdb.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'qbdb_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main),
    url(r'^add_tournament/$', add_tournament),
    url(r'^tournaments/$', tournaments),
    url(r'^tournament/(?P<id>[\d]+)$', get_tournament),
    url(r'^packet/(?P<id>[\d]+)$', get_packet),
    url(r'^search/$', search),
    url(r'^faq/$', faq),
    url(r'^register/$', register),
    url(r'^logout/$', do_logout),
    url(r'^login/$', do_login),
    url(r'^vote/$', vote)
]
