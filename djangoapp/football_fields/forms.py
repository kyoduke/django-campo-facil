from django import forms
from football_fields.models import FootballField, Address, Attachment

class FootballFieldForm(forms.ModelForm):
    main_image = forms.ImageField()
    description = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': '5'}))
    hour_price = forms.IntegerField(min_value=0)
    facilities = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':'3'}))
    rules = forms.CharField(max_length=500, widget=forms.widgets.Textarea(attrs={'rows': '3'}))


    class Meta:
        model = FootballField
        fields = ['main_image', 'name', 'field_dimensions', 'description', 'grass_type', 'has_field_lighting', 'has_changing_room', 'hour_price',
                  'facilities', 'rules']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('football_field',)


AttachmentFormSet = forms.inlineformset_factory(
    FootballField,
    Attachment,
    form=forms.models.ModelForm,
    fields = ['image'],
    extra = 3,
    can_delete=True
)


class FootballFieldFilterForm(forms.Form):
    """
    
    """

    # adds an empty choice as default
    grass_choices = [('', '----------')] + FootballField.GRASS_CHOICES.copy()

    labels = {
        'city': 'Cidade',
        'grass_type': 'Tipo de Grama',
        'has_field_lighting': 'Iluminação Noturna',
        'has_changing_room': 'Vestiário',
        'max_hour_price': 'Preço máximo por hora'
    }

    city = forms.CharField(required=False, label=labels['city'])
    grass_type = forms.ChoiceField(choices=grass_choices, required=False, label=labels['grass_type'])
    has_field_lighting = forms.BooleanField(required=False, label=labels['has_field_lighting'])
    has_changing_room = forms.BooleanField(required=False, label=labels['has_changing_room'])
    max_hour_price = forms.IntegerField(min_value=0, required=False, label=labels['max_hour_price'])


    def __init__(self, *args, **kwargs):
        super(FootballFieldFilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
