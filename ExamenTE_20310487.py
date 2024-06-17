import requests
import pandas as pd
import hashlib
import time
import sqlite3
import json
#Obtener datos de la API de REST Countries
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
countries = response.json()
#Listas para almacenar los datos
data = []
#Procesar cada país
for country in countries:
    start_time = time.time()
    name = country.get('name', {}).get('common', 'Unknown')
    languages = country.get('languages', {})
    language_names = list(languages.values())
    if language_names:
        language = language_names[0]
        #Encriptar el idioma con SHA1
        language_sha1 = hashlib.sha1(language.encode()).hexdigest()
    else:
        language_sha1 = 'Unknown'
    end_time = time.time()
    processing_time = end_time - start_time
    data.append([name, language_sha1, processing_time])
#Crear un DataFrame con Pandas
df = pd.DataFrame(data, columns=['Country', 'Language_SHA1', 'Time'])
#Calcular estadísticas de tiempo
total_time = df['Time'].sum()
average_time = df['Time'].mean()
min_time = df['Time'].min()
max_time = df['Time'].max()
print(f"Total Time: {total_time:.6f} seconds")
print(f"Average Time: {average_time:.6f} seconds")
print(f"Min Time: {min_time:.6f} seconds")
print(f"Max Time: {max_time:.6f} seconds")
#Guardar los datos en una base de datos SQLite
conn = sqlite3.connect('countries.db')
df.to_sql('countries', conn, if_exists='replace', index=False)
#Generar y guardar un archivo JSON con los datos
json_data = df.to_json(orient='records')
with open('data.json', 'w') as json_file:
    json_file.write(json_data)
#Cerrar la conexión a la base de datos
conn.close()
