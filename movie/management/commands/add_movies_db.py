from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os


class Command(BaseCommand):
    help = 'Load 100 movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # movies.json debe estar en la MISMA carpeta que este archivo:
        # movie/management/commands/movies.json
        here = os.path.dirname(__file__)
        json_path = os.path.join(here, 'movies.json')

        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f'No se encontró {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        created = 0
        updated = 0

        for row in data[:100]:
            # title (obligatorio)
            title = (row.get('title') or row.get('Title') or '').strip()
            if not title:
                continue

            # description (usa la que exista)
            description = (
                row.get('description')
                or row.get('plot')
                or row.get('overview')
                or ''
            ).strip()

            # genre (si es lista toma el primero; si es string toma antes de la coma)
            genres_raw = row.get('genre') or row.get('genres') or ''
            if isinstance(genres_raw, list):
                genre = (genres_raw[0] if genres_raw else '') or ''
            else:
                genre = str(genres_raw).split(',')[0].strip() if genres_raw else ''

            # year (int o None)
            year_raw = row.get('year') or row.get('Year')
            try:
                year = int(year_raw) if year_raw not in (None, '', 'None') else None
            except Exception:
                year = None

            defaults = {
                'description': description,
                'genre': genre,
                'year': year,
                # ruta relativa a MEDIA_ROOT
                'image': 'media/movie/images/default.jpg',
            }

            obj, was_created = Movie.objects.get_or_create(title=title, defaults=defaults)
            if was_created:
                created += 1
            else:
                # si ya existe, actualiza campos
                for k, v in defaults.items():
                    setattr(obj, k, v)
                obj.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Procesadas {min(len(data), 100)} películas. Creadas: {created}, Actualizadas: {updated}.'
        ))
