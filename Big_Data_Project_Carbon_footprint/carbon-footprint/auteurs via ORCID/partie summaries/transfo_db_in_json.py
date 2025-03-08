import sqlite3
import json
print("loading...")
# Connexion à la base de données SQLite
conn = sqlite3.connect('auteurs.db')
cursor = conn.cursor()

# Exécution de la requête pour récupérer les données
cursor.execute('SELECT author_ID, author_name, author_location, nom2 FROM auteurs')

# Initialisation du dictionnaire pour stocker les données
data_dict = {}
cpt=0
# Parcours des résultats de la requête
for row in cursor.fetchall():
    id, nom_source, ville, nom2 = row
    if nom_source not in data_dict:
        data_dict[nom_source] = {
            'id': id,
            'nom2': nom2,
            'ville': ville
            }
    cpt+=1
    print(cpt)

# Fermeture de la connexion à la base de données
conn.close()
print("writing")
# Écriture du dictionnaire au format JSON dans un fichier
with open('auteurs_before_summaries.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)

print('Conversion terminée. Le fichier JSON a été créé avec succès.')
