from django.contrib import admin
from .models import Photo, Comment  # We import the photo model

# Register your models here.
admin.site.register(Photo)
admin.site.register(Comment)
