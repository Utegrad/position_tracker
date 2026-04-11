from django.urls import path

from .views.listing import (
    ListingListView,
    ListingCreateView,
    ListingUpdateView,
    ListingDetailView,
    ListingDeleteView,
)

app_name = "listings"

urlpatterns = [
    path("create/", ListingCreateView.as_view(), name="create"),
    path("<str:ticker>/", ListingDetailView.as_view(), name="detail"),
    path("<str:ticker>/update/", ListingUpdateView.as_view(), name="update"),
    path("<str:ticker>/delete/", ListingDeleteView.as_view(), name="delete"),
    path("", ListingListView.as_view(), name="listings"),
]