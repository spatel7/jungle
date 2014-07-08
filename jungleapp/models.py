from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)

class Jungle(models.Model):
  name = models.CharField(max_length=200)
  date = models.DateTimeField('date_created')
  users = models.ManyToManyField(User)

  def __unicode__(self):
    return self.name

  def get_posts(self):
    return self.post_set.all()

class Post(models.Model):
  jungle = models.ForeignKey(Jungle)
  original = models.ForeignKey(User, related_name='original_post_author')
  displayed = models.ForeignKey(User, related_name='displayed_post_author')
  content = models.CharField(max_length=200)
  date = models.DateTimeField('date_created')

  def __unicode__(self):
    return str(self.displayed.username) + ' (' + str(self.original.username) + ') says: ' + self.content