import django_filters

from .models import Visit


class VisitFilter(django_filters.FilterSet):
    start_date_time_gte = django_filters.DateTimeFilter(
        field_name='start_date_time',
        lookup_expr='gte',
    )
    start_date_time_lte = django_filters.DateTimeFilter(
        field_name='start_date_time',
        lookup_expr='lte',
    )

    class Meta:
        model = Visit
        fields = ['status', 'caregiver', 'patient']
