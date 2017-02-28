from django.conf.urls import url
from .views import (
		CategoryCreateView,
		CategoryDetailView,
		CategoryListView,
		CategoryUpdateView,
		CategoryDeleteView,
	)

urlpatterns = [
	url(r'^$', CategoryListView.as_view(), name="list"),
	url(r'^create/$', CategoryCreateView.as_view(), name="create"),
	url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name="detail"),
	url(r'^(?P<slug>[\w-]+)/update/$', CategoryUpdateView.as_view(), name="update"),
	url(r'^(?P<slug>[\w-]+)/delete/$', CategoryDeleteView.as_view(), name="delete"),

]