from django_filters import rest_framework as filters
from titles.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre')
    category = filters.CharFilter(field_name='category')
    name = filters.CharFilter(field_name='name', lookup_expr="icontains")
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
