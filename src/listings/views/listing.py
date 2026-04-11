from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from ..models.listing import Listing
from ..forms import ListingForm


class ListingListView(ListView):
    model = Listing


class ListingDetailView(DetailView):
    model = Listing

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Listing, ticker=self.kwargs["ticker"])


class ListingCreateView(CreateView):
    form_class = ListingForm
    model = Listing


class ListingUpdateView(UpdateView):
    form_class = ListingForm
    model = Listing

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Listing, ticker=self.kwargs["ticker"])


class ListingDeleteView(DeleteView):
    model = Listing
    success_url = reverse_lazy("listings:listings")

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Listing, ticker=self.kwargs["ticker"])
