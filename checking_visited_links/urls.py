from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    path('checker/', include('checker.urls', namespace='checker')),
]
