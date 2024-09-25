from django import forms
from football_fields.models import FootballField, Address, Attachment


class FootballFieldForm(forms.ModelForm):
    description = forms.CharField(widget=forms.widgets.Textarea(attrs={"rows": "5"}))
    hour_price = forms.IntegerField(min_value=0)
    facilities = forms.CharField(widget=forms.widgets.Textarea(attrs={"rows": "3"}))
    rules = forms.CharField(
        max_length=500, widget=forms.widgets.Textarea(attrs={"rows": "3"})
    )

    class Meta:
        model = FootballField
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(FootballFieldForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs["class"] = "form-check-input"
            elif isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs["class"] = "form-select"
            else:
                visible.field.widget.attrs["class"] = "form-control"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("football_field",)

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs["class"] = "form-check-input"
            elif isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs["class"] = "form-select"
            else:
                visible.field.widget.attrs["class"] = "form-control"


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        exclude = ("football_field",)

    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.FileInput):
                visible.field.widget.attrs["class"] = "form-control"


AttachmentFormSet = forms.inlineformset_factory(
    FootballField,
    Attachment,
    form=AttachmentForm,
    fields=["image"],
    extra=3,
    can_delete=True,
)


class FootballFieldFilterForm(forms.Form):
    """ """

    # adds an empty choice as default
    grass_choices = [("", "----------")] + FootballField.GRASS_CHOICES.copy()

    labels = {
        "city": "Cidade",
        "grass_type": "Tipo de Grama",
        "has_field_lighting": "Iluminação Noturna",
        "has_changing_room": "Vestiário",
        "max_hour_price": "Preço máximo por hora",
    }

    city = forms.CharField(required=False, label=labels["city"])
    grass_type = forms.ChoiceField(
        choices=grass_choices, required=False, label=labels["grass_type"]
    )
    has_field_lighting = forms.BooleanField(
        required=False, label=labels["has_field_lighting"]
    )
    has_changing_room = forms.BooleanField(
        required=False, label=labels["has_changing_room"]
    )
    max_hour_price = forms.IntegerField(
        min_value=0, required=False, label=labels["max_hour_price"]
    )

    def __init__(self, *args, **kwargs):
        super(FootballFieldFilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs["class"] = "form-check-input"
            elif isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs["class"] = "form-select"
            else:
                visible.field.widget.attrs["class"] = "form-control"
