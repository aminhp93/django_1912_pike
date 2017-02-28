from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.
class Video(models.Model):
	embed_code 		= models.TextField()
	title 			= models.CharField(max_length=120)
	slug 			= models.SlugField(blank=True)
	free			= models.BooleanField(default=True)
	member_required = models.BooleanField(default=False)
	updated 		= models.DateTimeField(auto_now=True)
	timestamp		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("videos:detail", kwargs={"slug": self.slug})

def pre_save_video_receiver(sender, instance, *args, **kwargs):
	# print(sender, instance, args, kwargs)
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_video_receiver, sender=Video)





	