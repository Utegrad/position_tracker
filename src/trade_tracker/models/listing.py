import urllib.parse
from django.db import models
from django.urls import reverse
from pydantic import BaseModel, Field
from . import TimeStampedObjectModel


class ListingData(BaseModel):
    """This class simplifies creating Listing objects using data from outside sources where the field name doesn't
    match the model's field names.  The class is representative of data from
    https://www.nasdaq.com/market-activity/stocks/screener
    TODO: Move to a 'schemas' package
    """

    name: str = Field(..., alias="Name")
    ticker: str = Field(..., alias="Symbol")
    country: str = Field(None, alias="Country")
    sector: str = Field(None, alias="Sector")
    industry: str = Field(None, alias="Industry")


class ListingManager(models.Manager):
    def from_listing_data(self, data: ListingData):
        listing = self.create(**data)
        return listing


class Listing(TimeStampedObjectModel):
    """Model to represent a market listing.
    Structured to match download from: https://www.nasdaq.com/market-activity/stocks/screener
    """

    name = models.CharField(
        max_length=255,
        blank=False,
    )
    ticker = models.CharField(
        max_length=32,
        blank=False,
        unique=True,
        db_index=True,
        help_text="The symbol for a listing.",
    )
    active = models.BooleanField(
        default=True,
        help_text="False indicates this listing is can no longer be traded.",
    )
    country = models.CharField(null=True, default="", blank=True, max_length=128)
    sector = models.CharField(null=True, default="", blank=True, max_length=128)
    industry = models.CharField(null=True, default="", blank=True, max_length=128)

    objects = ListingManager()

    @property
    def original_ticker(self):
        _original_ticker = urllib.parse.unquote(self.ticker)
        return _original_ticker

    def __str__(self):
        return "{0} [{1}]".format(self.ticker, self.name)

    def get_absolute_url(self):
        return reverse("listings:detail", args=[self.ticker])

    class Meta:
        unique_together = (("name", "ticker"),)
