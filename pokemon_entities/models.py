from datetime import datetime

from django.utils import timezone
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='Нет описания')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    appeared_at = models.DateTimeField(default=datetime.now(), blank=True)
    disappeared_at = models.DateTimeField(default=datetime.now(), blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def is_visible(self):
        if self.appeared_at < timezone.localtime() < self.disappeared_at:
            return True
