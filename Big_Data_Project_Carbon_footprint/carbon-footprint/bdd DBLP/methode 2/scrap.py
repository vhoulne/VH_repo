import json
import time
######################################### on créé conftest ##########################################################
"""
# Fonction pour transformer la clé de la conférence en URL
def transform_key(key):
    parts = key.split('/')
    return f"https://dblp.org/db/{parts[0]}/{parts[1]}/index.html"

# Ouvrir le fichier d'entrée
with open('conferences.json', 'r') as f_in, open('conftest.json', 'w') as f_out:
    # Charger le contenu du fichier JSON
    data = json.load(f_in)
    
    # Nouveau dictionnaire pour stocker les couples noms de dictionnaires et transformations
    transformed_data = {}
    
    # Parcourir chaque élément du dictionnaire d'entrée
    for key, value in data.items():
        # Appliquer la transformation de la clé
        transformed_key = transform_key(key)
        # Ajouter le couple dans le nouveau dictionnaire
        transformed_data[key] = transformed_key
    
    # Écrire le nouveau dictionnaire dans le fichier de sortie
    json.dump(transformed_data, f_out, indent=4)
    f_in.close()
    f_out.close()
    """
################################# scrapping ###############################################################

import requests
from bs4 import BeautifulSoup

def scrape_with_year(url, year):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        h2_tags = soup.find_all('h2', {'id': str(year)})
        conferences = [h2_tag.text for h2_tag in h2_tags]
        return conferences
    else:
        print("La requête a échoué avec le code :", response.status_code)
        return []
#méthode 1 ( trop long)
    
""""
def scrape_json_database(input_db, output_db):
    with open(input_db, 'r', encoding='utf-8') as f:
        print("start loading")
        data = json.load(f)
        print("finish loading")
    scraped_data = {}
    
    for key, value in data.items():
        # Extraire l'année de la clé si c'est possible
        year = key.split("/")[-1]
        try:
            year = int(year[:4])
        except ValueError:
            # Si la conversion en entier échoue, passer à la prochaine itération
            continue
        
        # Appliquer le scraping uniquement si la clé représente une année valide
        print("scrap init")
        conferences = scrape_with_year(value, year)
        print("scrap finish")
        if conferences:
            scraped_data[key] = conferences
        time.sleep(3)
    
    with open(output_db, 'w', encoding='utf-8') as f:
        print("dumping the data !!!!!!!!!!!!!!!")
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
"""
#méthode 2

def scrape_json_database(input_db, output_db):
    with open(input_db, 'r', encoding='utf-8') as f:
        print("start loading")
        data = json.load(f)
        print("finish loading")
        f.close()

    with open(output_db, 'w', encoding='utf-8') as f:
        ind=53689
        for key, value in data.items():
            # Extraire l'année de la clé si c'est possible
            ind+=1
            year = key.split("/")[-1]
            try:
                year = int(year[:4])
            except ValueError:
                # Si la conversion en entier échoue, passer à la prochaine itération
                continue
            scraped_data = {}   
            # Appliquer le scraping uniquement si la clé représente une année valide
            # print("scrap init")
            conferences = scrape_with_year(value, year)
            # print("scrap finish")
            if conferences:
                scraped_data[key] = conferences
            time.sleep(2)
            print("dumping the data !!!!!!!!!!!!!!!")
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)
            print(ind)
    f.close()
       




# Chemin d'accès des bases de données JSON d'entrée et de sortie
input_db_path = "conftest3.json"
output_db_path = "database_output.json"

# Appel de la fonction de scraping avec les bases de données JSON spécifiées
scrape_json_database(input_db_path, output_db_path)
