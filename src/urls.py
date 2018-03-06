"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see
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
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from Enlight import views 
from accounts_info import views as accounts_info_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^signup/$',accounts_info_views.signup,name = 'signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    url(r'^forum/(?P<pk>\d+)/$', views.topic_list, name='topic'),
    url(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    url(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/delete/$', views.delete, name='delete'),
    url(r'^forum/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^$',views.forum_list,name='home')
]
