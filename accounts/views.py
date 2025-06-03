from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/dashboard/')  # şimdilik sabit
        else:
            print("Giriş başarısız")

    return render(request, 'accounts/login.html', {'form': form})




def index_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        return redirect('login')  # name='login' olan URL'e gider
