from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from courses.models import Course, Lecture
from categories.models import Category

# Create your views here.

class SearchView(View):
	def get(self, request, *args, **kwargs):
		print("amin", request)
		query = request.GET.get("q")
		qs = None
		c_qs = None
		l_qs = None
		if query:
			lec_lookup = Q(title__icontains=query) \
			| Q(description__icontains=query)

			query_lookup = lec_lookup \
			| Q(category__title__icontains=query) \
			| Q(category__description__icontains=query) \
			| Q(lecture__title__icontains=query)

			qs = Course.objects.filter(query_lookup).distinct()

			qs_ids = [x.id for x in qs]
			print("minh", qs_ids)

			cat_lookup = Q(primary_category__in=qs_ids) \
			| Q(secondary_category__in=qs_ids)
			print(cat_lookup)

			c_qs = Category.objects.filter(lec_lookup | cat_lookup).distinct()

			l_qs = Lecture.objects.filter(lec_lookup).distinct()

		template = "search/default.html"
		context = {
			"qs": qs, "l_qs": l_qs, "c_qs": c_qs,
		}
		return render(request, template, context)