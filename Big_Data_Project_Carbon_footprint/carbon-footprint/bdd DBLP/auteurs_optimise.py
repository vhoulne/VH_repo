import json
import requests
import sqlite3
import time

# Charger le fichier JSON 
with open('C:/Users/rahma/proj-important/auteurs_finaux.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

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

def fetch_orcid_location(cursor, normalized_author_name, retry_count=5):
    for _ in range(retry_count):
        try:
            cursor.execute('SELECT ville FROM chercheurs WHERE nom_source = ?', (author_name,))
            result = cursor.fetchone()
            if result:
                print("il ya le nom qu'on cherche dans ORCID")
                return result[0]
            else:
                return None 
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                time.sleep(1)  # Attendre avant de réessayer
            else:
                raise
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
                # Recherche dans ORCID.db 
                with sqlite3.connect('C:/Users/rahma/proj-important/ORCID.db') as conn_orcid:
                    cursor_orcid = conn_orcid.cursor()
                    author_location = fetch_orcid_location(cursor_orcid, author_name)
                    if author_location:
                        print(f"Localisation trouvée dans ORCID.db pour {author_name}: {author_location}")
                    else:
                        print(f"Localisation non trouvée pour {author_name}")
    else:
                print(f"on commence la recherche dans ORCID pour l'auteur {author_name}")
                # Recherche dans ORCID.db
                with sqlite3.connect('C:/Users/rahma/proj-important/ORCID.db') as conn_orcid:
                    cursor_orcid = conn_orcid.cursor()
                    author_location = fetch_orcid_location(cursor_orcid, author_name)
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
