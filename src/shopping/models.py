from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

def handle_upload(instance, filename):
	if instance.slug:
		return "{}/images/{}".format(instance.slug, filename)
	return "unknown/images/{}".format(filename)

class Shopping(models.Model):

	title = models.CharField(max_length=120)
	slug = models.SlugField(blank=True)
	link = models.TextField()
	image = models.ImageField(
			upload_to=handle_upload,
			height_field='image_height',
			width_field='image_width',
			blank=True, null=True
		)
	image_height = models.IntegerField(blank=True, null=True)
	image_width = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return str(self.title)

def pre_save_shopping_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_shopping_receiver,sender=Shopping)		



