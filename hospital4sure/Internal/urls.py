"""hospital4sure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from Internal import views

urlpatterns = [    
    url(r'^$', views.index , name='visitorindex' ),
    url(r'^login/$', views.logineventuser , name='logineventuser' ),
    url(r'^dashboard/$', views.dashboard , name='dashboard' ),
    url(r'^add/$', views.add , name='add' ),
    url(r'^edit/(?P<id>[0-9-]+)/$', views.edit , name='edit' ),
    url(r'^view/(?P<id>[0-9-]+)/$', views.view , name='view' ),
    url(r'^logout/$', views.logouteventuser , name='visitorlogouteventuser' ),
]
