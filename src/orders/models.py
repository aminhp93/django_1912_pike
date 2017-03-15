
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

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


