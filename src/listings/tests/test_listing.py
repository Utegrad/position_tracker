import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

from listings.models.listing import Listing
from listings.forms import ListingForm


@pytest.mark.django_db
class TestBasicListingModelsAndViews:
    """Test for some basic listing view operations."""

    def test_create_listing_view(self, client):
        """Create a listing through the view."""
        listing_data = {
            "name": "Foo",
            "ticker": "FOO",
        }
        response = client.post(reverse("listings:create"), data=listing_data)
        assert response.status_code == 302
        listing = Listing.objects.get(ticker="FOO")
        assert listing.name == "Foo"

    def test_update_listing_view(self, client):
        _ = Listing.objects.create(name="Foo", ticker="FOO")
        new_name = "Foo & Sons"
        response = client.post(
            reverse("listings:update", kwargs={"ticker": "FOO"}),
            data={
                "name": new_name,
                "ticker": "FOO",
            },  # All required form fields must be sent.
        )
        assert response.status_code == 302
        listing = Listing.objects.get(ticker="FOO")
        assert listing.name == new_name

    def test_delete_listing_view(self, client):
        _ = Listing.objects.create(name="Foo", ticker="FOO")
        response = client.post(
            reverse("listings:delete", kwargs={"ticker": "FOO"}),
        )
        assert response.status_code == 302
        assert Listing.objects.filter(ticker="FOO").exists() is False

    def test_listing_name_in_view_content(self, client):
        """Given a listing in the database, the URL for that database should return content that includes the name of
        the listing."""
        listing = Listing.objects.create(name="Foo", ticker="FOO")
        url = reverse("listings:detail", kwargs={"ticker": listing.ticker})
        response = client.get(url)
        assertContains(response, listing, status_code=200)

    def test_listings_names_in_listing_list_view(self, client):
        """Given multiple listings, check that their names are in the list view."""
        listing1 = Listing.objects.create(name="Foo", ticker="FOO")
        listing2 = Listing.objects.create(name="Bar", ticker="BAR")
        url = reverse("listings:listings")
        response = client.get(url)
        assertContains(response, listing1, status_code=200)
        assertContains(response, listing2, status_code=200)

    @pytest.mark.parametrize(
        ("ticker",),
        [
            ("FOO",),
            ("FOO^A",),
            ("FOO/A",),
        ],
    )
    def test_special_chars_in_ticker_matches_reverse(self, ticker, client):
        """Test that the different contents expected for tickers can be used as a URL."""
        form = ListingForm(data={"ticker": ticker, "name": "Foo"})
        form.is_valid()
        listing = form.save()
        url = reverse("listings:detail", kwargs={"ticker": listing.ticker})
        response = client.get(url)
        assertContains(response, listing, status_code=200)
