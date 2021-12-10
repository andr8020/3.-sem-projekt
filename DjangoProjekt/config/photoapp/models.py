# photoapp/models.py
from PIL.Image import Image
from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.urls import reverse
from PIL import ImageDraw, Image, ImageFont
from io import BytesIO
from django.core.files.uploadhandler import InMemoryUploadedFile
import sys


class Photo(models.Model):

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    likes = models.ManyToManyField(get_user_model(), related_name='photos')

    tags = TaggableManager()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def save(self):
        im = Image.open(self.image)

        output = BytesIO()

        I1 = ImageDraw.Draw(im)

        myFont = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 65)

        # Add Text to an image
        I1.text((28, 36), "nice Car", font=myFont, fill=(255, 0, 0))

        im.save(output, format='JPEG', quality=90)
        output.seek(0)

        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                          sys.getsizeof(output), None)

        super(Photo, self).save()


class Comment(models.Model):
    post = models.ForeignKey(
        Photo, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='navn')
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('list')
