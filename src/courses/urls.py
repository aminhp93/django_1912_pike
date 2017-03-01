from django.conf.urls import url
from .views import (
		CourseCreateView,
		CourseDetailView,
		CourseListView,
		CourseUpdateView,
		CourseDeleteView,
	)

urlpatterns = [
	url(r'^$', CourseListView.as_view(), name="list"),
	url(r'^create/$', CourseCreateView.as_view(), name="create"),
	url(r'^(?P<slug>[\w-]+)/$', CourseDetailView.as_view(), name="detail"),
	url(r'^(?P<slug>[\w-]+)/update/$', CourseUpdateView.as_view(), name="update"),
	url(r'^(?P<slug>[\w-]+)/delete/$', CourseDeleteView.as_view(), name="delete"),

]