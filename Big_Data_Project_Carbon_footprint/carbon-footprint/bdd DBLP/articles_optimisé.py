import json
import sqlite3
import faiss
import numpy as np
from thefuzz import process

# Charger les fichiers JSON
print("Chargement du fichier articles_finaux_valid.json...")
with open('C:/Users/rahma/proj-important/articles_finaux_valid.json', 'r', encoding='utf-8') as file:
    articles_data = json.load(file)
print("Le fichier articles_finaux_valid.json a été chargé avec succès.")

print("Chargement du fichier conferences.json...")
with open('C:/Users/rahma/proj-important/presentation_020524/conferences/conferences.json', 'r', encoding='utf-8') as file:
    conferences_data = json.load(file)
print("Le fichier conferences.json a été chargé avec succès.")

# Préparer les données pour FAISS
print("Préparation des données pour FAISS...")
titles = []
title_to_article = {}
for article in articles_data:
    inproceedings = article.get('inproceedings', [])
    for item in inproceedings:
        if 'title' in item:
            title = item['title']
            titles.append(title)
            title_to_article[title] = article

# Créer un index FAISS pour les titres
d = 512  # dimension des vecteurs, peut être ajustée selon le besoin
index = faiss.IndexFlatL2(d)

title_vectors = np.zeros((len(titles), d), dtype='float32')
for i, title in enumerate(titles):
    title_vector = np.zeros(d, dtype='float32')
    for char in title.lower():
        title_vector[ord(char) % d] += 1
    title_vectors[i] = title_vector

index.add(title_vectors)

def fetch_article_faiss(article_title, threshold=80):
    if article_title is None:
        return None
    title_vector = np.zeros((1, d), dtype='float32')
    for char in article_title.lower():
        title_vector[0, ord(char) % d] += 1
    
    D, I = index.search(title_vector, 1)
    if D[0][0] < threshold:
        return titles[I[0][0]]
    return None

# Connexion à la base de données SQLite
print("Connexion à la base de données SQLite...")
conn = sqlite3.connect('conference_articles.db')
cursor = conn.cursor()
print("Connexion réussie.")

# Créer la table
print("Création de la table conference_articles si elle n'existe pas déjà...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS conference_articles (
    article_nom TEXT PRIMARY KEY,
    conference_nom TEXT,
    auteur_1 TEXT,
    auteur_2 TEXT,
    auteur_3 TEXT,
    auteur_4 TEXT,
    auteur_5 TEXT,
    auteur_6 TEXT,
    auteur_7 TEXT,
    auteur_8 TEXT
)
''')
print("Table créée ou déjà existante.")

# Extraire les données et insérer dans la table
print("Insertion des données dans la table conference_articles...")
for conf_name, articles in conferences_data.items():
    print(f"Traitement de la conférence : {conf_name}")
    for article_title in articles:
        if article_title is None:
            print("Article sans titre trouvé, ignoré.")
            continue
        print(f"Traitement de l'article : {article_title}")
        found_title = fetch_article_faiss(article_title)
        if found_title:
            article = title_to_article[found_title]
            inproceedings = article.get('inproceedings', [])
            authors = [item['author'] for item in inproceedings if 'author' in item]
            authors += [''] * (8 - len(authors))  # Remplir avec des chaînes vides si moins de 8 auteurs

            # Insérer chaque ligne individuellement
            cursor.execute('''
            INSERT OR IGNORE INTO conference_articles (
                article_nom, conference_nom, auteur_1, auteur_2, auteur_3, auteur_4, auteur_5, auteur_6, auteur_7, auteur_8
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (article_title, conf_name, authors[0], authors[1], authors[2], authors[3], authors[4], authors[5], authors[6], authors[7]))
            print(f"Article {article_title} inséré dans la base de données.")
        else:
            print(f"Article non trouvé dans articles_finaux_valid.json: {article_title}")
        # Sauvegarder les changements après chaque insertion
        conn.commit()

# Fermer la connexion
conn.close()
print("Connexion à la base de données fermée.")
print("Les données ont été insérées avec succès dans la base de données 'conference_articles.db'.")
=======
import json
import sqlite3
import faiss
import numpy as np
from thefuzz import process

# Charger les fichiers JSON
print("Chargement du fichier articles_finaux_valid.json...")
with open('C:/Users/rahma/proj-important/articles_finaux_valid.json', 'r', encoding='utf-8') as file:
    articles_data = json.load(file)
print("Le fichier articles_finaux_valid.json a été chargé avec succès.")

print("Chargement du fichier conferences.json...")
with open('C:/Users/rahma/proj-important/presentation_020524/conferences/conferences.json', 'r', encoding='utf-8') as file:
    conferences_data = json.load(file)
print("Le fichier conferences.json a été chargé avec succès.")

# Préparer les données pour FAISS
print("Préparation des données pour FAISS...")
titles = []
title_to_article = {}
for article in articles_data:
    inproceedings = article.get('inproceedings', [])
    for item in inproceedings:
        if 'title' in item:
            title = item['title']
            titles.append(title)
            title_to_article[title] = article

# Créer un index FAISS pour les titres
d = 512  # dimension des vecteurs, peut être ajustée selon le besoin
index = faiss.IndexFlatL2(d)

title_vectors = np.zeros((len(titles), d), dtype='float32')
for i, title in enumerate(titles):
    title_vector = np.zeros(d, dtype='float32')
    for char in title.lower():
        title_vector[ord(char) % d] += 1
    title_vectors[i] = title_vector

index.add(title_vectors)

def fetch_article_faiss(article_title, threshold=80):
    if article_title is None:
        return None
    title_vector = np.zeros((1, d), dtype='float32')
    for char in article_title.lower():
        title_vector[0, ord(char) % d] += 1
    
    D, I = index.search(title_vector, 1)
    if D[0][0] < threshold:
        return titles[I[0][0]]
    return None

# Connexion à la base de données SQLite
print("Connexion à la base de données SQLite...")
conn = sqlite3.connect('conference_articles.db')
cursor = conn.cursor()
print("Connexion réussie.")

# Créer la table
print("Création de la table conference_articles si elle n'existe pas déjà...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS conference_articles (
    article_nom TEXT PRIMARY KEY,
    conference_nom TEXT,
    auteur_1 TEXT,
    auteur_2 TEXT,
    auteur_3 TEXT,
    auteur_4 TEXT,
    auteur_5 TEXT,
    auteur_6 TEXT,
    auteur_7 TEXT,
    auteur_8 TEXT
)
''')
print("Table créée ou déjà existante.")

# Extraire les données et insérer dans la table
print("Insertion des données dans la table conference_articles...")
for conf_name, articles in conferences_data.items():
    print(f"Traitement de la conférence : {conf_name}")
    for article_title in articles:
        if article_title is None:
            print("Article sans titre trouvé, ignoré.")
            continue
        print(f"Traitement de l'article : {article_title}")
        found_title = fetch_article_faiss(article_title)
        if found_title:
            article = title_to_article[found_title]
            inproceedings = article.get('inproceedings', [])
            authors = [item['author'] for item in inproceedings if 'author' in item]
            authors += [''] * (8 - len(authors))  # Remplir avec des chaînes vides si moins de 8 auteurs

            # Insérer chaque ligne individuellement
            cursor.execute('''
            INSERT OR IGNORE INTO conference_articles (
                article_nom, conference_nom, auteur_1, auteur_2, auteur_3, auteur_4, auteur_5, auteur_6, auteur_7, auteur_8
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (article_title, conf_name, authors[0], authors[1], authors[2], authors[3], authors[4], authors[5], authors[6], authors[7]))
            print(f"Article {article_title} inséré dans la base de données.")
        else:
            print(f"Article non trouvé dans articles_finaux_valid.json: {article_title}")
        # Sauvegarder les changements après chaque insertion
        conn.commit()

# Fermer la connexion
conn.close()
print("Connexion à la base de données fermée.")
print("Les données ont été insérées avec succès dans la base de données 'conference_articles.db'.")
>>>>>>> ece0cc6fb556d38535bfe10911f685417a45680a
