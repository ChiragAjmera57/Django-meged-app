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

# View for register/SignIn new user
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

# View for Category list
def Cat_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/Cat_list.html', {'categories':categories})

def Tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/Tag_list.html', {'tags':tags})

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
            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")

def Cat_Details(request, category_slug):
    categories = get_object_or_404(Category, title=category_slug)
    posts = Post.objects.filter(post_cat=categories)

    return render(request, 'blog/post_list.html', {'posts': posts,'categorie':categories,"query":category_slug})

def Tag_Details(request, tag_slug):
    tags = get_object_or_404(Tag, name=tag_slug)
    posts = Post.objects.filter(tags=tags)

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
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES, instance=request.user)
        
        print(form,"form .....")
        print(form.is_valid(),"from is valid....")
        if form.is_valid():
            form.save()
            return redirect('blog:post_list') 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})


def user_detail(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'blog/userdetails.html', {'user': user})