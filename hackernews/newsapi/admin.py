from django.contrib import admin
from .models import OurNews, NewHNStories, HNew, Comments
# Register your models here.

admin.site.register(OurNews)
admin.site.register(NewHNStories)
admin.site.register(HNew)
admin.site.register(Comments)