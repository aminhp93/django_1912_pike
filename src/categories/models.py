
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from videos.models import Video

# Create your models here.
class Category(models.Model):
	video 		= models.ForeignKey(Video, null=True, blank=True)
	title 		= models.CharField(max_length=120)
	slug 		= models.SlugField(blank=True)
	description = models.TextField()
	active 		= models.BooleanField(default=True)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("categories:detail", kwargs={"slug": self.slug})

def pre_save_category_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_category_receiver, sender=Category)