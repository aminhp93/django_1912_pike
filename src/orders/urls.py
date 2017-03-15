from django.conf.urls import url
from .views import (
		# ShoppingCreateView,
		OrderDetailView,
		OrderListView,
		# ShoppingUpdateView,
		# ShoppingDeleteView,
	)

urlpatterns = [
	url(r'^$', OrderListView.as_view(), name="list"),
	# url(r'^create/$', ShoppingCreateView.as_view(), name="create"),
	url(r'^(?P<pk>\d+)/$', OrderDetailView.as_view(), name="detail"),
	# url(r'^(?P<slug>[\w-]+)/update/$', ShoppingUpdateView.as_view(), name="update"),
	# url(r'^(?P<slug>[\w-]+)/delete/$', ShoppingDeleteView.as_view(), name="delete"),

]