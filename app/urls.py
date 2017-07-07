from django.conf.urls import patterns, url
from app import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^ajaxtweets/(?P<woeid>[-\w]+)/(?P<hashtag>[-\w]+)/(?P<count>[-\w]+)/$',views.tweet_fetch, name ="Fetch tweets"),
	url(r'^search/$', views.autocompleteModel , name = 'search'),
	url(r'^hashtag/(?P<hasht>[-\w]+)/$', views.hashtag , name = 'hashtag'),
	url(r'^moretweets/(?P<hashtag>[-\w]+)/(?P<currt>[-\w]+)$', views.moretweets , name = 'moretweets'),
	#url(r'^other/$', views.other, name="other"),
]
