from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from core.constants import MODEL_ICONS
from core.utils.cache_utils import clear_user_cache_keys, set_user_cache_key_if_changed
from core.utils.file_utils import read_excel_file
from core.utils.model_utils import extract_field_meta, create_objects, update_self_relations
from django.db.models import Q
from django.core.paginator import Paginator
import io
from django.core.files.base import ContentFile
from django.apps import apps
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps
from django.http import JsonResponse
from django.core.cache import cache
import pandas as pd


@staff_member_required
@require_POST
def upload_excel(request, model):
    try:
        model_class = apps.get_model("customs_general", model)
        user_id = getattr(request.user, "id", None)


        if "excel_file" not in request.FILES:
            return JsonResponse({"success": False, "error": "Excel dosyası eksik!"})

        df = read_excel_file(request.FILES["excel_file"])
        total = len(df)
        field_meta = extract_field_meta(model_class)

        created_count, failed_rows, temp_id_map = create_objects(
            df, model_class, field_meta, total,
            on_progress=lambda current, total_data: set_user_cache_key_if_changed(user_id, "upload_progress", int((current / total_data) * 65))
        )

        if temp_id_map:
            update_self_relations(
                df, model_class, field_meta, temp_id_map, total,
                on_progress=lambda current, total: set_user_cache_key_if_changed(
                    user_id, "upload_progress", 65 + int((current / total) * 35), timeout=20
                )
            )
            # her halükarda %100 garantile
            set_user_cache_key_if_changed(user_id, "upload_progress", 100, timeout=20)
        else:
            set_user_cache_key_if_changed(user_id, "upload_progress", 100, timeout=20)
        clear_user_cache_keys(user_id, "upload_progess", "failed_rows")
        set_user_cache_key_if_changed(user_id, "failed_rows", failed_rows)
        return JsonResponse({
            "success": True,
            "message": f"{created_count} kayıt başarıyla eklendi!",
            "failed_rows_count": len(failed_rows),
            "failed_rows_download_url": f"/customs_general/download-failed-rows/{model}/"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@staff_member_required
def upload_progress(request):
    user_id = getattr(request.user, "id", None)
    if not user_id:
        return JsonResponse({"progress": 0, "debug": "user not logged in"})
    progress = cache.get(f"upload_progress:{user_id}", 0)

    return JsonResponse({"progress": progress})


@staff_member_required
def download_failed_rows(request, model):
    cache_key = f"failed_rows:{request.user.id}"
    failed_rows = cache.get(cache_key)

    if not failed_rows:
        return HttpResponse("İndirilecek hata bulunamadı.", content_type="text/plain")

    df = pd.DataFrame(failed_rows)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={model}_hatalar.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    cache.delete(cache_key)  # İndirildikten sonra temizle (isteğe bağlı)

    return response
