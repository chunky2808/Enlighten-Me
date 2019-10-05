from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Forum(models.Model):
    name = models.CharField(max_length = 50,unique=True)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_count(self):
        return Post.objects.filter(topic__forum=self).count()

    def get_last_post(self):
        a = Post.objects.filter(topic__forum=self).order_by('-created_at').first()  
        return a  
            

class Topic(models.Model):
    subject = models.CharField(max_length = 256)
    last_updated = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(Forum,related_name = 'topics')
    started_by = models.ForeignKey(User,related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def delete_thread(self,pk):
        a = Topic.objects.get(pk=pk)
        return a.delete()


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        return self.message


class Site(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=100)
    created_by = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
