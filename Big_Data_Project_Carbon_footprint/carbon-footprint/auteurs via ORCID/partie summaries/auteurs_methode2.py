import json
import sqlite3

cpt = 0
cpu = 0

def normalize_name(name):
    """Normalise le nom en supprimant les espaces et en le mettant en minuscules."""
    return ''.join(name.lower().split())

print("loading")

# Chargement des données depuis les fichiers JSON
with open('auteurs_before_summaries.json', 'r', encoding='utf-8') as file:
    with open('orcid_summaries.json', 'r', encoding='utf-8') as file2:
        orcid = json.load(file2)
        dblp = json.load(file)  # pas vrmt dblp mtn

        # Création de la connexion à la base de données SQLite
        conn = sqlite3.connect('auteurs_2.db')
        cursor = conn.cursor()

        # Création de la table auteurs si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auteurs (
                author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                author_name TEXT,
                author_location TEXT,
                nom2 TEXT   
            )
        ''')

        # Insertion des données dans la table auteurs
        for key, value in dblp.items():
            cpt += 1
            print(cpt)
            author_name = key
            author_location = value["ville"]
            nom2 = value["nom2"]

            if author_location == "":
                # Chercher dans orcid
                if author_name in orcid:
                    y = orcid[author_name].get('ville')
                    if y and y != "yyy":
                        author_location = y
                        cpu += 1
                else:
                    n = normalize_name(author_name)
                    if n in orcid:
                        y = orcid[n].get('ville')
                        if y and y != "yyy":
                            author_location = y
                            cpu += 1
                    elif nom2 and nom2 in orcid:
                        y = orcid[nom2].get('ville')
                        if y and y != "yyy":
                            author_location = y
                            cpu += 1

            # Insertion des données dans la table auteurs
            cursor.execute('''
                INSERT INTO auteurs (author_name, author_location, nom2) VALUES (?, ?, ?)
            ''', (author_name, author_location, nom2))

        print("dumping")
        print("orcid apporte :", cpu)
        
        # Commit des changements et fermeture de la connexion à la base de données
        conn.commit()
        conn.close()
