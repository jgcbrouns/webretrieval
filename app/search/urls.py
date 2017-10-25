# howdy/urls.py
from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^getContent/$', views.getContent),
    # url(r'^paper/(?P<id>\w{0,50})/$', views.page_view),
    url(r'^paper/$', views.page_view),
    url(r'^Topics/$', views.topics_view),
    url(r'^Author/$', views.author_view),
    url(r'^clusters/$', views.clusters_view),
    url(r'^clusters/cluster1$', views.cluster1_view),
    url(r'^clusters/cluster2$', views.cluster2_view),
    url(r'^clusters/cluster3$', views.cluster3_view),
    url(r'^clusters/cluster4$', views.cluster4_view),
    url(r'^clusters/cluster5$', views.cluster5_view),
    url(r'^clusters/AuthorClustering$', views.authorclustering)
]