from django import forms
from football_fields.models import FootballField, Address, Attachment

class FootballFieldForm(forms.ModelForm):
    main_image = forms.ImageField(max_length=200)
    name = forms.CharField()
    field_dimensions = forms.CharField()
    description = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': '5'}))
    grass_type = forms.ChoiceField(choices=FootballField.GRASS_CHOICES)
    has_field_lighting = forms.BooleanField(required=False)
    has_changing_room = forms.BooleanField(required=False)
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