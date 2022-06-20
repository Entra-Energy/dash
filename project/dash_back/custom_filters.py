import django_filters
from dash_back import models as django_models
from django_filters import rest_framework as filters
from rest_framework import viewsets

class PriceFilter(filters.FilterSet):
    class Meta:
        model = django_models.Price
        fields = {
            'timestamp': ('lte', 'gte')
        }

    filter_overrides = {
        django_models.Price: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }

class PostFilter(filters.FilterSet):
    class Meta:
        model = django_models.Post
        fields = {
            'created_date': ('lte', 'gte')
        }










# from django_filters import FilterSet, AllValuesFilter,IsoDateTimeFilter,NumberFilter,DateRangeFilter,DateFilter,CharFilter,DateTimeFilter
#
# from dash_back.models import Post, Price


# class PostFilter(FilterSet):
#
#     start_date = IsoDateTimeFilter(field_name='created_date',lookup_expr=('gte'),)
#     end_date = IsoDateTimeFilter(field_name='created_date',lookup_expr=('lte'))
#     date_range = DateRangeFilter(field_name='created_date')
#     dev = AllValuesFilter(field_name='devId')
#     class Meta:
#         model = Post
#         fields = ('start_date','end_date','date_range','dev')
#
# class PriceFilter(FilterSet):
#     start_date = IsoDateTimeFilter(field_name='timestamp',lookup_expr=('gte'),)
#     end_date = IsoDateTimeFilter(field_name='timestamp',lookup_expr=('lte'))
#     date_range = DateRangeFilter(field_name='timestamp')
#     class Meta:
#         model = Price
#         fields = ['timestamp']
