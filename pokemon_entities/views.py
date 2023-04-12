import folium

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from .models import Pokemon
from .models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=local_time,
        disappeared_at__gte=local_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else '',
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    local_time = localtime()
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = pokemon.entities.filter(
        appeared_at__lt=local_time,
        disappeared_at__gt=local_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemon_for_template = {
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }

    pokemon_next_evolution = pokemon.next_evolutions.first()
    if pokemon_next_evolution:
        pokemon_for_template['next_evolution'] = {
            'pokemon_id': pokemon_next_evolution.id,
            'title_ru': pokemon_next_evolution.title,
            'img_url': pokemon_next_evolution.image.url
        }

    if pokemon.previous_evolution:
        pokemon_for_template['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': pokemon.previous_evolution.image.url
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_for_template
    })
