import json
import sqlite3


json_file_path = 'articles_f.json'
db_file_path = 'articles.db'

# Charger le contenu du fichier JSON
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Créer une connexion à la base de données SQLite
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Créer la table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS conferences (
        article_nom TEXT,
        conference_nom TEXT,
        auteur1 TEXT,
        auteur2 TEXT,
        auteur3 TEXT,
        auteur4 TEXT,
        auteur5 TEXT,
        auteur6 TEXT,
        auteur7 TEXT,
        auteur8 TEXT,
        auteur9 TEXT,
        auteur10 TEXT
    )
''')

# Insérer les données dans la table
for article_nom, details in data.items():
    conference_nom = details[0]
    auteurs = details[1]  # Liste des auteurs
    if len(auteurs)>10:
        auteurs=auteurs[:10]
    # Ajouter None pour les colonnes d'auteurs manquantes
    while len(auteurs) < 10:
        auteurs.append(None)

    cursor.execute('''
        INSERT INTO conferences (
            article_nom, conference_nom, auteur1, auteur2, auteur3, auteur4,
            auteur5, auteur6, auteur7, auteur8, auteur9, auteur10
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (article_nom, conference_nom, *auteurs))
    conn.commit()



# Sauvegarder (commit) les modifications
conn.commit()

# Fermer la connexion
conn.close()

print("Les données ont été insérées avec succès dans la base de données.")
