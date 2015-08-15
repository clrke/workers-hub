from django.conf.urls import url
import api.v1.views

urlpatterns = [
    url(r'^login$', api.v1.views.login),
    url(r'^requests$', api.v1.views.request),
    url(r'^requests/(?P<request_id>\d+)/proposals$', api.v1.views.proposal),
    url(r'^requests/(?P<request_id>\d+)/proposals/(?P<proposal_id>\d+)$', api.v1.views.accept_proposal),
    url(r'^workers/(?P<worker_id>\d+)$', api.v1.views.show_worker),
    url(r'^request/(?P<request_id>\d+)/$', api.v1.views.list_proposals),
]
