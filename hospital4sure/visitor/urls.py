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
from visitor import views

urlpatterns = [    
    url(r'^$', views.index , name='visitorindex' ),
    url(r'^signup/$', views.signup , name='visitorsignup' ),
    url(r'^logout/$', views.logoutuser , name='visitorlogoutuser' ),
    url(r'^sendotp/$', views.sendotp , name='visitorsendotp' ),
    url(r'^changeotp/$', views.changeotp , name='changeotp' ),
    url(r'^login/$', views.loginuser , name='visitorloginuser' ),
    url(r'^checkph/$', views.checkph , name='checkph' ),
    url(r'^book/$', views.book , name='book' ),
    url(r'^rate/$', views.rate , name='rate' ),
    url(r'^review/$', views.review , name='review' ),
    url(r'^signupprocess/$', views.signupprocess , name='visitorsignupprocess' ),
]
