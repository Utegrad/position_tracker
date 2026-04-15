import pytest

from listings.models.listing_upload import ListingUpload


class TestListingUploadModel:
    """Tests for ListingUpload that do not require database access."""

    def test_trimmed_friendly_file_name_returns_full_value_when_short(self):
        listing_upload = ListingUpload(description="short filename.csv")

        assert listing_upload.trimmed_friendly_file_name == "short filename.csv"

    def test_trimmed_friendly_file_name_truncates_long_value(self):
        listing_upload = ListingUpload(description="a" * 30)

        assert listing_upload.trimmed_friendly_file_name == f"{'a' * 24}..."

    def test_trimmed_description_returns_full_value_when_short(self):
        listing_upload = ListingUpload(description="short description")

        assert listing_upload.trimmed_description == "short description"

    def test_trimmed_description_truncates_long_value(self):
        listing_upload = ListingUpload(description="b" * 30)

        assert listing_upload.trimmed_description == f"{'b' * 24}..."

    def test_get_absolute_url_uses_uuid(self, monkeypatch):
        listing_upload = ListingUpload(uuid="12345678-1234-5678-1234-567812345678")

        captured = {}

        def fake_reverse(viewname, args=None, kwargs=None):
            captured["viewname"] = viewname
            captured["args"] = args
            captured["kwargs"] = kwargs
            return "/fake-url/"

        monkeypatch.setattr("listings.models.listing_upload.reverse", fake_reverse)

        assert listing_upload.get_absolute_url() == "/fake-url/"
        assert captured["viewname"] == "listings:listings_upload_detail"
        assert captured["args"] == ["12345678-1234-5678-1234-567812345678"]
        assert captured["kwargs"] is None

    def test_str_returns_empty_string(self):
        listing_upload = ListingUpload(description="anything")

        assert str(listing_upload) == ""

    def test_imported_defaults_to_false(self):
        listing_upload = ListingUpload(description="anything")

        assert listing_upload.imported is False


@pytest.mark.django_db
class TestListingUploadDatabaseBehavior:
    """Tests for ListingUpload behavior that should be verified against the database."""

    def test_can_create_listing_upload(self):
        listing_upload = ListingUpload.objects.create(
            uuid="12345678-1234-5678-1234-567812345678",
            description="NASDAQ listings export.csv",
        )

        fetched = ListingUpload.objects.get(uuid=listing_upload.uuid)

        assert fetched.description == "NASDAQ listings export.csv"
        assert fetched.imported is False