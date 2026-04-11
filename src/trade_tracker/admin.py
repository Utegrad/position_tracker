from django.contrib import admin

from .models.listing import Listing


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
