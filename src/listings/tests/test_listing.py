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

    def test_listing_str_returns_ticker_and_name(self):
        listing = Listing(name="Foo", ticker="FOO")
        assert str(listing) == "FOO [Foo]"

    def test_create_listing_view_rejects_missing_required_fields(self, client):
        response = client.post(reverse("listings:create"), data={"ticker": "FOO"})
        assert response.status_code == 200
        assert Listing.objects.filter(ticker="FOO").exists() is False

    def test_create_listing_view_rejects_duplicate_ticker(self, client):
        Listing.objects.create(name="Foo", ticker="FOO")

        response = client.post(
            reverse("listings:create"),
            data={"name": "Another Foo", "ticker": "FOO"},
        )

        assert response.status_code == 200
        assert Listing.objects.filter(ticker="FOO").count() == 1

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

    def test_listing_list_view_shows_empty_page_when_no_listings(self, client):
        response = client.get(reverse("listings:listings"))
        assert response.status_code == 200

    def test_listing_detail_view_returns_404_for_missing_listing(self, client):
        response = client.get(reverse("listings:detail", kwargs={"ticker": "MISSING"}))
        assert response.status_code == 404

    def test_listing_update_view_returns_404_for_missing_listing(self, client):
        response = client.get(reverse("listings:update", kwargs={"ticker": "MISSING"}))
        assert response.status_code == 404

    def test_listing_delete_view_returns_404_for_missing_listing(self, client):
        response = client.post(reverse("listings:delete", kwargs={"ticker": "MISSING"}))
        assert response.status_code == 404

    def test_listing_list_view_includes_detail_update_delete_links(self, client):
        listing = Listing.objects.create(name="Foo", ticker="FOO")
        response = client.get(reverse("listings:listings"))

        assertContains(
            response, reverse("listings:detail", kwargs={"ticker": listing.ticker})
        )
        assertContains(
            response, reverse("listings:update", kwargs={"ticker": listing.ticker})
        )
        assertContains(
            response, reverse("listings:delete", kwargs={"ticker": listing.ticker})
        )

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

    def test_listing_get_absolute_url_uses_ticker(self):
        listing = Listing(name="Foo", ticker="FOO")
        assert listing.get_absolute_url() == reverse("listings:detail", args=["FOO"])

    def test_listing_original_ticker_decodes_encoded_value(self):
        listing = Listing(name="Foo", ticker="FOO%2FA")
        assert listing.original_ticker == "FOO/A"
