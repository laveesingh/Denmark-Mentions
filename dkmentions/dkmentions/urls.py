from django.conf.urls import url
from django.contrib import admin

from . import views
from app import views as app_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.main),
    url(r'^update', app_views.update)
]
