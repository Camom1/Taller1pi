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
    all_movies = Movie.objects.all()

    # --- Movies per year ---
    counts_year = {}
    for m in all_movies:
        y = m.year if m.year else "None"
        counts_year[y] = counts_year.get(y, 0) + 1

    plt.figure()
    years = list(counts_year.keys())
    vals_year = [counts_year[y] for y in years]
    plt.bar(range(len(years)), vals_year, width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year'); plt.ylabel('Number of movies')
    plt.xticks(range(len(years)), years, rotation=90)
    plt.tight_layout()
    buf = io.BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); plt.close()
    graphic_year = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # --- Movies per genre ---
    counts_genre = {}
    for m in all_movies:
        g = (m.genre or '').strip()
        if not g:
            g = 'None'
        else:
            g = g.split(',')[0].split('/')[0].strip()
        counts_genre[g] = counts_genre.get(g, 0) + 1

    plt.figure()
    genres = list(counts_genre.keys())
    vals_genre = [counts_genre[g] for g in genres]
    plt.bar(range(len(genres)), vals_genre, width=0.5, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre'); plt.ylabel('Number of movies')
    plt.xticks(range(len(genres)), genres, rotation=45, ha='right')
    plt.tight_layout()
    buf2 = io.BytesIO(); plt.savefig(buf2, format='png'); buf2.seek(0); plt.close()
    graphic_genre = base64.b64encode(buf2.getvalue()).decode('utf-8')
    buf2.close()

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre,
    })


