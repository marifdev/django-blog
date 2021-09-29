from datetime import datetime
from posts.models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def index(request):
  posts = Post.objects.all()
  return render(request, 'index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already used')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already used')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials are invalid')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        post_body = request.POST['post_body']
        post = Post.objects.create(title=title, body=post_body)
        post.save()
        return redirect('/')
    else:
        return render(request, 'create_post.html')


def post(request, post_id):
    post_object = Post.objects.get(id=post_id)
    post = {
        "title": post_object.title,
        "body": post_object.body
    }
    return render(request, 'post.html', {'post': post})