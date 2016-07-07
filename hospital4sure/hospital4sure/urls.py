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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from auths import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('visitor.urls')),
    url(r'^$', views.index , name='index' ),
    url(r'^signup/$', views.signup , name='signup' ),
    url(r'^logout/$', views.logoutuser , name='logoutuser' ),
    url(r'^sendotp/$', views.sendotp , name='sendotp' ),
    url(r'^changeotp/$', views.changeotp , name='changeotp' ),
    url(r'^login/$', views.loginuser , name='loginuser' ),
    url(r'^signupprocess/$', views.signupprocess , name='signupprocess' ),
    url(r'^category/$', views.category , name='category' ),
    url(r'^subcategory/$', views.subcategory , name='subcategory' ),
    url(r'^test/$', views.test , name='test' ),
    url(r'^form/$', views.form , name='form' ),
    url(r'^submit/$', views.submit , name='submit' ),
    url(r'^profile/$', views.profile , name='profile' ),
    url(r'^edit/$', views.edit , name='edit' ),
    url(r'^checkph/$', views.checkph , name='checkph' ),
    url(r'^search/$', views.search , name='search' ),
    url(r'^get-cities/$', views.getcities , name='get-cities' ),
    url(r'^get-local/$', views.getlocal , name='get-local' ),
    url(r'^get-spec/$', views.getspec , name='get-spec' ),
    url(r'^(?P<category_name>[a-z,A-Z,0-9-]+)/(?P<username>[a-z,A-Z,0-9-]+)/$', views.viewprofile , name='viewprofile' ),
    url(r'^link/(?P<category_name>[a-z,A-Z,0-9-]+)/(?P<spec>[a-z,A-Z,0-9,\s-]+)/$', views.searchlink , name='viewprofile' ),
    
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)