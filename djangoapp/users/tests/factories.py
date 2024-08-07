import factory
from faker import Faker
from users.models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


    email = fake.email()
    password = fake.password()
    phone_number = fake.phone_number()
    first_name = fake.first_name()
    last_name = fake.last_name()
    profile_image = fake.image_url()