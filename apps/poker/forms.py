from django import forms
from .models import Table


class NewTable(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_size', 'buy_in']

    def __init__(self, *args, **kwargs):
        super(NewTable, self).__init__(*args, **kwargs)
        self.fields['table_size'].empty_label = None
        self.fields['buy_in'].empty_label = None