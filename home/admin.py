from django.contrib import admin
from .models import *
from .models import Blog, Profile, BlogPost

#admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Blog)