from django.contrib import admin

from .models.listing import Listing
from .models.listing_upload import ListingUpload


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "active", "country", "sector", "industry")
    list_filter = (
        "country",
        "sector",
        "industry",
        "active",
    )
    readonly_fields = ("original_ticker",)
    ordering = ("ticker",)
    search_fields = (
        "ticker",
        "name",
    )
    fieldsets = (
        (None, {"fields": ("name", "ticker", "active")}),
        (
            "About",
            {
                "classes": ("collapse",),
                "fields": (
                    "country",
                    "sector",
                    "industry",
                    "original_ticker",
                ),
            },
        ),
    )


@admin.register(ListingUpload)
class ListingUploadAdmin(admin.ModelAdmin):
    list_display = (
        "trimmed_friendly_file_name",
        "trimmed_description",
        "imported",
        "created_on",
    )
    search_fields = (
        "listing_file",
        "description",
    )
    readonly_fields = (
        "imported",
        "latest_task_id",
    )
    fields = (
        "listing_file",
        "description",
        "imported",
        "latest_task_id",
    )
