from django.conf.urls import include, url
import api.v1.urls

urlpatterns = [
    url(r'^v1/', include(api.v1.urls)),
]

