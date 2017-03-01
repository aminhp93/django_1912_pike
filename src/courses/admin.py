from django.contrib import admin

from .models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
	# list_display = ["title", "timestamp"]
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ["title"]
	class Meta:
		model = Course

admin.site.register(Course, CourseAdmin)

