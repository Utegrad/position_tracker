from django.contrib import admin

from .models.listing_upload import ListingUpload
from .models.listing import Listing


@admin.register(ListingUpload)
class ListingsUploadAdmin(admin.ModelAdmin):
    list_display = (
        "trimmed_friendly_file_name",
        "trimmed_description",
        "imported",
    )
    search_fields = (
        "listings_file",
        "description",
    )
    readonly_fields = (
        "latest_task_status",
        "imported",
        "latest_task_id",
    )
    fields = (
        "listings_file",
        "description",
        "imported",
        "latest_task_id",
        "latest_task_status",
    )


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