from django.shortcuts import redirect
from blog.customUserCreate import CustomUserChangeForm, CustomUserCreationForm
from .forms import PostForm
from django.shortcuts import render
from django.utils import timezone
from .models import Category, Post, Tag
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

class LogoutInterface(LogoutView):
    template_name = 'blog/logout.html'
    
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form)
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})   


@login_required(login_url='login')
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories})

@login_required(login_url='login')
def Cat_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all()
    return render(request, 'blog/Cat_list.html', {'categories':categories})

@login_required(login_url='login')
def Tag_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    tags = Tag.objects.all()
    return render(request, 'blog/Tag_list.html', {'tags':tags})

@login_required(login_url='login')
def post_detail(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required(login_url='login')
def Cat_Details(request, category_slug):
    categories = get_object_or_404(Category, title=category_slug)
    posts = Post.objects.filter(post_cat=categories)

    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories})


@login_required(login_url='login')
def Tag_Details(request, tag_slug):
    tags = get_object_or_404(Tag, name=tag_slug)
    posts = Post.objects.filter(tags=tags)
    print(tags,posts)

    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url='login')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            print(form)
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', post_slug=post.post_slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url='login')
def post_edit(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            print(form)
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', post_slug=post.post_slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account/profile_update.html') 
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'account/edit_profile.html', {'form': form})