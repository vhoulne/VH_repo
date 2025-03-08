import json
import sqlite3

# Étape 1 : Lire le fichier JSON
with open('C:/Users/Paul/Desktop/auteurs_finaux.json', 'r', encoding='utf-8') as f:
    auteurs = json.load(f)



# Étape 2 : Créer une base de données SQLite
conn = sqlite3.connect('auteurs_test.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS auteurs (
    auteur_ID TEXT PRIMARY KEY
)
''')

# Étape 3 : Insérer les données dans la table
for auteur_id in auteurs.keys():
    print("Insertion de l'auteur ID :", auteur_id)  # Afficher l'auteur ID pour vérification
    cursor.execute('''
    INSERT INTO auteurs (auteur_ID) VALUES (?)
    ''', (auteur_id,))
    conn.commit()

# Sauvegarde (commit) des modifications et fermeture de la connexion
conn.commit()

# Vérifiez le contenu de la table
cursor.execute('SELECT * FROM auteurs')
rows = cursor.fetchall()
print("Contenu de la table après insertion :")
for row in rows:
    print(row)

conn.close()
