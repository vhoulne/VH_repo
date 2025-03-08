import sqlite3
import json

# Connexion à la base de données
conn = sqlite3.connect('auteurs_2.db')
cursor = conn.cursor()

# Requête SQL pour obtenir le nombre d'occurrences de chaque localisation
query = """
SELECT author_location, COUNT(*) as count
FROM auteurs
GROUP BY author_location
"""
print("querry")
cursor.execute(query)
results = cursor.fetchall()
print("coupting")
# Transformation des résultats en un dictionnaire
location_counts = {row[0]: row[1] for row in results}

# Fermeture de la connexion
conn.close()

# Affichage du dictionnaire
print("dumping")
with open('location_counts.json', 'w', encoding='utf-8') as f:
    json.dump(location_counts, f, ensure_ascii=False,indent=4)

