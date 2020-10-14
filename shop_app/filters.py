import django_filters
from . import models
from django.forms import CheckboxSelectMultiple

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
    widget=CheckboxSelectMultiple,
    queryset=models.Category.objects.all()
    )

    class Meta:
        model = models.Product
        fields = ['category']