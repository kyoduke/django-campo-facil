from django.db import models

# Create your models here.

"""
    O modelo deve ter:

    nome
    endereço
    dimensão do campo

    /////////////////////// fotos do campo

    descrição
    tipo de gramado
    iluminação noturna = bool
    vestiário = bool
    preço por hora
    facilidades = text field
    regras de uso
"""




class FootballField(models.Model):

    GRASS_CHOICES = [
    ('SIN', 'Sintético'),
    ('NAT', 'Natural'),
    ('HIB', 'Híbrido'),
    ]

    main_image = models.ImageField(blank=True, null=True, upload_to='football_fields_images')
    name = models.CharField(max_length=100, default='Campo')
    field_dimensions = models.CharField(max_length=9, blank=True, default='')
    description = models.TextField(max_length=1500, blank=True, default='')
    grass_type = models.CharField(max_length=3, choices=GRASS_CHOICES, default='SIN')
    has_field_lighting = models.BooleanField(blank=True, default=False)
    has_changing_room = models.BooleanField(blank=True, default=False)
    hour_price = models.PositiveSmallIntegerField(null=True)
    facilities = models.TextField(max_length=500, blank=True, default='')
    rules = models.TextField(max_length=1500, blank=True, default='')


    def save(self, *args, **kwargs):
        super().save()

    def __str__(self) -> str:
        return self.name

class Address(models.Model):

    STATE_CHOICES = [
    ('RJ', 'Rio de Janeiro'),
    ('SP', 'São Paulo'),
    ('MG', 'Minas Gerais'),
    ]

    football_field = models.OneToOneField(FootballField, on_delete=models.CASCADE, related_name='address')
    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='')
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    cep_code = models.CharField(max_length=9)


    def save(self, *args, **kwargs):
        super().save()
    def __str__(self) -> str:
        return f'{self.address_one} {self.address_two} - {self.state}'

class Attachment(models.Model):
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='attachments') 
    image = models.ImageField(blank=True, null=True, upload_to='football_fields_images')


    def save(self, *args, **kwargs):
        super().save()

    def __str__(self) -> str:
        return self.image.name