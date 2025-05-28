import os
import tempfile
import zipfile
from typing import Optional

from django.conf import settings
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse

from core.constants import CLIENT_CONF
from core.utils import generate_wg_keys
from core.wg_manager import Wireguard
from wireguard.models import WgClient


@admin.register(WgClient)
class WgClientAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "address")
    list_display_links = ("comment",)
    search_fields = ("id", "comment", "address")
    ordering = ("id", "comment", "address")
    fields = ("comment",)
    actions = ["download_configs", "delete_clients"]

    def save_model(self, request: HttpRequest, obj: WgClient, form: ModelForm, change: bool) -> None:
        private_key, public_key = generate_wg_keys()

        obj.private_key = private_key
        obj.public_key = public_key
        obj.set_address()
        super().save_model(request, obj, form, change)
        self._reload_wg()

    def download_configs(self, request: HttpRequest, queryset: QuerySet) -> Optional[HttpResponse]:
        if queryset.count() == 0:
            self.message_user(request, "Select one or more clients.", level="error")
            return

        client: WgClient
        wg = Wireguard()

        if queryset.count() == 1:
            client = queryset.first()
            config_content = CLIENT_CONF.format(
                client.private_key, client.address,
                wg.public_key, settings.SERVER_IP, settings.WG_PORT)

            response = HttpResponse(config_content, content_type="text/plain")
            response["Content-Disposition"] = f'attachment; filename="{client.comment.replace(" ", "_")}.conf"'
            return response

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            zip_filename = temp_zip.name
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for client in queryset:
                    config_content = CLIENT_CONF.format(
                        client.private_key, client.address,
                        wg.public_key, settings.SERVER_IP, settings.WG_PORT)

                    config_filename = f"{client.comment.replace(' ', '_')}.conf"
                    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
                        temp_file.write(config_content)
                        temp_file.flush()
                        temp_file.close()
                        zip_file.write(temp_file.name, config_filename)  # Add to ZIP
                        os.unlink(temp_file.name)  # Delete temp file

        with open(zip_filename, "rb") as zip_file:
            response = HttpResponse(zip_file.read(), content_type="application/zip")
            response["Content-Disposition"] = 'attachment; filename="wg_configs.zip"'
            os.unlink(zip_filename)
            return response

    def delete_clients(self, request, queryset: QuerySet):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} records", level=messages.SUCCESS)
        self._reload_wg()

    download_configs.short_description = "Download config(s)"
    delete_clients.short_description = "Delete client(s)"

    @staticmethod
    def _reload_wg() -> None:
        wg = Wireguard()
        wg.write_config()
        wg.reload()
