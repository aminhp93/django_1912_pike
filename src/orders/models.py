
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from carts.models import Cart

import braintree

if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

class UserCheckout(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	email 			= models.EmailField(unique=True)
	braintree_id 	= models.CharField(max_length=120, blank=True, null=True)


	def __str__(self):
		return self.email

	@property
	def get_braintree_id(self):

		instance = self
		print(instance)
		if not instance.braintree_id:
			result = braintree.Customer.create({
					"email": instance.email
				})
			print(result, "line 32")
			if result.is_success:
				instance.braintree_id = result.customer.id
				instance.save()
		return instance.braintree_id

	def get_client_token(self):
		customer_id = self.get_braintree_id
		if customer_id:
			client_token = braintree.ClientToken.generate({
					"customer_id": customer_id
				})
			return client_token
		return None

def update_braintree_id(sender, instance, *args, **kwargs):
	if not instance.braintree_id:
		instance.get_braintree_id

post_save.connect(update_braintree_id, sender=UserCheckout)


ORDER_STATUS_CHOICE = (
		('created', 'Created'),
		('paid', 'Paid'),
		('shipped', 'Shipped'),
	)

class Order(models.Model):
	status 		= models.CharField(max_length=120, choices=ORDER_STATUS_CHOICE, default='created')
	cart 		= models.ForeignKey(Cart)
	user 		= models.ForeignKey(UserCheckout, null=True)
	order_total = models.DecimalField(decimal_places=2, max_digits=50)

	def __str__(self):
		return str(self.cart.id)

def order_pre_save(sender, instance, *args, **kwargs):
	
	cart_total = instance.cart.total
	instance.order_total = cart_total

pre_save.connect(order_pre_save, sender=Order)





















