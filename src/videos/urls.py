from django.conf.urls import url
from .views import (
		VideoCreateView,
		VideoDetailView,
		VideoListView,
		VideoUpdateView,
		VideoDeleteView,
	)

urlpatterns = [
	url(r'^$', VideoListView.as_view(), name="list"),
	url(r'^create/$', VideoCreateView.as_view(), name="create"),
	url(r'^(?P<slug>[\w-]+)/$', VideoDetailView.as_view(), name="detail"),
	url(r'^(?P<slug>[\w-]+)/update/$', VideoUpdateView.as_view(), name="update"),
	url(r'^(?P<slug>[\w-]+)/delete/$', VideoDeleteView.as_view(), name="delete"),

]