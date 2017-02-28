from django.contrib import admin

from .models import Video
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp"]
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ["title"]
	class Meta:
		model = Video

admin.site.register(Video, VideoAdmin)

