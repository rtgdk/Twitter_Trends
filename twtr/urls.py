from django.conf.urls import include, url,patterns
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twtr2.views.home', name='home'),
    # url(r'^twtr2/', include('twtr2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^(/)?$', RedirectView.as_view(url='/app/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('app.urls')),
)

urlpatterns += staticfiles_urlpatterns()
