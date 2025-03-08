import json
import requests
import sqlite3
import time
import faiss
import numpy as np
from thefuzz import process

# Charger le fichier JSON
with open('C:/Users/Paul/Desktop/auteurs_finaux.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def normalize_name(name):
    """Normalise le nom en supprimant les espaces et en le mettant en minuscules."""
    return ''.join(name.lower().split())

def get_coordonnees(place_name):
    """Cette fonction permet de retourner les coordonnées GPS d'un endroit à partir de son adresse en utilisant l'API de Nominatim d'OpenStreetMap."""
    if any(keyword in place_name.lower() for keyword in ["virtual", "Virtual", "Online", "online"]):
        return [-1, "Virtual", 0, 0]
    else:
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Vérifie si la requête a réussi
            try:
                data = response.json()
                if data:
                    latitude = float(data[0]['lat'])
                    longitude = float(data[0]['lon'])
                    return [1, place_name, latitude, longitude]
                else:
                    return [0, "", 0, 0]
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON pour l'adresse : {place_name}")
                return [0, "", 0, 0]
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des coordonnées pour l'adresse {place_name}: {e}")
            return [0, "", 0, 0]
        finally:
            time.sleep(1)  # Ajouter un délai pour éviter de se faire bloquer

def load_orcid_data(db_path):
    """Charge les données ORCID en mémoire."""
    orcid_data = {}
    with sqlite3.connect(db_path, timeout=30) as conn_orcid:
        conn_orcid.execute('PRAGMA journal_mode=WAL;')
        cursor_orcid = conn_orcid.cursor()
        cursor_orcid.execute('SELECT nom_source, ville FROM chercheurs')
        for row in cursor_orcid.fetchall():
            normalized_name = normalize_name(row[0])
            orcid_data[normalized_name] = row[1]
    return orcid_data

# Préparer les données ORCID pour Faiss
orcid_data = load_orcid_data('C:/Users/Paul/Desktop/PROJ104/carbon-footprint/ORCID.db')
orcid_names = list(orcid_data.keys())
orcid_locations = list(orcid_data.values())

# Encoder les noms normalisés en vecteurs pour Faiss
d = 512  # dimension des vecteurs, peut être ajustée selon le besoin
index = faiss.IndexFlatL2(d)

name_vectors = np.zeros((len(orcid_names), d), dtype='float32')
for i, name in enumerate(orcid_names):
    name_vector = np.zeros(d, dtype='float32')
    for char in name:
        name_vector[ord(char) % d] += 1
    name_vectors[i] = name_vector

index.add(name_vectors)

def fetch_orcid_location_faiss(author_name, threshold=80):
    normalized_author_name = normalize_name(author_name)
    name_vector = np.zeros((1, d), dtype='float32')
    for char in normalized_author_name:
        name_vector[0, ord(char) % d] += 1
    
    D, I = index.search(name_vector, 1)
    if D[0][0] < threshold:
        return orcid_locations[I[0][0]]
    return None

# Créer une connexion à la base de données SQLite
conn = sqlite3.connect('auteurs.db')
cursor = conn.cursor()

# Créer la table avec `author_ID` comme clé primaire autoincrémentée
cursor.execute('''
CREATE TABLE IF NOT EXISTS auteurs (
    author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT,
    author_location TEXT,
    DOI TEXT 
)
''')

# Insérer les données dans la table
DOI = ""
for key, value in data.items():
    author_name = key
    author_location = ""
    if value:
        dict_value = value
        if "note" in dict_value:
            note = dict_value["note"]
            coordonnees = get_coordonnees(note)
            if coordonnees != [0, "", 0, 0]:
                print("Localisation trouvée dans le fichier JSON")
                author_location = note
            else:
                print(f"on commence la recherche dans ORCID pour l'auteur {author_name}")
                # Recherche dans les données préchargées ORCID avec Faiss
                author_location = fetch_orcid_location_faiss(author_name)
                if author_location:
                    print(f"Localisation trouvée dans ORCID.db pour {author_name}: {author_location}")
                else:
                    print(f"Localisation non trouvée pour {author_name}")

    cursor.execute('''
        INSERT INTO auteurs (author_name, author_location, DOI) VALUES (?, ?, ?)
    ''', (author_name, author_location, DOI))
    conn.commit()
    print("Insertion en cours...")

# Sauvegarder (commit) les changements et fermer la connexion
conn.commit()
conn.close()

print("Les données ont été insérées avec succès dans la base de données 'auteurs.db'.")
