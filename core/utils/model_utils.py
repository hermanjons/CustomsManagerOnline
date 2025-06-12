from django.db import models
import math
from core.constants import SYSTEM_FIELDS


def extract_field_meta(model_class):
    meta = {
        'field_names': [],
        'foreign_keys': {},
        'self_relation_fields': [],
        'required_fields': [],
        'm2m_fields': [field.name for field in model_class._meta.many_to_many],
    }

    for field in model_class._meta.fields:

        if field.name in SYSTEM_FIELDS:
            print("otomatik alan tespit edildi",field)
            continue  # Otomatik alanları atla ❗
        meta['field_names'].append(field.name)

        if isinstance(field, models.ForeignKey):
            meta['foreign_keys'][field.name] = field.remote_field.model
            if field.remote_field.model == model_class:
                meta['self_relation_fields'].append(field.name)

        if not field.null and not field.blank and not isinstance(field, models.AutoField):
            meta['required_fields'].append(field.name)
    print(meta)
    return meta


def create_objects(df, model_class, meta, total, on_progress=None):
    created_count = 0
    failed_rows = []
    temp_id_map = {}

    for index, row in df.iterrows():
        try:
            record_id = int(row.get("id"))
            obj_data = {}

            for field in meta['field_names']:
                val = row.get(field)

                # Eksik veya boş veri kontrolü
                if val in [None, '', ' '] or (isinstance(val, float) and math.isnan(val)):
                    if field in meta['required_fields']:
                        raise ValueError(f"Zorunlu alan eksik: {field}")
                    obj_data[field] = None
                    continue

                # SELF-RELATION alanlar için ilk aşamada boş geç
                if field in meta['self_relation_fields']:
                    obj_data[field] = None
                    continue

                # ForeignKey alanları için instance çek
                if field in meta['foreign_keys']:
                    fk_model = meta['foreign_keys'][field]
                    try:
                        # Float veya string gibi gelen id'leri düzgün parse et
                        if isinstance(val, float) and val.is_integer():
                            val = int(val)
                        elif isinstance(val, str) and val.replace('.', '', 1).isdigit():
                            val = int(float(val))
                        obj_data[field] = fk_model.objects.get(id=val)
                    except (fk_model.DoesNotExist, ValueError, TypeError):
                        raise ValueError(f"{field} alanı için FK bulunamadı: {val}")
                else:
                    obj_data[field] = val

            # Nesneyi oluştur
            obj = model_class.objects.create(**obj_data)
            temp_id_map[record_id] = obj

            # M2M alanlar
            for m2m_field in meta['m2m_fields']:
                if m2m_field in df.columns:
                    value = row.get(m2m_field)
                    if value not in [None, '', ' '] and not (isinstance(value, float) and math.isnan(value)):
                        ids = [int(float(v.strip())) for v in str(value).split(',') if v.strip().replace('.', '', 1).isdigit()]
                        model_field = model_class._meta.get_field(m2m_field)
                        related_model = model_field.related_model
                        m2m_objs = related_model.objects.filter(id__in=ids)
                        getattr(obj, m2m_field).set(m2m_objs)

            created_count += 1

        except Exception as e:
            failed_rows.append({'satir': index + 2, 'hata': str(e)})

        if on_progress:
            on_progress(index + 1, total)

    return created_count, failed_rows, temp_id_map



def update_self_relations(df, model_class, meta, temp_id_map, total, on_progress=None):
    for index, row in df.iterrows():
        try:
            record_id = int(row.get("id"))
            obj = temp_id_map.get(record_id)
            if not obj:
                continue

            for field in meta['self_relation_fields']:
                relation_id = row.get(field)
                if relation_id is not None:
                    related_instance = temp_id_map.get(int(relation_id))
                    if related_instance:
                        setattr(obj, field, related_instance)

            obj.save()

        except Exception:
            continue
        print(65 + (index + 1 / total) * 100)
        # her adımda dışarıya ilerleme bildir
        if on_progress:
            on_progress(index + 1, total)
