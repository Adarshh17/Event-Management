from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    """
    Custom filter for Event model.
    Allows filtering by title, location, organizer, and date range.
    """
    title = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    organizer = filters.CharFilter(field_name='organizer__username', lookup_expr='icontains')
    start_date = filters.DateFilter(field_name='start_time', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='end_time', lookup_expr='lte')
    is_public = filters.BooleanFilter()

    class Meta:
        model = Event
        fields = ['title', 'location', 'organizer', 'start_date', 'end_date', 'is_public']
