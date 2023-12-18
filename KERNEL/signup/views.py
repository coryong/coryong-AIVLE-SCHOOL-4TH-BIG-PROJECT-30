from django.shortcuts import render, redirect
from .forms import UserTableForm
from django.db import models
    
def signup_view(request):
    if request.method == 'POST':
        form = UserTableForm(request.POST)
        if form.is_valid():
            # 여기에서 유효한 데이터 처리 (예: 데이터베이스에 저장)
            form.save()
            return redirect('home')  # 가입 후 이동할 페이지
    else:
        form = UserTableForm()

    return render(request, 'signup/signup.html', {'form': form})