from django.conf.urls import url
import views.login

urlpatterns = [
    url(r'^login', views.login),
]
