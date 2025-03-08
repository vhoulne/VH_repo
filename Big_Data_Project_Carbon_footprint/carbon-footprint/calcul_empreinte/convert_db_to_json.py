import sqlite3
import json


def load_data_from_db(db_path):
    """Charge les données depuis une base de données SQLite et les retourne sous forme de dictionnaire."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT author_name, author_location FROM auteurs")
    data = cursor.fetchall()
    conn.close()
    
    # Convertir les données en dictionnaire
    authors_dict = {author_name: author_location for author_name, author_location in data}
    return authors_dict



def save_data_to_json(data, json_path):
    """Sauvegarde les données sous forme de fichier JSON."""
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)



def main(db_path, json_path):
    authors_dict = load_data_from_db(db_path)
    save_data_to_json(authors_dict, json_path)
    print(f"Les données ont été sauvegardées dans le fichier JSON: {json_path}")



# Chemin du fichier .db et du fichier .json de sortie
db_path = 'auteurs_f.db'
json_path = 'authors.json'



# Appel de la fonction principale
main(db_path, json_path)
