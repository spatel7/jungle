from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from jungleapp.forms import UserForm, JungleForm, PostForm
from jungleapp.models import Jungle, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def index(request):
  if request.user.is_authenticated():
    return redirect('/home')
  context = RequestContext(request)
  return render_to_response('jungleapp/index.jade', {}, context)

def register(request):
  if request.user.is_authenticated():
    return redirect('/home')
  context = RequestContext(request)
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    if user_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()
      return HttpResponseRedirect('/login/')
    else:
      print user_form.errors
  else:
    user_form = UserForm()
  return render_to_response('jungleapp/register.jade', {'user_form': user_form}, context)

def user_login(request):
  if request.user.is_authenticated():
    return redirect('/home')
  context = RequestContext(request)
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/home')
      else:
        return HttpResponse('Your account has been disabled')
    else:
      return HttpResponse('Invalid login information supplied')
  return render_to_response('jungleapp/login.jade', {}, context)

@login_required
def home(request):
  context = RequestContext(request)
  u = User.objects.get(username=request.user)
  js = Jungle.objects.filter(users__in=[u])
  context_dict = {'user': u, 'jungles': js}
  return render_to_response('jungleapp/home.jade', context_dict, context)

@login_required
def jungle(request, jungle_id_url):
  context = RequestContext(request)
  jungle_id = jungle_id_url
  context_dict = {'jungle_id': jungle_id}
  try:
    jungle = Jungle.objects.get(id=jungle_id)
    posts = Post.objects.filter(jungle=jungle)
    context_dict['jungle'] = jungle
    context_dict['posts'] = posts
  except Jungle.DoesNotExist:
    pass
  return render_to_response('jungleapp/jungle.jade', context_dict, context)

@login_required
def add_jungle(request):
  context = RequestContext(request)
  if request.method == 'POST':
    jungle_form = JungleForm(request.POST)
    if jungle_form.is_valid():
      jungle = jungle_form.save(commit=False)
      jungle.date = timezone.now()
      jungle.save()
      jungle.users.add(User.objects.get(username=request.user))
      jungle.save()
      return HttpResponseRedirect('/jungles/'+str(jungle.id))
    else:
      print jungle_form.errors
  else:
    jungle_form = JungleForm
  return render_to_response('jungleapp/add_jungle.jade', {'jungle_form': jungle_form}, context)

@login_required
def add_user(request, jungle_id_url):
  context = RequestContext(request)
  jungle_id = jungle_id_url
  context_dict = {'id': jungle_id}
  try:
    jungle = Jungle.objects.get(id=jungle_id)
    context_dict['jungle'] = jungle
    if request.method == 'POST':
      username = request.POST['username']
      u = User.objects.get(username=username)
      if u is not None and u not in jungle.users.all():
        jungle.users.add(u)
        jungle.save()
      return HttpResponseRedirect('/jungles/'+str(jungle.id))
  except Jungle.DoesNotExist:
    return HttpResponse("That jungle does not exist!")
  except User.DoesNotExist:
    return HttpResponse("That user does not exist!")
  return render_to_response('jungleapp/add_user.jade', context_dict, context)

@login_required
def write_post(request, jungle_id_url):
  context = RequestContext(request)
  jungle_id = jungle_id_url
  context_dict = {'id': jungle_id}
  try:
    jungle = Jungle.objects.get(id=jungle_id)
    context_dict['jungle'] = jungle
    full_users = jungle.users.all()
    context_dict['users'] = full_users.exclude(username=request.user)
    if request.method == 'POST':
      post_form = PostForm(data=request.POST)
      if post_form.is_valid():
        displayed = request.POST['displayed']
        content = request.POST['new_post']
        if not content:
          return HttpResponse("You can't post nothing.")
        post = post_form.save(commit=False)
        post.jungle = jungle
        post.content = content
        post.original = User.objects.get(username=request.user)
        post.displayed = User.objects.get(username=displayed)
        if post.original not in full_users or post.displayed not in context_dict['users']:
          return HttpResponse('Dont try to add a user you know isnt valid hahaha')
        post.date = timezone.now()
        post.save()
        return HttpResponseRedirect('/jungles/'+str(jungle_id))
      else:
        print post_form.errors
    else:
      context_dict['post_form'] = PostForm()
  except Jungle.DoesNotExist:
    return HttpResponse("That jungle does not exist!")
  except User.DoesNotExist:
    return HttpResponse("That user does not exist!")
  return render_to_response('jungleapp/write_post.jade', context_dict, context)

@login_required
def leave_jungle(request, jungle_id_url):
  context = RequestContext(request)
  jungle_id = jungle_id_url
  try:
    jungle = Jungle.objects.get(id=jungle_id)
    jungle.users.remove(User.objects.get(username=request.user))
    # delete jungle if last user
    jungle.save()
  except Jungle.DoesNotExist:
    pass
  return HttpResponseRedirect('/home/')

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/index')