from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


ARTICLE_TYPES = ["story", "job", "comment", "poll", "pollopt"]
ARTICLE_CHOICES = [(ARTICLE_TYPES[i], ARTICLE_TYPES[i]) for i in range(0,5)]


class OurNews(models.Model):
    
    
    by = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    score = models.IntegerField(_("News Score"))
    time_created = models.DateTimeField(_("time created"), auto_now=True)
    title = models.CharField(_("article title"), max_length=50)
    type = models.CharField(_("article type"), max_length=10, choices=ARTICLE_CHOICES, default="story")
    content = models.CharField(_("article content"), max_length=1000)
    
    
    def __str__(self):
        return f"{self.title} written by {self.by}"


class NewHNStories(models.Model):
    hn_id = models.IntegerField(_("HN unique ID"))
    
    def __str__(self):
        return f"{self.hn_id}"


class HNew(models.Model):
    
    # pk_id = models.ForeignKey(NewHNStories, verbose_name=_("HN Unique ID"), on_delete=models.CASCADE, default=1)
    pk_id = models.IntegerField(_("HN unique ID"))
    by = models.CharField(_("Author"), max_length=50)
    score = models.IntegerField(_("News Score"))
    time_created = models.DateTimeField(_("time created"), auto_now=True)
    title = models.CharField(_("article title"), max_length=50)
    type = models.CharField(_("article type"), max_length=10, choices=ARTICLE_CHOICES, default="story")
    url = models.URLField(_("Article link"), max_length=200) 
    
    
    def __str__(self):
        return f"{self.title} written by {self.by}"
    
    
class Comments(models.Model):
    type = models.CharField(_("article type"), max_length=10, choices=ARTICLE_CHOICES, default="comment")
    by = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    time = models.DateTimeField(_("Time Created"), auto_now=True)
    parent = models.ForeignKey(OurNews, verbose_name=_("Article"), on_delete=models.CASCADE)
    text = models.CharField(_("Comment"), max_length=250)
    
    def __str__(self):
        return f"Comment written by {self.by}"
    
    