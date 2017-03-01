from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	CreateView,
	ListView, 
	DetailView,
	UpdateView, 
	DeleteView
	)

from .forms import CourseForm
from .models import Course

# Create your views here.

class CourseCreateView(CreateView):
	model = Course
	form_class = CourseForm

class CourseListView(ListView):
	queryset = Course.objects.all()

class CourseDetailView(DetailView):
	queryset = Course.objects.all()

	# def get_object(self):
	# 	abc = self.kwargs.get("slug")
	# 	print("test", abc)
	# 	obj = get_object_or_404(Course, slug=abc)
	# 	print(obj)
	# 	return get_object_or_404(Course, slug=abc)

class CourseUpdateView(UpdateView):
	model = Course
	form_class = CourseForm

class CourseDeleteView(DeleteView):
	queryset = Course.objects.all()
	success_url = "/courses/"