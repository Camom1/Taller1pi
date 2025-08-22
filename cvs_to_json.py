import pandas as pd
import json

# Lee el archivo CSV
df = pd.read_csv('movies_initial.csv')

# Guarda el DataFrame como JSON
df.to_json('movies.json', orient='records')

# Verifica que se haya creado correctamente leyendo las primeras 100 películas
with open('movies.json', 'r') as file:
    movies = json.load(file)

for i in range(100):
    movie = movies[i]
    print(movie)
    break
