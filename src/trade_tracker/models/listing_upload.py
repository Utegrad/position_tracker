import uuid

from django.db import models
from django.urls import reverse
from django_celery_results.models import TaskResult

from . import TimeStampedObjectModel


class ListingUpload(TimeStampedObjectModel):
    """A model for an uploaded file with listing data.
    Designed around downloading a CSV file from: https://www.nasdaq.com/market-activity/stocks/screener to populate the
    Listings table.
    """

    listings_file = models.FileField(upload_to="uploads")
    description = models.CharField(max_length=255, blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imported = models.BooleanField(
        default=False,
        help_text="Marked True when the task has processed this file to import listings data.",
    )
    latest_task_id = models.CharField(
        blank=True,
        max_length=255,
        help_text="This field can hold the task_id when using an async task to process the listings_file.",
    )

    @property
    def latest_task_status(self):
        try:
            task_result = TaskResult.objects.get(task_id=self.latest_task_id)
            date_done = task_result.date_done.isoformat()
            latest_task_status_str = (
                f"{self.latest_task_id}: {task_result.status} at {date_done}"
            )
        except TaskResult.DoesNotExist:
            latest_task_status_str = "None"
        return latest_task_status_str

    @property
    def trimmed_description(self):
        desc_display_length = 24
        trailer = "..." if len(self.description) > desc_display_length else ""
        return f"{self.description[:desc_display_length]}{trailer}"

    @property
    def trimmed_friendly_file_name(self):
        max_friendly_file_name_length = 24
        trailer = (
            "..." if len(self.listings_file) > max_friendly_file_name_length else ""
        )
        return f"{self.listings_file.name[:max_friendly_file_name_length]}{trailer}"

    def get_absolute_url(self):
        return reverse("listings:listings_upload_detail", args=[self.pk])

    def __str__(self):
        return f"{self.trimmed_friendly_file_name} ({self.trimmed_description}"

    class Meta:
        get_latest_by = "created_on"