from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'workers_hub.views.home', name='home'),
    url(r'^api/', include('api.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
