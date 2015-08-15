from django.conf.urls import url
import api.v1.views

urlpatterns = [
    url(r'^login', api.v1.views.login),
    url(r'^request', api.v1.views.create_request),
    url(r'^proposal', api.v1.views.create_proposal),
    url(r'^workers/(?P<id>\d+)', api.v1.views.show_worker),
]
