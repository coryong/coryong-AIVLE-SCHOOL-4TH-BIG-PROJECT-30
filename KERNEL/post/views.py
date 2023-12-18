from django.shortcuts import render
from .models import PostTable
from django.shortcuts import redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm

def post_list(request):
    posts = PostTable.objects.all()
    return render(request, 'post/post_list.html', {'posts': posts})

# @login_required
# def add_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)  # Save the form but don't commit to the database yet
#             post.user = request.user  # Set the user of the post to the currently logged-in user
#             post.save()  # Now save the post to the database
#             return redirect('post_list')
#     else:
#         form = PostForm()

#     return render(request, 'post/add_post.html', {'form': form})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Save the form but don't commit to the database yet
            if request.user.is_authenticated:
                post.user = request.user  # Set the user of the post to the currently logged-in user
            # else: Optionally, you can handle the case for anonymous users here
            post.save()  # Now save the post to the database
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'post/add_post.html', {'form': form})