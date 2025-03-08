# cet algorithme va permettre de calculer l'empreinte carbone des différentes conférences
#les données d'entrée sont 
## Table conferences : Contient les colonnes conference_id, location
## Table articles : Contient les colonnes article_id, conference_id, authors (une liste d'auteurs séparés par des virgules).
## Table authors : Contient les colonnes author_id, location
# tous situées sur un seul fichier SQlite dont le chemin est db_path 

import random
import math
import sqlite3


def haversine_distance(lat1, lon1, lat2, lon2):
    "cette fonction permet de calculer et retourner la distance entre 2 endroits à partir de leurs coordonnées GPS (lat1,lon1) et (lat2,lon2) à l'aide de la formule de Haversine"
    R = 6371  # Rayon de la terre en km 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_coordonnees(place_name):
    " cette fonction permet de retourner les coordonnées GPS d'un endroit à partir de son adresse en utilisant l'API de Nominatim d'OpenStreetMap"
    if any(keyword in place_name.lower() for keyword in ["virtual", "Virtual", "Online", "online"]):
        return [-1, "Virtual", 0, 0]
    else:
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
        response = requests.get(url)
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return [1, place_name, latitude, longitude]
        else:
            return [0, "", 0, 0]
        

def load_data_from_db(db_path):
    "cette fonction permet de charger les données des conférences, des articles et des auteurs à partir de la base de données SQLite et de les retourner sous forme de dictionnaires"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # ici on charge le dictionnaire des conférences
    cursor.execute("SELECT conference_id, location FROM conferences")
    conferences = {}
    for row in cursor.fetchall():
        conference_id, location = row
        status, place_name, lat, lon = get_coordonnees(location)
        if status == 1:
            conferences[conference_id] = (lat, lon)
    
      # ici on charge le dictionnaire des articles
    cursor.execute("SELECT article_id, conference_id, authors FROM articles")
    articles = {}
    for row in cursor.fetchall():
        article_id, conference_id, authors_str = row
        authors = authors_str.split(',')
        articles[article_id] = {'conference_id': conference_id, 'authors': authors}
    
    # ici on charge le dictionnaire des auteurs
    cursor.execute("SELECT author_id, location FROM authors")
    authors = {}
    for row in cursor.fetchall():
        author_id, location = row
        status, place_name, lat, lon = get_coordonnees(location)
        if status == 1:
            authors[author_id] = (lat, lon)
    
    conn.close()
    return conferences, articles, authors

def initial_solution(conferences, articles, author_locations):
    "cette fonction permet de générer une solution initiale simple pour gérer le problème de l'affectation des auteurs aux articles en minimisant la distance entre les auteurs et les conférences"
    solution = {}
    total_distance = 0
    
    for article_id, article_data in articles.items():
        conference_id = article_data['conference_id']
        conf_lat, conf_lon = conferences[conference_id]
        
        min_distance = float('inf')
        selected_author = None
        
        for author_id in article_data['authors']:
            author_lat, author_lon = author_locations.get(author_id, (0, 0))
            distance = haversine_distance(conf_lat, conf_lon, author_lat, author_lon)
            
            if distance < min_distance:
                min_distance = distance
                selected_author = author_id
        
        solution[article_id] = selected_author
        total_distance += min_distance
    
    return solution, total_distance