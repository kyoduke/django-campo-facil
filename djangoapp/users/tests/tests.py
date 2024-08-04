import pytest
from users.models import User
from allauth.account.forms import SignupForm
# Create your tests here.


@pytest.mark.parametrize(
    'email, password1, password2, validity',
    [
        ('arnaldo@gmail.com', 'hjkln4142', 'hjkln4142', True),
        ('arnaldo@gmail.com', '123', '123', False),
        ('', 'hjkln4142', 'hjkln4142', False),
        ('arnaldo@gmail.com', '', 'hjkln4142', False),
        ('arnaldo@gmail.com', 'hjkln4142', '', False),
        ('arnaldo', 'hjkln4142', 'hjkln4142', False),
    ],
)
@pytest.mark.django_db
def test_user_signup_form(email,password1, password2, validity):
    form = SignupForm(data={
        'email': email,
        'password1': password1,
        'password2': password2,
    }
    )
    assert form.is_valid() is validity
