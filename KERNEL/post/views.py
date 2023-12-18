from django.shortcuts import render
from .models import PostTable
from django.shortcuts import redirect
from .forms import PostForm

def post_list(request):
    posts = PostTable.objects.all()
    return render(request, 'post/post_list.html', {'posts': posts})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post/add_post.html', {'form': form})