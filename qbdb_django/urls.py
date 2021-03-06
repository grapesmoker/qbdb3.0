from django.conf.urls import include, url
from django.contrib import admin

from qbdb.views import *
from qbdb.api import *

from tastypie.api import Api

qbdb_api = Api(api_name='v1')
qbdb_api.register(TournamentResource())
qbdb_api.register(PacketResource())
qbdb_api.register(TossupResource())
qbdb_api.register(BonusResource())
qbdb_api.register(BonusPartResource())

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
    url(r'^random/$', get_random_question),
    url(r'^search/$', search),
    url(r'^faq/$', faq),
    url(r'^register/$', register),
    url(r'^logout/$', do_logout),
    url(r'^login/$', do_login),
    url(r'^vote/$', vote),

    url(r'^api/', include(qbdb_api.urls))
]
