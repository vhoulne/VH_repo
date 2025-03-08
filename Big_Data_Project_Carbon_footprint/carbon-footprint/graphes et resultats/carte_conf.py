import json
import pandas as pd
import folium
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Charger les données JSON avec encodage UTF-8
with open('transformed_conferences.json', 'r', encoding='utf-8') as f:
    adresses_f = json.load(f)

with open('location_conferences_counts.json', 'r', encoding='utf-8') as f:
    location_count = json.load(f)

# Créer une liste pour stocker les données fusionnées
data = []

for location, count in location_count.items():
    location = location.strip()  # Enlever les espaces en trop
    if location in adresses_f:
        lat = adresses_f[location]["latitude"]
        lon = adresses_f[location]["longitude"]
        # Vérifier que les coordonnées sont valides
        if lat != 0 and lon != 0 and -90 <= lat <= 90 and -180 <= lon <= 180:
            data.append([location, lat, lon, count])

# Convertir en DataFrame
df = pd.DataFrame(data, columns=['Location', 'Latitude', 'Longitude', 'Count'])

# Créer la carte de densité
m = folium.Map(location=[0, 0], zoom_start=2)

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=max(1, min(row['Count'], 5)),  # Limiter la taille des cercles
        popup=row['Location'],
        color='red',  # Couleur rouge pour les bordures des cercles
        fill=True,
        fill_color='red',  # Couleur rouge pour l'intérieur des cercles
        fill_opacity=0.6
    ).add_to(m)

# Enregistrer la carte en fichier HTML
m.save('population_density_map3.html')
