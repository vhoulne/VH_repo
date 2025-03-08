import requests
from bs4 import BeautifulSoup
import json

def scrape_dblp_articles(conference_name):
    url = f'https://dblp.uni-trier.de/db/conf/si3d/{conference_name}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Initialiser une liste pour stocker les articles
        articles = []
        # Trouver tous les éléments de liste (balise <li>) contenant les articles
        article_list_items = soup.find_all('li', class_='entry')
        # Parcourir les éléments de la liste des articles
        for item in article_list_items:
            # Extraire le titre de l'article
            title = item.find('span', class_='title').text.strip()
            # Extraire les informations sur les auteurs
            authors = [author.text for author in item.find_all('span', itemprop='author')]
            # Créer un dictionnaire pour stocker les informations de l'article
            article_info = {
                'title': title,
                'authors': authors
            }
            # Ajouter le dictionnaire à la liste des articles
            articles.append(article_info)

        # Imprimer les articles au format JSON
        print(json.dumps(articles, indent=4))
    else:
        print('Erreur lors de la récupération de la page')

# test
scrape_dblp_articles('si3d2020')
