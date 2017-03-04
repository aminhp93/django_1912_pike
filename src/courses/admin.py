from django.contrib import admin

from .forms import LectureAdminForm
from .models import Course, MyCourse, Lecture

# Register your models here.
class LectureInline(admin.TabularInline):
	model = Lecture
	prepopulated_fields = {"slug": ("title", )}
	form = LectureAdminForm
	extra = 1

class CourseAdmin(admin.ModelAdmin):
	# list_display = ["title", "timestamp"]
	inlines = [LectureInline]
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ["title"]
	class Meta:
		model = Course

admin.site.register(Course, CourseAdmin)
admin.site.register(MyCourse)
