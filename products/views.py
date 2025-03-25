from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Brand, ProductModel
from .forms import BrandForm
from django.urls import reverse_lazy
from django.views.generic import CreateView




def brand_page_view(request):
    # Arama ve sayfalama parametrelerini al
    query = request.GET.get('q', '')
    per_page = request.GET.get('per_page', '10')
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    # Markalar için sorgu: arama varsa filtrele, yoksa tüm markaları al
    brands_queryset = Brand.objects.all()
    if query:
        brands_queryset = brands_queryset.filter(brand_name__icontains=query)

    # Sayfalama işlemi: Paginator ile belirlenen sayıda marka göster
    paginator = Paginator(brands_queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,  # Arama terimi
        'per_page': per_page,  # Sayfa başına gösterilecek kayıt sayısı
        'page_obj': page_obj,  # Sayfalama nesnesi (markalar için)
        'brands': page_obj.object_list,  # Sayfadaki marka kayıtları
    }
    return render(request, 'products/brand_page.html', context)


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_create.html'
    success_url = reverse_lazy('brand_page_view')

