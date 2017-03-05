from django.shortcuts import render
from django.views import View

from courses.models import Course

class HomeView(View):

	def get(self, request, *args, **kwargs):
		qs = Course.objects.all().featured().order_by("?")[:6]
		template = 'home.html'
		context = {
			"qs": qs,
		}
		return render(request, template, context)

