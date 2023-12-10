from django.apps import AppConfig
from django.db.models.signals import post_save


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self) -> None:
        from main.signals import update_historicaldata

        sender = self.get_model("PurchaseOrderModel")
        post_save.connect(receiver=update_historicaldata, sender=sender)
