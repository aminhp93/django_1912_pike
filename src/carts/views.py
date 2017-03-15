from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView

from courses.models import Course
from orders.models import UserCheckout

from .models import Cart, CartItem



# Create your views here.
class CartView(View):
	model = Cart
	template_name = 'carts/view.html'

	def get_object(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(id=cart_id)

		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart

	def get(self, request, *args, **kwargs):
		cart = self.get_object()
		print(request, "line 25")
		print(request.GET)
		item_id = request.GET.get("item")
		print(item_id, "line 27")

		if item_id:
			item_instance = get_object_or_404(Course, id=item_id)
			quanity = request.GET.get("quantity", 1)

			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)

			print(cart_item)

		template = self.template_name

		context = {
			"object": self.get_object()
		}
		return render(request, template, context)


class CheckoutView(DetailView):
	model = Cart
	template_name = "carts/checkout_view.html"

	def get_object(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			return None
		cart = Cart.objects.get(id=cart_id)
		return cart

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)

		if self.request.user.is_authenticated():
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()
			self.request.session['user_checkout_id'] = user_checkout.id
		else:
			pass

		return context









