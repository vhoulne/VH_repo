import json
import requests
import sqlite3
import time
import faiss
import numpy as np
from thefuzz import process

# Charger le fichier JSON
with open('/home/infres/pgonzalez-23/auteurs_finaux.json', 'r', encoding='utf-8') as file:
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
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            conn_orcid = sqlite3.connect(db_path, timeout=60)  # Ouvrir avec accès en lecture et écriture
            cursor_orcid = conn_orcid.cursor()
            cursor_orcid.execute('SELECT nom_source, ville, id_chercheur FROM chercheurs')
            for row in cursor_orcid.fetchall():
                normalized_name = normalize_name(row[0])
                orcid_data[normalized_name] = (row[1], row[2])
            conn_orcid.close()
            break
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                retries += 1
                time.sleep(5)  # Attendre 5 secondes avant de réessayer
            else:
                raise
    return orcid_data

def load_orcid_dois(db_path):
    """Charge les DOI depuis la base de données ORCID."""
    dois_data = {}
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            conn_orcid = sqlite3.connect(db_path, timeout=60)  # Ouvrir avec accès en lecture et écriture
            cursor_orcid = conn_orcid.cursor()
            cursor_orcid.execute('SELECT id_chercheur, doi FROM dois')
            for row in cursor_orcid.fetchall():
                dois_data.setdefault(row[0], []).append(row[1])
            conn_orcid.close()
            break
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                retries += 1
                time.sleep(5)  # Attendre 5 secondes avant de réessayer
            else:
                raise
    return dois_data

# Préparer les données ORCID pour Faiss
print("on va commencer pour load_orcid_date")
orcid_data = load_orcid_data("/home/infres/pgonzalez-23/lamedell17/carbon-footprint/ORCID.db")
orcid_dois = load_orcid_dois("/home/infres/pgonzalez-23/lamedell17/carbon-footprint/ORCID.db")
print("on a fini pour load_orcid_date et on commence pour names ")
orcid_names = list(orcid_data.keys())
print("on a fini pour names")
orcid_locations = [value[0] for value in orcid_data.values()]
orcid_ids = [value[1] for value in orcid_data.values()]
print("on a fini avec le listing ")
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

def fetch_orcid_location_and_dois_faiss(author_name, threshold=80):
    normalized_author_name = normalize_name(author_name)
    name_vector = np.zeros((1, d), dtype='float32')
    for char in normalized_author_name:
        name_vector[0, ord(char) % d] += 1
    
    D, I = index.search(name_vector, 1)
    if D[0][0] < threshold:
        location = orcid_locations[I[0][0]]
        id_chercheur = orcid_ids[I[0][0]]
        dois = orcid_dois.get(id_chercheur, [])
        return location, dois[:3]  # Limiter à trois DOI
    return None, []

# Créer une connexion à la base de données SQLite
conn = sqlite3.connect('auteurs.db')
cursor = conn.cursor()

# Créer la table avec `author_ID` comme clé primaire autoincrémentée
cursor.execute('''
CREATE TABLE IF NOT EXISTS auteurs (
    author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT,
    author_location TEXT,
    DOI1 TEXT,
    DOI2 TEXT,
    DOI3 TEXT
)
''')

# Insérer les données dans la table
for key, value in data.items():
    author_name = key
    author_location = ""
    DOI1, DOI2, DOI3 = "", "", ""
    if value:
        dict_value = value
        if "note" in dict_value:
            note = dict_value["note"]
            print("Localisation trouvée dans le fichier JSON")
            author_location = note
    else:
        print(f"on commence la recherche dans ORCID pour l'auteur {author_name}")
        # Recherche dans les données préchargées ORCID avec Faiss
        author_location, dois = fetch_orcid_location_and_dois_faiss(author_name)
        if author_location:
            print(f"Localisation trouvée dans ORCID.db pour {author_name}: {author_location}")
            if dois:
                DOI1, DOI2, DOI3 = dois[0], dois[1] if len(dois) > 1 else "", dois[2] if len(dois) > 2 else ""
        else:
            print(f"Localisation non trouvée pour {author_name}")

    cursor.execute('''
        INSERT INTO auteurs (author_name, author_location, DOI1, DOI2, DOI3) VALUES (?, ?, ?, ?, ?)
    ''', (author_name, author_location, DOI1, DOI2, DOI3))
    conn.commit()
    print("Insertion en cours...")

# Sauvegarder (commit) les changements et fermer la connexion
conn.commit()
conn.close()

print("Les données ont été insérées avec succès dans la base de données 'auteurs.db'.")
