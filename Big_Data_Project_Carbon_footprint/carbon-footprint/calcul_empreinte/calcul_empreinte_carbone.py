import sqlite3
import json
import math



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
            moyen_transport = transport["mode"]
            facteur_emission = transport["facteur_emission"]
            break
    if distance_km != float('inf'):
        emissions_tonnes_co2e = distance_km * facteur_emission/1000
    else : 
        emissions_tonnes_co2e = distance_km
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
    print("je charge")
    with open(json_path, 'r', encoding='utf-8') as file:
        print("le chargement est good")
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
        empreinte=calculer_emissions_co2e(distance)
        if empreinte < min_empreinte:
            min_empreinte = empreinte
            selected_author = author_id
    return selected_author, min_empreinte 








def main(conferences, articles, authors, gps_coords, conferences_gps_coords):
    grand_total=0
    compteur_conf_total = 0
    compteur_conf_nulle = 0
    compteur_conf_ok = 0

    for conference in conferences:
        compteur_conf_total += 1
        conference_id, conference_location = conference

        if conference_id in conferences_gps_coords:
            conference_coords = conferences_gps_coords[conference_id][2:4]
            if conference_coords != [0, 0]:
                compteur_conf_ok += 1
                total_empreinte = 0
                dist_nulle = 0
                dist_ok = 0

                if conference_id in articles:
                    for article_nom, article_authors in articles[conference_id].items():
                        authors_coords = {author: [0,0] for author in article_authors}
                        for author in authors_coords:
                            if author in authors: 
                                if authors[author] in gps_coords:
                                    authors_coords[author]=gps_coords[authors[author]]
                        selected_author, empreinte = find_nearest_author(conference_coords, authors_coords)
                        if empreinte != float('inf'):
                            total_empreinte += empreinte
                            dist_ok += 1
                        else:
                            dist_nulle += 1

                if dist_ok > 0:
                    moyenne = total_empreinte/ dist_ok
                    total_empreinte += dist_nulle * moyenne 
                    grand_total+=total_empreinte
                print("l'empreinte carbone pour la conf", conference_id,"est:",total_empreinte)

            else:
                compteur_conf_nulle += 1
       
        
    if compteur_conf_nulle > 0 and compteur_conf_ok > 0:
        conf_moyenne = grand_total / compteur_conf_ok 
        grand_total+= conf_moyenne * compteur_conf_nulle 
    print("le grand total est", grand_total)

    
    return grand_total 






# Chargement des données en dehors de la fonction main
gps_coords = load_gps_coordinates('adresses_f.json')
conferences_gps_coords = load_gps_coordinates('conferences_finales.json')
conferences = load_data_from_db('conferences.db', "SELECT conference_id, location FROM conferences")
articles = load_articles_from_json('articles__.json')  # Nouvelle fonction pour charger les articles depuis JSON
authors = load_authors_from_json('authors.json')  # Nouvelle fonction pour charger les auteurs depuis JSON

total_distance_final = main(conferences, articles, authors, gps_coords, conferences_gps_coords)
print(total_distance_final)


