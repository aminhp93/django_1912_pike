from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify

from categories.models import Category
# Create your models here.
class CourseQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class CourseManager(models.Manager):
	def get_queryset(self):
		return CourseQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().all().active()

def handle_upload(instance, filename):
	if instance.slug:
		return "{}/images/{}".format(instance.slug, filename)
	return "unknown/images/{}".format(filename)


class Course(models.Model):
	title 		= models.CharField(max_length=120)
	slug 		= models.SlugField(blank=True)
	category 	= models.ForeignKey(Category, related_name="primary_category", null=True, blank=True)
	secondary 	= models.ManyToManyField(Category, related_name="secondary_category", blank=True)
	image 		= models.ImageField(
			upload_to=handle_upload,
			height_field='image_height',
			width_field='image_width',
			blank=True,null=True
		)
	image_height= models.IntegerField(blank=True,null=True)
	image_width	= models.IntegerField(blank=True,null=True)
	price		= models.DecimalField(decimal_places=2, max_digits=100)
	active 		= models.BooleanField(default=True)
	description = models.TextField()
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = CourseManager()
	
	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("courses:detail", kwargs={"slug": self.slug})


def pre_save_course_receiver(sender, instance, *args, **kwargs):
	# print(sender, instance, args, kwargs)
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_course_receiver, sender=Course)
