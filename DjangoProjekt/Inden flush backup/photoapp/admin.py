from django.contrib import admin
from .models import Photo, Comment, Profile  # We import the photo model

# Register your models here.
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Profile)
