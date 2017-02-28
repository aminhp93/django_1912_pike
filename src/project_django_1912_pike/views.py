from django.shortcuts import render
from django.views import View

class HomeView(View):

	def get(self, request, *args, **kwargs):
		template = 'home.html'
		context = {

		}
		return render(request, template, context)

