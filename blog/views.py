from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .models import *

def logout_view(request):
    logout(request)
    return redirect('blog:post_list')  
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form}) 



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories})

def Cat_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all()
    return render(request, 'blog/Cat_list.html', {'categories':categories})

def Tag_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    tags = Tag.objects.all()
    return render(request, 'blog/Tag_list.html', {'tags':tags})

def post_detail(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    reply_form = ReplyForm()  # Create an instance of ReplyForm

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('blog:post_detail', post_slug=post_slug)

        reply_form = ReplyForm(request.POST)  

        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.comment = Comment.objects.get(pk=request.POST.get('comment_id'))
            new_reply.save()
            return redirect('blog:post_detail', post_slug=post_slug)

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'reply_form': reply_form})

    
def reply_to_comment(request, comment_id,post_slug):
    comment = get_object_or_404(Comment, id=comment_id)
    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.comment = comment
            new_reply.save()
            return redirect('blog:post_detail',post_slug=post_slug)

    return render(request, 'blog/reply.html', {'comment': comment, 'reply_form': reply_form})

def Cat_Details(request, category_slug):
    categories = get_object_or_404(Category, title=category_slug)
    posts = Post.objects.filter(post_cat=categories)

    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories})


def Tag_Details(request, tag_slug):
    tags = get_object_or_404(Tag, name=tag_slug)
    posts = Post.objects.filter(tags=tags)

    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url='login')
def post_new(request):
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
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url='login')
def post_edit(request, post_slug):
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
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list') 
    else:
        form = CustomUserChangeForm(instance=request.user)
       
        

    return render(request, 'blog/edit_profile.html', {'form': form})

def user_detail(request, username):
    user = get_object_or_404(CustomUser, username=username)
    print(user.img_preview2,"user img")
    return render(request, 'blog/userdetails.html', {'user': user})