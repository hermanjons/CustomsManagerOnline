from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = "Verilen modelin tüm kayıtlarını siler ve ID sırasını 1'e sıfırlar."

    def add_arguments(self, parser):
        parser.add_argument("app_label", type=str, help="Uygulama adı (ör: customs_general)")
        parser.add_argument("model_name", type=str, help="Model adı (ör: Country)")

    def handle(self, *args, **options):
        app_label = options["app_label"]
        model_name = options["model_name"]

        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f"{app_label}.{model_name} modeli bulunamadı.")

        # Tablonun tam adı
        table_name = model._meta.db_table
        sequence_name = f"{table_name}_id_seq"

        # Kayıtları sil
        deleted, _ = model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"✔️ {deleted} kayıt silindi: {app_label}.{model_name}"))

        # Sequence sıfırla
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")
                self.stdout.write(self.style.SUCCESS(f"🔁 ID sırası sıfırlandı: {sequence_name}"))
            except Exception as e:
                raise CommandError(f"🚫 Sequence sıfırlanamadı: {e}")
