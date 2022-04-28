from django_filters import FilterSet, AllValuesFilter,IsoDateTimeFilter,NumberFilter,DateRangeFilter,DateFilter,CharFilter,DateTimeFilter

from dash_back.models import Post, Price


class PostFilter(FilterSet):
    start_date = IsoDateTimeFilter(field_name='created_date',lookup_expr=('gte'),)
    end_date = IsoDateTimeFilter(field_name='created_date',lookup_expr=('lte'))
    date_range = DateRangeFilter(field_name='created_date')
    class Meta:
        model = Post
        fields = ['created_date']

class PriceFilter(FilterSet):
    start_date = IsoDateTimeFilter(field_name='timestamp',lookup_expr=('gte'),)
    end_date = IsoDateTimeFilter(field_name='timestamp',lookup_expr=('lte'))
    date_range = DateRangeFilter(field_name='timestamp')
    class Meta:
        model = Price
        fields = ['timestamp']
