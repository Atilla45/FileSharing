from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from users.models import Profile



# USER_MODEL = get_user_model()
class Post(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
    # share = models.ForeignKey(Sh)
	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

class SharingFile(models.Model):
    user = models.ForeignKey(User, related_name='sharing_user', on_delete=models.CASCADE)
    title = models.ForeignKey(Post, related_name='sharing_title' ,on_delete=models.CASCADE)
    file = models.ForeignKey(Post, related_name='sharing_file', on_delete=models.CASCADE)
    sharing_type = models.IntegerField('Sharing Type', choices=((1, 'Access'), (2, 'Deny'),))
    date_posted = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = ('Sharing File')
        verbose_name_plural = ('Sharing File')

    def __str__(self):
        return self.file.title






class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages',on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

