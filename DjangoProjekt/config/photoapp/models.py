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
import random
import time
import textwrap
from string import ascii_letters
from django.utils import timezone


class Photo(models.Model):

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(default=timezone.now)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    likes = models.ManyToManyField(get_user_model(), related_name='photos')

    tags = TaggableManager()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def save(self):

        # Memegenrator:
        file1 = open(
            r'C:\Users\afkaf\Downloads\card and text\cardsagainstadvanced\cards.txt')
        file2 = open(
            r'C:\Users\afkaf\Downloads\card and text\cardsagainstadvanced\words.txt')

        Sætning = file1.readlines()
        SætningVal = random.choice(Sætning)

        Ærstatning = file2.readlines()
        ÆrstatningVal = random.choice(Ærstatning)

        Tekst = SætningVal.replace("blank", ÆrstatningVal)

        # Billedegenering:

        myFont = ImageFont.truetype('C:\Windows\Fonts\Tahoma.ttf', 50)

        im = Image.open(self.image)

        output = BytesIO()

        I2 = ImageDraw.Draw(im)

        stroke_color = (0, 0, 0)

        avg_char_width = sum(myFont.getsize(
            char)[0] for char in ascii_letters) / len(ascii_letters)

        max_char_count = int(im.size[0] * .618 / avg_char_width)

        Tekst = textwrap.fill(text=Tekst, width=max_char_count)

        I2.text((im.size[0]/2, im.size[1] / 2), Tekst, font=myFont,
                fill="#ffffff", stroke_width=1, stroke_fill=stroke_color, anchor='rs')

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
