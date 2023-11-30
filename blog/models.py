from django.conf import settings
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone



    
class Category(models.Model):
    # post = models.ForeignKey(Post,on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,null=True)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    published_date = models.DateTimeField(blank=True, null=True)
    post_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None, )  
    post_cat = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    tags = models.ManyToManyField(Tag)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
