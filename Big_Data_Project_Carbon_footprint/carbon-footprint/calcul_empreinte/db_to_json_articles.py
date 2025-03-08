import sqlite3
import json

def load_data_from_db(db_path):
    """Charge les données depuis une base de données SQLite et les retourne sous forme de liste de tuples."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT article_nom, conference_nom, auteur1, auteur2, auteur3, auteur4, auteur5, auteur6, auteur7, auteur8, auteur9, auteur10 FROM conferences")
    data = cursor.fetchall()
    conn.close()
    return data

def transform_data_to_dict(data):
    """Transforme les données en dictionnaire de dictionnaires."""
    conferences_dict = {}
    cpt=0
    for row in data:
        article_nom = row[0]
        conference_nom = row[1]
        authors = [author for author in row[2:] if author]  # Filtre les auteurs non vides
        
        if conference_nom not in conferences_dict:
            cpt+=1
            print(cpt)
            conferences_dict[conference_nom] = {}
        
        conferences_dict[conference_nom][article_nom] = authors
    
    return conferences_dict

def save_data_to_json(data, json_path):
    """Sauvegarde les données sous forme de fichier JSON."""
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main(db_path, json_path):
    data = load_data_from_db(db_path)
    conferences_dict = transform_data_to_dict(data)
    print("je commence le dump")
    save_data_to_json(conferences_dict, json_path)
    print(f"Les données ont été sauvegardées dans le fichier JSON: {json_path}")

# Chemin du fichier .db et du fichier .json de sortie
db_path = 'articles.db'
json_path = 'articles__.json'

# Appel de la fonction principale
main(db_path, json_path)
