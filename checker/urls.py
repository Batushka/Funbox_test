from django.urls import path, re_path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import visited_links, visited_domains

app_name = 'checker'


urlpatterns = [
    path('visited-links/', visited_links, name='visited-links'),
    path('visited-domains/', visited_domains, name='visited-domains')
]
urlpatterns = format_suffix_patterns(urlpatterns)
