import logging
import urllib.parse

from django.forms import ModelForm

from .models.listing import Listing


logger = logging.getLogger(__name__)


class ListingForm(ModelForm):
    """Form to validate and create a Listing object.  Use in HTML and for processing data imports."""

    class Meta:
        model = Listing
        fields = (
            "name",
            "ticker",
            "country",
            "sector",
            "industry",
        )

    def clean_ticker(self):
        _ticker = self.cleaned_data["ticker"]
        encoded_ticker = urllib.parse.quote(_ticker, safe="")
        return encoded_ticker