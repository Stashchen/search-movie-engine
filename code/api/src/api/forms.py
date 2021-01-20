from django import forms
from django.core.validators import MinValueValidator

from .logic.data_structures.enums import SortField, SortOrder


DEFAULT_MOVIES_FORM_INITIALS = {
    'limit': 50,
    'page': 1,
    'search': '',
    'sort': SortField.ID.value,
    'sort_order': SortOrder.ASC.value
}


class MoviesSearchForm(forms.Form):
    """
    This form checks if the GET params, that are used as ElasticSearch details, are valid.
    """
    limit = forms.IntegerField(min_value=0)
    page = forms.IntegerField(min_value=1)
    search = forms.CharField(required=False)
    sort = forms.ChoiceField(
        choices=(
            (SortField.ID.value, SortField.ID.value),
            (SortField.TITLE.value, SortField.TITLE.value),
            (SortField.IMDB_RATING.value, SortField.IMDB_RATING.value),
        )
    )
    
    sort_order = forms.ChoiceField(
        choices=[
            (SortOrder.ASC.value, SortOrder.ASC.value),
            (SortOrder.DESC.value, SortOrder.DESC.value),
        ]
    )