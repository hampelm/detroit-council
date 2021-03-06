from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from core.views import *

urlpatterns = patterns('',
    # Example:
    ('^$', home),

    url(r'^member/(?P<member>[-\w]+)$', member, name="member"),
    url(r'^contract/(?P<contract>[-\d]+)$', contract, name="contract"),
   
    url(r'^meeting/(\d{4})/(\d+)/(\d+)/$', meeting, name="meeting"),
    url(r'^item/(\w+)$', item, name="sitem"),
    url(r'^page/(\d+)$', page, name="page"),

    url(r'^search/$', search, name="search"),
    
    url(r'^test/$', test, name="search"),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)


if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"^assets/(?P<path>.*)$", 'static.serve', {
            "document_root": settings.MEDIA_ROOT,})
    )
