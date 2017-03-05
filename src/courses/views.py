from django.http import Http404
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
		obj = None
		
		course_qs = Course.objects.filter(slug=cslug)#.lectures().owned(self.request.user)
		# print(qs, "===", qs.lectures(), "====", qs.lectures().owned(self.request.user))
		if not course_qs.exists():
			raise Http404

		course = course_qs.first()
		lecture_qs = course.lecture_set.filter(slug=lslug)

		if not lecture_qs.exists():
			raise Http404

		obj = lecture_qs.first()

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

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()
		return super().form_valid(form)

class CourseListView(ListView):
	
	def get_queryset(self):
		user = self.request.user
		qs = Course.objects.all()
		if user.is_authenticated():
			qs = qs.owned(user)
		return qs

class CourseDetailView(DetailView):
	queryset = Course.objects.all()

	def get_object(self):
		slug = self.kwargs.get("slug")
		qs = Course.objects.filter(slug=slug).lectures().owned(self.request.user)
		print(qs, "test")
		if qs.exists():
			obj = qs.first()
			return obj
		raise Http404

class CourseUpdateView(UpdateView):
	model = Course
	form_class = CourseForm

class CourseDeleteView(DeleteView):
	queryset = Course.objects.all()
	success_url = "/courses/"