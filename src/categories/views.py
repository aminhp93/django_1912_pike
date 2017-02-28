from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	CreateView,
	ListView, 
	DetailView,
	UpdateView, 
	DeleteView
	)

from .forms import CategoryForm
from .models import Category

# Create your views here.

class CategoryCreateView(CreateView):
	model = Category
	form_class = CategoryForm

class CategoryListView(ListView):
	queryset = Category.objects.all()

class CategoryDetailView(DetailView):
	queryset = Category.objects.all()

	# def get_object(self):
	# 	abc = self.kwargs.get("slug")
	# 	print("test", abc)
	# 	obj = get_object_or_404(Category, slug=abc)
	# 	print(obj)
	# 	return get_object_or_404(Category, slug=abc)

class CategoryUpdateView(UpdateView):
	model = Category
	form_class = CategoryForm

class CategoryDeleteView(DeleteView):
	queryset = Category.objects.all()
	success_url = "/categories/"