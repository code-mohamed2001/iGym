# checkins/filters.py
import django_filters
from .models import CheckIn


class CheckInFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date',
        label='Created at date',
    )
    visit_type = django_filters.ChoiceFilter(
        choices=CheckIn.VISIT_TYPE_CHOICES
    )
    created_at__gte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    class Meta:
        model = CheckIn
        fields = ['visit_type', 'date']
