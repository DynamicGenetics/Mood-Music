import factory
from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import post_generation


class UserFactory(factory.django.DjangoModelFactory):

    email = factory.Faker("email", domain="bristol.ac.uk")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else factory.Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(self.password)

    class Meta:
        model = get_user_model()
