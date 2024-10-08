import pytest
from django.core.exceptions import ValidationError
from football_fields.models import FootballField, Address, Attachment
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestModels:

    @pytest.fixture()
    def user_fixture(self):
        yield User.objects.create_user(email="test@test.com", password="test123")

    @pytest.fixture()
    def football_field_fixture(self, user_fixture):
        yield FootballField.objects.create(
            owner=user_fixture, name="campinho", hour_price=200, main_image="test.jpg"
        )

    @pytest.fixture()
    def address_fixture(self, football_field_fixture):
        yield Address.objects.create(
            football_field=football_field_fixture,
            address_one="R. Dois",
            state="RJ",
            city="Maricá",
            district="Itaipuaçu",
            cep_code="24999-392",
        )

    @pytest.fixture()
    def attachment_fixture(self, football_field_fixture):
        image_url = "http://placehold.it/640x480"
        yield Attachment.objects.create(
            football_field=football_field_fixture, image=image_url
        )

    def test_field_creation_without_price(self):
        with pytest.raises(ValidationError, match="hour_price"):
            FootballField.objects.create(name="campinho")
        assert FootballField.objects.all().count() == 0

    def test_field_str_method(self, football_field_fixture):
        assert football_field_fixture.__str__() == f"{football_field_fixture.name}"

    @pytest.mark.parametrize(
        "address_one, address_two, state, city, district, cep_code, error",
        [
            ("", "Quadra 2", "RJ", "Maricá", "Itaipuaçu", "24999-293", "address_one"),
            ("R. Dois", "Quadra 2", "", "Maricá", "Itaipuaçu", "24999-293", "state"),
            ("R. Dois", "Quadra 2", "RJ", "", "Itaipuaçu", "24999-293", "city"),
            ("R. Dois", "Quadra 2", "RJ", "Maricá", "", "24999-293", "district"),
            ("R. Dois", "Quadra 2", "RJ", "Maricá", "Itaipuaçu", "", "cep_code"),
        ],
    )
    def test_empty_address_creation(
        self,
        football_field_fixture,
        address_one,
        address_two,
        state,
        city,
        district,
        cep_code,
        error,
    ):
        with pytest.raises(ValidationError, match=error):
            Address.objects.create(
                football_field=football_field_fixture,
                address_one=address_one,
                address_two=address_two,
                state=state,
                city=city,
                district=district,
                cep_code=cep_code,
            )

    def test_address_creation(self, address_fixture: Address):
        assert Address.objects.all().count() == 1

    def test_address_str_method(self, address_fixture: Address):
        assert (
            address_fixture.__str__()
            == f"{address_fixture.address_one} {address_fixture.address_two} - {address_fixture.state}"
        )

    def test_attachment_creation(self, attachment_fixture: Attachment):
        assert Attachment.objects.all().count() == 1

    def test_attachment_str_method(self, attachment_fixture: Attachment):
        assert attachment_fixture.__str__() == attachment_fixture.image.name
