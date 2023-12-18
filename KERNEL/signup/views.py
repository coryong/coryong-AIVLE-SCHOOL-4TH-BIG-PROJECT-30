from django.shortcuts import render, redirect
from .forms import UserTableForm
from django.db import models
    
def signup(request):
    if request.method == 'POST':
        form = UserTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # 'home'은 회원가입 성공 후 이동할 페이지의 URL 이름입니다.
    else:
        form = UserTableForm()
    return render(request, 'signup.html', {'form': form})