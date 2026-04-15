import uuid

from django.db import models
from django.urls import reverse

from . import TimeStampedObjectModel


class ListingUpload(TimeStampedObjectModel):
    """A model for an uploaded file with listing data.
    Designed around download a CSV file from [NASDAQ](https://www.nasdaq.com/market-activity/stocks/screener) to
    populate the listing table.
    """

    listing_file = models.FileField(upload_to="uploads/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imported = models.BooleanField(
        default=False,
        help_text="Marked True when the task has processed this file to import listings data.",
    )
    latest_task_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="This field can hold the task_id when using an async task to process the listings_file.",
    )

    @property
    def trimmed_friendly_file_name(self):
        max_friendly_file_name_length = 24
        trailer = "..." if len(self.description) > max_friendly_file_name_length else ""
        return f"{self.description[:max_friendly_file_name_length]}{trailer}"

    @property
    def trimmed_description(self):
        desc_display_length = 24
        trailer = "..." if len(self.description) > desc_display_length else ""
        return f"{self.description[:desc_display_length]}{trailer}"

    def get_absolute_url(self):
        return reverse("listings:listings_upload_detail", args=[str(self.uuid)])

    def __str__(self):
        return f""

    class Meta:
        get_latest_by = "created_on"
