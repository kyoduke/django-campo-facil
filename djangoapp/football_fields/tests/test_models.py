import pytest 
from django.core.exceptions import ValidationError
from football_fields.models import FootballField, Address

@pytest.mark.django_db
class TestModels:

    @pytest.fixture
    def field(self):
        return FootballField.objects.create(name='campinho', hour_price=200)

    @pytest.fixture
    def address_fixture(self, field):
        return Address.objects.create(football_field=field, address_one='R. Dois', state='RJ', city='Maricá', district='Itaipuaçu', cep_code='24999-392')

    def test_field_creation_without_price(self):
        with pytest.raises(ValidationError, match="hour_price"):
            FootballField.objects.create(name='campinho')

        assert FootballField.objects.all().count() == 0


    def test_field_str_method(self, field):
        assert field.__str__() == f'{field.name}'


    @pytest.mark.parametrize(
            'address_one, address_two, state, city, district, cep_code, error',
            [
                ('', 'Quadra 2', 'RJ', 'Maricá', 'Itaipuaçu', '24999-293', 'address_one'),
                ('R. Dois', 'Quadra 2', '', 'Maricá', 'Itaipuaçu', '24999-293', 'state'),
                ('R. Dois', 'Quadra 2', 'RJ', '', 'Itaipuaçu', '24999-293', 'city'),
                ('R. Dois', 'Quadra 2', 'RJ', 'Maricá', '', '24999-293', 'district'),
                ('R. Dois', 'Quadra 2', 'RJ', 'Maricá', 'Itaipuaçu', '', 'cep_code'),
            ]
    )
    def test_empty_address_creation(self, field, address_one, address_two, state, city, district, cep_code, error):
        with pytest.raises(ValidationError, match=error):
            Address.objects.create(football_field=field, address_one=address_one, address_two=address_two, state=state, city=city, district=district, cep_code=cep_code)
        

    def test_address_creation(self, address_fixture):
        assert Address.objects.all().count() == 1


    def test_address_str_method(self, address_fixture):
        assert address_fixture.__str__() == f'{address_fixture.address_one} {address_fixture.address_two} - {address_fixture.state}'