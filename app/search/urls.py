# howdy/urls.py
from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^getContent/$', views.getContent),
    # url(r'^paper/(?P<id>\w{0,50})/$', views.page_view),
    url(r'^paper/$', views.page_view),
]