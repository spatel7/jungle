import os
from django.utils import timezone

def populate():
  u1 = add_user('sahilpatel', '123')
  u2 = add_user('kevinlin', '123')
  u3 = add_user('aakashjapi', '123')
  u4 = add_user('jontau', '123')

  j1 = add_jungle('The Main Homies', u1)
  j2 = add_jungle('Subset', u1)

  add_user_to_jungle(j1, u2)
  add_user_to_jungle(j1, u3)
  add_user_to_jungle(j1, u4)

  p1 = add_post(j1, u1, u2, 'I like eating peanuts.')
  p2 = add_post(j1, u1, u3, 'I like jumping over cars')
  p3 = add_post(j1, u2, u1, 'Monkeys are my best friends')

  for jungle in Jungle.objects.all():
    for post in Post.objects.filter(jungle=jungle):
      print "- {0} - {1}".format(str(jungle), str(post))

def add_user(username, password):
  u = User.objects.get_or_create(username=username)[0]
  u.set_password(password)
  u.save()
  return u

def add_jungle(name, user):
  j = Jungle.objects.get_or_create(name=name, date=timezone.now())[0]
  j.users.add(user)
  j.save()
  return j

def add_user_to_jungle(jungle, user):
  jungle.users.add(user)
  jungle.save()

def add_post(jungle, original, displayed, content):
  p = Post.objects.get_or_create(jungle=jungle, original=original, displayed=displayed, content=content, date=timezone.now())[0]
  return p

if __name__ == '__main__':
  print 'Starting Jungle population'
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle.settings')
  from jungleapp.models import Jungle, Post
  from django.contrib.auth.models import User
  populate()