import pytest
from football_fields.models import FootballField, Address, Attachment
from football_fields.forms import FootballFieldForm, AddressForm, AttachmentFormSet, FootballFieldFilterForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
import os

User = get_user_model()

@pytest.mark.django_db
class TestFootballFieldForms():

    @pytest.fixture
    def user_fixture(self):
        yield User.objects.create_user(email='test@user.com', password='abc123')

    @pytest.fixture
    def football_field_form_data(self):
        image_path = os.path.abspath('./football_fields/tests/img/test.png')
        image_data = SimpleUploadedFile('test_image.png', open(image_path, 'rb').read())
        form_data = {'data': {
            'name': 'campinho passarinho',
            'main_image': 'path/to/image/img.jpg',
            'field_dimensions': '250x200',
            'description': 'Um lugar lindo para jogar futebol',
            'grass_type': 'SIN',
            'has_field_lighting': True,
            'has_changing_room': True,
            'facilities': 'Muitas coisas',
            'hour_price': 200,
            'rules': 'não há regras',
        }, 'files': {
            'main_image': image_data
        }}
        yield form_data


    def test_footballfield_form_validation(self, football_field_form_data):
        form = FootballFieldForm(data=football_field_form_data['data'], files=football_field_form_data['files'])
        assert form.is_valid()

    def test_classes_in_filter_form_widget(self):
        form = FootballFieldFilterForm()
        assert 'class="form-check-input"' in form.as_p()
        assert 'class="form-control"' in form.as_p()