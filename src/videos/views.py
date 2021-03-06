from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	CreateView,
	ListView, 
	DetailView,
	UpdateView, 
	DeleteView
	)

from .forms import VideoForm
from .models import Video

# Create your views here.

class VideoCreateView(CreateView):
	model = Video
	form_class = VideoForm

class VideoListView(ListView):
	paginate_by = 4

	queryset = Video.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		print(context, dir(context))
		return context

class VideoDetailView(DetailView):
	queryset = Video.objects.all()

	# def get_object(self):
	# 	abc = self.kwargs.get("slug")
	# 	print("test", abc)
	# 	obj = get_object_or_404(Video, slug=abc)
	# 	print(obj)
	# 	return get_object_or_404(Video, slug=abc)

class VideoUpdateView(UpdateView):
	model = Video
	form_class = VideoForm

class VideoDeleteView(DeleteView):
	queryset = Video.objects.all()
	success_url = "/videos/"