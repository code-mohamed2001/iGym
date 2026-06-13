# checkins/filters.py
import django_filters
import datetime
from .models import CheckIn


class CheckInFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='created_at',
        method='filter_by_date',
        label='Created at date',
    )
    visit_type = django_filters.ChoiceFilter(
        choices=CheckIn.VISIT_TYPE_CHOICES,
        empty_label="All",
        method='filter_visit_type'
    )

    def filter_by_date(self, queryset, name, value):
        """
        Convert the date to a UTC range to avoid SQLite timezone issues.
        value is a datetime.date object.
        """
        import pytz
        cairo = pytz.timezone('Africa/Cairo')

        # start of day in Cairo → convert to UTC
        start = cairo.localize(
            datetime.datetime.combine(value, datetime.time.min))
        end = cairo.localize(
            datetime.datetime.combine(value, datetime.time.max))

        start_utc = start.astimezone(pytz.utc)
        end_utc = end.astimezone(pytz.utc)

        return queryset.filter(created_at__range=(start_utc, end_utc))

    def filter_visit_type(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(visit_type=value)

    class Meta:
        model = CheckIn
        fields = ['visit_type', 'date']
