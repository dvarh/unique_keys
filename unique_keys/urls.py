"""unique_keys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from api_keys import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api_keys/$', views.IssuedKey.as_view(), name='issue_key'),
    url(r'^api_keys/(?P<key>[a-zA-Z0-9]{4})/$', views.UseKey.as_view(), name='use_key'),
    url(r'^api_keys/(?P<key>[a-zA-Z0-9]{4})/info$', views.KeyInfo.as_view(), name='key_info'),
    url(r'^api_keys/count$', views.KeyCount.as_view(), name='key_counts'),
]
