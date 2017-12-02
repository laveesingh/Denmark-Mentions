from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from app import views as app_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.main),
    url(r'^update', app_views.update),
    url(r'^user_list_update', app_views.user_list_update)
]

urlpatterns += staticfiles_urlpatterns()
