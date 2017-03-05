from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, Prefetch
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from categories.models import Category
from videos.models import Video

# Create your models here.
class MyCourse(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL)
	courses 	= models.ManyToManyField("Course", related_name="owned", blank=True)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} | {} courses".format(str(self.user.username), str(self.courses.all().count()))

def post_save_user_create(sender, instance, created, *args, **kwargs):
	if created:
		MyCourse.objects.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)

class CourseQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(Q(secondary__slug__iexact='featured'))

	def lectures(self):
		return self.prefetch_related(
				'lecture_set'
			)

	def owned(self, user):
		if user.is_authenticated():
			qs = MyCourse.objects.filter(user=user)
		else:
			qs = MyCourse.objects.all()
		return self.prefetch_related(
				Prefetch(
					"owned",
					queryset=qs,
					to_attr="is_owner",
					)
			)

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
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL)
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

	def get_purchase_url(self):
		return reverse("courses:purchase", kwargs={"slug": self.slug})


def pre_save_course_receiver(sender, instance, *args, **kwargs):
	# print(sender, instance, args, kwargs)
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_course_receiver, sender=Course)

class Lecture(models.Model):
	course 		= models.ForeignKey(Course)
	video 		= models.ForeignKey(Video)
	title 		= models.CharField(max_length=120)
	slug 		= models.SlugField(blank=True)
	free 		= models.BooleanField(default=True)
	description = models.TextField()
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["title"]

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("courses:lecture-detail", kwargs={"cslug": self.course.slug, "lslug": self.slug})

def pre_save_lecture_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_lecture_receiver, sender=Lecture)








