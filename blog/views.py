from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

import pandas as pd

from .forms import *
from .models import *

def logout_view(request):
    logout(request)
    send_push_notification(title="Logout", body="User Logout", data={"key": "value"})
    return redirect(reverse('blog:post_list')+'?logout=true')  
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            send_push_notification(title="login", body="User login",data={"key": "value"})
            return redirect('blog:post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# View for register/SignIn new user
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_push_notification(title="Resigster", body="Proceed to Login",data={"key": "value"})
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form}) 

def post_list(request):
    posts = Post.objects.order_by('-published_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories})

# View for Category list
def cat_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/cat_list.html', {'categories':categories})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags':tags})

def post_detail(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return  redirect('blog:post_detail', post_slug=post_slug)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html',{'post':post,'comments': comments,'comment_form':comment_form})

# view to reply over a comment
def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id') 
            parent_id = request.POST.get('parent')  
            post_url = request.POST.get('post_url')  
            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            send_push_notification(title="Replied", body="User Replied", data={"key": "value"})
            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")

def cat_details(request, category_slug):
    categories = get_object_or_404(Category, title=category_slug)
    posts = Post.objects.filter(post_cat=categories)
    category_slug = "Category for: "+category_slug
    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories,"query":category_slug})

def tag_details(request, tag_slug):
    tags = get_object_or_404(Tag, name=tag_slug)
    posts = Post.objects.filter(tags=tags)
    tag_slug = "Tag for: "+tag_slug
    return render(request, 'blog/post_list.html', {'posts': posts,"query":tag_slug})

@login_required(login_url='blog:login')
def post_new(request):
    heading = "New Post"
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', post_slug=post.post_slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form,'heading':heading})

def bulk_post_upload(request):
    if request.method == 'POST':
        form = BulkPostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            
            for _, row in df.iterrows():
                tag_names = [tag.strip() for tag in row['tags'].split(',')]
                tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tag_names]
                category_name = row['category']
                category, created = Category.objects.get_or_create(title=category_name)
                post = Post.objects.create(
                    title=row['title'],
                    text=row['text'],
                    author=request.user,
                    published_date=row['published_date'],
                    image=row['image'],
                    feature_img= row['feature_img'],
                    post_cat=category
                )
                post.tags.add(*tags)

            return redirect('blog:post_list')  
    else:
        form = BulkPostUploadForm()

    return render(request, 'blog/bulk_post_upload.html', {'form': form})

@login_required(login_url='blog:login')
def post_edit(request, post_slug):
    heading = "Edit post"
    post = get_object_or_404(Post, post_slug=post_slug)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', post_slug=post.post_slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'heading':heading})

@login_required(login_url='blog:login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:user_detail'  ,username=user.username) 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})

def user_detail(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'blog/userdetails.html', {'user': user})