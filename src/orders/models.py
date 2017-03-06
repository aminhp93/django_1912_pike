from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete


# Create your models here.
import braintree

if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

class UserCheckout(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True) #not required
	email = models.EmailField(unique=True) #-> required
	braintree_id = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.email

	@property
	def get_braintree_id(self, ):
		instance = self
		if not instance.braintree_id:
			result = braintree.Customer.create({
					"email": instance.email,
				})
			if result.is_success:
				print(result.customer)
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

ORDER_STATUS_CHOICES = (
		('created', 'Created'),
		('paid', 'Paid'),
	)

class Order(models.Model):
	status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
	user = models.ForeignKey(UserCheckout, null=True)
	order_total = models.DecimalField(decimal_places=2, max_digits=50)
	order_id = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		return reverse('order-detail', kwargs={"pk": self.pk})

	# def mark_completed(self, order_id=None):
	# 	self.status = 'paid'
	# 	if order_id and not self.order_id:
	# 		self.order_id = order_id
	# 	self.save()

	class Meta:
		ordering = ["-id"]





