from django.contrib.auth import get_user_model
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from football_fields.models import FootballField
import pytest
import os


User = get_user_model()

@pytest.mark.django_db
class TestFootballFieldViews():

    @pytest.fixture
    def form_data(self):
        image_path = os.path.abspath('./football_fields/tests/img/test.png')
        data = {
            'address_one': 'R. Dois',
            'state': 'RJ',
            'city': 'Maricá',
            'district': 'Itaipuaçu',
            'cep_code': '24999-23',
            'main_image': SimpleUploadedFile('test.png',open(image_path, 'rb').read()),
            'name': 'campinhola',
            'description': 'hellloo',
            'grass_type': 'SIN',
            'hour_price': 240,
            'facilities': 'sim',
            'rules': 'no hay rules',
            'image': '',
            'attachments-TOTAL_FORMS': 0,
            'attachments-INITIAL_FORMS': 0,
        }
        yield data

    @pytest.fixture
    def user_fixture(self):
        yield User.objects.create_user(email='test_views@views.com', password='abc123')

    @pytest.fixture
    def logged(self, client: Client, user_fixture):
        logged = client.login(email=user_fixture.email, password='abc123')
        yield logged 

    def test_access_without_login(self, client: Client):
        response = client.get('/fields/')

        assert '/accounts/login/' in response.url
        assert response.status_code == 302

    def test_access_with_logged_user(self, client: Client, logged):
        response = client.get('/fields/')

        assert logged is True
        assert response.status_code == 200

    def test_post_invalid_data(self, client: Client, logged):
        response = client.post('/fields/new')
        content = response.content.decode('utf-8')

        assert 'errorlist' in content
        assert response.status_code == 200

    def test_field_creation_with_valid_data(self, client: Client, logged, form_data):
        response = client.post('/fields/new', data=form_data)
        count = FootballField.objects.all().count()

        assert count == 1

    def test_post_request_redirects(self, client: Client, logged, form_data):
        print(FootballField.objects.all().count())
        response = client.post('/fields/new', data=form_data)
        print(response.content.decode('utf-8'))

        assert response.status_code == 302
        assert 'fields' in response.url


    def test_is_form_rendered(self, client: Client, logged):
        response = client.get('/fields/new')
        content = response.content.decode('utf-8')
        print(content)
        assert response.status_code == 200
        assert '<input type="text"' in content