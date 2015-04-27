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
    url(r'^test/$', test)
]
