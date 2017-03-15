from django.views.generic import DetailView, ListView

from .models import Order

class OrderDetailView(DetailView):
	model = Order

class OrderListView(ListView):
	queryset = Order.objects.all()