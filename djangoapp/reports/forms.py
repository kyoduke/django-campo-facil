from django import forms 


class FootballFieldReportFilterForm(forms.Form):
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)


