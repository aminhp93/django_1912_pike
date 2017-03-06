from django.shortcuts import render

from django.views.generic import (
		ListView,
	)
# Create your views here.
from .models import Shopping

class ShoppingListView(ListView):
	queryset = Shopping.objects.all()
