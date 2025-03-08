import sqlite3
import json
import math
import re


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcule et retourne la distance entre deux points GPS."""
    R = 6371  # Rayon de la terre en km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculer_emissions_co2e(distance_km):
    """
    :param distance_km: Distance parcourue en kilomètres
    :return: Emissions de CO2e en tonnes
    """
    transports = [
        {"mode": "Voiture", "seuil_min": 0, "seuil_max": 250, "facteur_emission": 0.192},
        {"mode": "Train", "seuil_min": 250, "seuil_max": 500, "facteur_emission": 0.041},
        {"mode": "Avion (court-courrier)", "seuil_min": 500, "seuil_max": 1500, "facteur_emission": 0.255},
        {"mode": "Avion (long-courrier)", "seuil_min": 1500, "seuil_max": float('inf'), "facteur_emission": 0.150}
    ]

    for transport in transports:
        if transport["seuil_min"] <= distance_km < transport["seuil_max"]:
            facteur_emission = transport["facteur_emission"]
            break
    else:
        facteur_emission = 0

    emissions_tonnes_co2e = distance_km * facteur_emission / 1000
    return emissions_tonnes_co2e


def load_data_from_db(db_path, query):
    """Charge les données depuis une base de données SQLite selon la requête spécifiée."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def load_gps_coordinates(json_path):
    """Charge les coordonnées GPS à partir d'un fichier JSON avec l'encodage utf-8."""
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_authors_from_json(json_path):
    """Charge les auteurs à partir d'un fichier JSON."""
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_articles_from_json(json_path):
    """Charge les articles à partir d'un fichier JSON."""
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def find_nearest_author(conference_coords, authors_coords):
    """Trouve l'auteur le plus proche de la conférence donnée."""
    min_empreinte = float('inf')
    selected_author = None
    for author_id, (lat, lon) in authors_coords.items():
        distance = haversine_distance(conference_coords[0], conference_coords[1], lat, lon)
        empreinte = calculer_emissions_co2e(distance)
        if empreinte < min_empreinte:
            min_empreinte = empreinte
            selected_author = author_id
    return selected_author, min_empreinte

def extract_year(conference_string):
    """Extrait l'année de la chaîne de conférence."""
    match = re.search(r'[-/](\d{4})$', conference_string)
    if match:
        return int(match.group(1))
    match = re.search(r'[-/](\d{2})$', conference_string)
    if match:
        year = int(match.group(1))
        return 1900 + year if year < 100 else 2000 + year
    match = re.search(r'(\d{4})$', conference_string)
    if match:
        return int(match.group(1))
    return None

def main(articles, authors, gps_coords, conferences_gps_coords):
    result = {}
    
    for year, conferences in articles.items():
        total_yearly_empreinte = 0
        
        for conference_id, articles_data in conferences.items():
            if conference_id in conferences_gps_coords:
                conference_coords = conferences_gps_coords[conference_id][2:4]
                if conference_coords == [0, 0]:
                    continue  # Skip if conference coordinates are not valid

                total_empreinte = 0

                for article_nom, article_authors in articles_data.items():
                    authors_coords = {author: gps_coords[authors[author]] for author in article_authors if author in authors and authors[author] in gps_coords}
                    selected_author, empreinte = find_nearest_author(conference_coords, authors_coords)
                    total_empreinte += empreinte if empreinte != float('inf') else 0

                total_yearly_empreinte += total_empreinte
        
        result[year] = total_yearly_empreinte

    return result

def save_dict_to_json(data, output_file_path):
    """Enregistre un dictionnaire dans un fichier JSON."""
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Chargement des données en dehors de la fonction main
gps_coords = load_gps_coordinates('adresses_f.json')
conferences_gps_coords = load_gps_coordinates('conferences_finales.json')
articles = load_articles_from_json('par_année_classement.json')
authors = load_authors_from_json('authors.json')

# Transformation des données
transformed_data = main(articles, authors, gps_coords, conferences_gps_coords)

# Sauvegarde des données transformées dans un nouveau fichier JSON
output_file_path = 'transformed_articles.json'
save_dict_to_json(transformed_data, output_file_path)
print(f"Transformed data saved to {output_file_path}")
