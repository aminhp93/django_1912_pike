
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.db.models.signals import pre_save
from django.utils.text import slugify

from videos.models import Video

# Create your models here.
class CategoryQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class CategoryManager(models.Manager):
	def get_queryset(self):
		return CategoryQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().all().active(
			).annotate(
				courses_length=Count("secondary_category", distinct=True)
			).prefetch_related("primary_category", "secondary_category")

class Category(models.Model):
	video 		= models.ForeignKey(Video, null=True, blank=True)
	title 		= models.CharField(max_length=120)
	slug 		= models.SlugField(blank=True)
	description = models.TextField()
	active 		= models.BooleanField(default=True)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = CategoryManager()

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