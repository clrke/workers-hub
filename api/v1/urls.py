from django.conf.urls import url


urlpatterns = [
    url(r'^login', 'api.v1.views.login'),
]

