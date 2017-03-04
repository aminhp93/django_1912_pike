from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	View,
	CreateView,
	ListView, 
	DetailView,
	UpdateView, 
	DeleteView,
	RedirectView,
	)

from .forms import CourseForm
from .models import Course, MyCourse, Lecture

# Create your views here.

class LectureDetailView(View):
	def get(self, request, cslug=None, lslug=None, *args, **kwargs):
		obj = Lecture.objects.all()

		template = "courses/lecture_detail.html"

		context = {
			"object": obj
		}

		return render(request, template, context)


class CoursePurchaseView(RedirectView):
	permanent = False

	def get_redirect_url(self, slug=None):
		qs = Course.objects.filter(slug=slug)#.owned(self.request.user)
		if qs.exists():
			user = self.request.user
			if user.is_authenticated():
				my_course, created = MyCourse.objects.get_or_create(user=user)
				if created:
					my_course.user = user
					my_course.courses = qs
					my_course.save()
				else:
					my_course = user.mycourse
					my_course.courses.add(qs.first())
		return "/courses/"

class CourseCreateView(CreateView):
	model = Course
	form_class = CourseForm

class CourseListView(ListView):
	
	def get_queryset(self):
		user = self.request.user
		qs = Course.objects.all()
		if user.is_authenticated():
			qs = qs.owned(user)
		return qs

class CourseDetailView(DetailView):
	queryset = Course.objects.all()

	# def get_object(self):
	# 	abc = self.kwargs.get("slug")
	# 	obj = get_object_or_404(Course, slug=abc)
	# 	return get_object_or_404(Course, slug=abc)

class CourseUpdateView(UpdateView):
	model = Course
	form_class = CourseForm

class CourseDeleteView(DeleteView):
	queryset = Course.objects.all()
	success_url = "/courses/"