import json
import sqlite3

# Charger le fichier JSON
with open('conferences_finales.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Connexion à la base de données SQLite (création si elle n'existe pas)
conn = sqlite3.connect('conferences.db')
cursor = conn.cursor()

# Créer la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS conferences (
    conference_ID TEXT PRIMARY KEY,
    location TEXT
)
''')

# Insérer les données dans la table
for key, value in data.items():
    conference_id = key
    location = value[1]  # le deuxième élément de la liste
    cursor.execute('''
    INSERT INTO conferences (conference_ID, location) VALUES (?, ?)
    ''', (conference_id, location))

# Sauvegarder (commit) les changements et fermer la connexion
conn.commit()
conn.close()

print("Les données ont été insérées avec succès dans la base de données 'conferences.db'.")
