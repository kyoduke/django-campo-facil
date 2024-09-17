from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FootballField(models.Model):

    GRASS_CHOICES = [
        ("SIN", "Sintético"),
        ("NAT", "Natural"),
        ("HIB", "Híbrido"),
    ]

    main_image = models.ImageField(
        blank=True, null=True, upload_to="football_fields_images"
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=100, default="Campo")
    field_dimensions = models.CharField(max_length=9, blank=True, default="")
    description = models.TextField(max_length=1500, blank=True, default="")
    grass_type = models.CharField(max_length=3, choices=GRASS_CHOICES, default="SIN")
    has_field_lighting = models.BooleanField(blank=True, default=False)
    has_changing_room = models.BooleanField(blank=True, default=False)
    hour_price = models.PositiveSmallIntegerField(null=True)
    facilities = models.TextField(max_length=500, blank=True, default="")
    rules = models.TextField(max_length=1500, blank=True, default="")

    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()

    def __str__(self) -> str:
        return self.name


class Address(models.Model):

    STATE_CHOICES = [
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    ]

    football_field = models.OneToOneField(
        FootballField, on_delete=models.CASCADE, related_name="address"
    )
    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="")
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    cep_code = models.CharField(max_length=9)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=7, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=7, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()

    def __str__(self) -> str:
        return f"{self.address_one} {self.address_two} - {self.state}"


class Attachment(models.Model):
    football_field = models.ForeignKey(
        FootballField, on_delete=models.CASCADE, related_name="attachments"
    )
    image = models.ImageField(blank=True, null=True, upload_to="football_fields_images")

    def save(self, *args, **kwargs):
        super().save()

    def __str__(self) -> str:
        return self.image.name
