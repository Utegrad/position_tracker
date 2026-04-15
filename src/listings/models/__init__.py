from django.db import models


class TimeStampedObjectModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


from .listing import Listing
from .listing_upload import ListingUpload
