from django.contrib import admin
from .models import Forum, Topic, Post, Site

admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Site)
# Register your models here.
