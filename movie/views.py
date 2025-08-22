from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import base64


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
            movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, "home.html", {'searchTerm':searchTerm, 'movies':movies, 'name':'Camilo Moreno'})

def about(request):
    return render(request, "about.html")

def signup(request):
    email = request.GET.get('email', '')
    return render(request, 'signup.html', {'email': email})


# movie/views.py
from django.shortcuts import render
from .models import Movie
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

def statistics_view(request):
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Conteo por año
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    # Gráfica de barras
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.figure()
    plt.bar(bar_positions, list(movie_counts_by_year.values()), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(list(bar_positions), list(movie_counts_by_year.keys()), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Exportar a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic})
