from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import UserCheckout, Order
# Create your views here.

class OrderDetail(DetailView):
	model = Order

	def dispatch(self, request, *args, **kwargs):
		try:
			user_checkout_id = self.request.session.get("user_checkout_id")
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
		except UserCheckout.DoesNotExist:
			
			user_checkout = UserCheckout.objects.get(user=request.user)
		except:
			
			user_checkout = None
		
		obj = self.get_object()
		if obj.user == user_checkout and user_checkout is not None:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404

class OrderList(ListView):
	queryset = Order.objects.all()

	# def get_queryset(self):
	# 	user_checkout_id = self.request.user.id
	# 	user_checkout = UserCheckout.objects.get(id=user_checkout_id)
	# 	return super().get_queryset().filter(user=user_checkout)


