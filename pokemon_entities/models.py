from django.utils import timezone
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='название на русском'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='название на английском'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='название на японском'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name='изображение'
    )
    description = models.TextField(
        blank=True,
        verbose_name='описание'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolution',
        verbose_name='из кого эволюционировал'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон'
    )
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(
        null=True,
        verbose_name='появится в'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        verbose_name='исчезнет в'
    )
    level = models.IntegerField(null=True, verbose_name='уровень')
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='здоровье'
    )
    strength = models.IntegerField(null=True, blank=True, verbose_name='сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='атака')
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='выносливость'
    )

    def is_visible(self):
        if self.appeared_at < timezone.localtime() < self.disappeared_at:
            return True

    def __str__(self):
        return "{}, {} уровень".format(self.pokemon.title, self.level)
