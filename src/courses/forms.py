from django import forms

from videos.models import Video
from .models import Course, Lecture

class CourseForm(forms.ModelForm):
	
	class Meta:
		model = Course
		fields = [
			"title",
			"category",
			"price",
			"active",
			"image",
			"description",
		]

class LectureAdminForm(forms.ModelForm):
	class Meta:
		model = Lecture
		fields = [
			"video",
			"free",
			"title",
			"slug",
			"description",
			# "course",
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		obj = kwargs.get("instance")
		qs = Video.objects.all().unused()
		if obj:
			if obj.video:
				this_ = Video.objects.filter(pk=obj.video.pk)
				qs = (qs|this_)
		self.fields["video"].queryset = qs
