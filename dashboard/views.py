
from django.shortcuts import render, get_list_or_404
from django.apps import apps


def dashboard_home(request):
    return render(request, 'dashboard/index.html')
