from django.conf.urls import url
from .views import (
		# ShoppingCreateView,
		# ShoppingDetailView,
		ShoppingListView,
		# ShoppingUpdateView,
		# ShoppingDeleteView,
	)

urlpatterns = [
	url(r'^$', ShoppingListView.as_view(), name="list"),
	# url(r'^create/$', ShoppingCreateView.as_view(), name="create"),
	# url(r'^(?P<slug>[\w-]+)/$', ShoppingDetailView.as_view(), name="detail"),
	# url(r'^(?P<slug>[\w-]+)/update/$', ShoppingUpdateView.as_view(), name="update"),
	# url(r'^(?P<slug>[\w-]+)/delete/$', ShoppingDeleteView.as_view(), name="delete"),

]