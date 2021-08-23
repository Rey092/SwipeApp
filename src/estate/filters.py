from django_filters import rest_framework as filters

from src.estate.models import Apartment


class ApartmentFilter(filters.FilterSet):
    price = filters.RangeFilter()
    price_per_square_meter = filters.RangeFilter()
    area = filters.RangeFilter()

    class Meta:
        model = Apartment
        fields = ["moderation_status", "purpose", "rooms", "furnish", "has_balcony", "for_sale", "complex",
                  "complex_relation_status", "is_booked", "corpus"]
