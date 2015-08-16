from django.conf.urls import url

import api.v1.views.public
import api.v1.views.customer
import api.v1.views.worker

urlpatterns = [
    url(r'^login$', api.v1.views.public.login),
    url(r'^requests$', api.v1.views.customer.request),
    url(r'^requests/(?P<request_id>\d+)$', api.v1.views.customer.cancel_request),
    url(r'^requests/(?P<request_id>\d+)/proposals$', api.v1.views.worker.proposal),
    url(r'^requests/(?P<request_id>\d+)/proposals/all$', api.v1.views.customer.list_proposals),
    url(r'^requests/(?P<request_id>\d+)/proposals/(?P<proposal_id>\d+)$', api.v1.views.customer.accept_proposal),
    url(r'^requests/(?P<request_id>\d+)/review$', api.v1.views.customer.write_review),
    url(r'^workers/(?P<worker_id>\d+)$', api.v1.views.customer.show_worker),
    url(r'^reviews$', api.v1.views.customer.show_reviews),
    url(r'^professions', api.v1.views.public.professions),
    url(r'^worker/requests$', api.v1.views.worker.requests),
    url(r'^worker/proposals$', api.v1.views.worker.proposals),
    url(r'^worker/accepted$', api.v1.views.worker.accepted),
    url(r'^worker/requests/(?P<request_id>\d+)/review$', api.v1.views.worker.write_review),
]
