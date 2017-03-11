from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save

from courses.models import Course

# Create your models here.

class Cart(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	item  			= models.ManyToManyField(Course, through="CartItem")
	timestamp 		= models.DateTimeField(auto_now_add=True, auto_now=False)
	updated 		= models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal 		= models.DecimalField(max_digits=50, decimal_places=2, default=0)
	tax_percentage 	= models.DecimalField(max_digits=50, decimal_places=2, default=0.08)
	tax_total 		= models.DecimalField(max_digits=50, decimal_places=2, default=0)
	total 			= models.DecimalField(max_digits=50, decimal_places=2, default=0)

	def __str__(self):
		return str(self.id)

	def update_subtotal(self):
		subtotal = 0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.total_line_item
		self.subtotal = subtotal
		self.save()

def cart_pre_save_receiver(sender, instance, *args, **kwargs):
	subtotal = instance.subtotal
	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2)
	total = round(subtotal + tax_total, 2)
	instance.tax_total = "{}".format(tax_total, '.2f')
	instance.total = "{}".format(total, '.2f')

pre_save.connect(cart_pre_save_receiver, sender=Cart)

class CartItem(models.Model):
	cart 			= models.ForeignKey("Cart")
	item 			= models.ForeignKey(Course)
	quantity 		= models.PositiveIntegerField(default=1)
	total_line_item = models.DecimalField(max_digits=50, decimal_places=2, default=0)

	def __str__(self):
		return str(self.item.title)

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	quantity = Decimal(instance.quantity)
	if quantity >= 1:
		price = Decimal(instance.item.price)
		instance.total_line_item = quantity * price

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, created, *args, **kwargs):
	instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)