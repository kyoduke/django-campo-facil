from django import forms


class FootballFieldReportFilterForm(forms.Form):
    # implement in the future
    # TYPE_CHOICES =  [
    #     ('pdf', 'PDF'),
    #     ('csv', 'CSV'),
    # ]
    # type = forms.ChoiceField(choices=TYPE_CHOICES)
    from_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}), required=False
    )
    to_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}), required=False
    )
