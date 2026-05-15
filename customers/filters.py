from django import forms
from django.contrib.auth import get_user_model
from django.db.models import F, Q
from django.utils import timezone
import django_filters

from .models import Subscription

# HTML5 date picker in DRF browsable API / django-filter forms
_DATE_FILTER_WIDGET = forms.DateInput(
    attrs={"type": "date"},
    format="%Y-%m-%d",
)


def _computed_expired_q() -> Q:
    """Matches SubscriptionSerializer.check_subscription_status == 'expired'."""
    today = timezone.now().date()
    return Q(end_date__lt=today) | Q(
        kind="session_pack",
        session_limit=F("sessions_used"),
    )


class SubscriptionFilter(django_filters.FilterSet):
    """
    Filters subscriptions. ``status=active`` / ``status=expired`` use the same
    rules as ``SubscriptionSerializer.check_subscription_status`` (not the DB
    column). ``status=cancelled`` / ``status=paused`` filter on the stored
    ``Subscription.status`` field.

    Date ranges (optional, inclusive):

    - ``start_date_min`` / ``start_date_max`` — ``start_date`` within the range.
    - ``end_date_min`` / ``end_date_max`` — ``end_date`` within the range.
    """

    kind = django_filters.ChoiceFilter(
        field_name="kind",
        choices=Subscription.KIND_CHOICES,
        empty_label="All",
    )
    created_by = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        empty_label="All",
    )
    status = django_filters.ChoiceFilter(
        choices=Subscription.STATUS_CHOICES,
        method="filter_status",
        empty_label="All",
    )
    start_date_min = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="gte",
        widget=_DATE_FILTER_WIDGET,
    )
    start_date_max = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="lte",
        widget=_DATE_FILTER_WIDGET,
    )
    end_date_min = django_filters.DateFilter(
        field_name="end_date",
        lookup_expr="gte",
        widget=_DATE_FILTER_WIDGET,
    )
    end_date_max = django_filters.DateFilter(
        field_name="end_date",
        lookup_expr="lte",
        widget=_DATE_FILTER_WIDGET,
    )

    class Meta:
        model = Subscription
        fields = ["kind", "created_by", "status", "customer"]

    def filter_status(self, queryset, name, value):
        if value in (None, ""):
            return queryset
        expired_q = _computed_expired_q()
        if value == "expired":
            return queryset.filter(expired_q)
        if value == "active":
            return queryset.filter(~expired_q)
        if value in ("cancelled", "paused"):
            return queryset.filter(status=value)
        return queryset.none()

