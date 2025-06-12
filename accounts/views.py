from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import ClientProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


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


@login_required
def select_active_client(request, client_id):
    user = request.user

    # Sadece müşavirler bu işlemi yapabilir
    if user.role != "consultant":
        return HttpResponseForbidden("Bu işlem sadece müşavirler içindir.")

    # Sadece kendisine atanmış client'ı seçebilsin
    client = get_object_or_404(ClientProfile, id=client_id, consultants=user)
    request.session["active_client_id"] = client.id

    # İsteğe bağlı: dashboard'a yönlendir
    return redirect("dashboard_home")



@login_required
def select_active_consultant(request, consultant_id):
    user = request.user

    # Sadece müşteriler bu işlemi yapabilir
    if user.role != "client":
        return HttpResponseForbidden("Bu işlem sadece müşteriler içindir.")

    # Kullanıcının bağlı olduğu müşavirler arasından seçim yapılabilir
    client_profile = getattr(user, "client_profile", None)
    if not client_profile:
        return HttpResponseForbidden("Profil bulunamadı.")

    consultant = get_object_or_404(client_profile.consultants, id=consultant_id)

    # Seçilen müşaviri session'a kaydet
    request.session["active_consultant_id"] = consultant.id

    # Örneğin dashboard'a yönlendirebilirsin
    return redirect("dashboard_home")
