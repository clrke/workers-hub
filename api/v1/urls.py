from django.conf.urls import url
import api.v1.views

urlpatterns = [
    url(r'^login', api.v1.views.login),
]
