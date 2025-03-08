import json
###########################################" part 1
#permet de créer le ficheir conférence
"""
# Initialiser un dictionnaire vide pour stocker les conférences avec les titres des articles comme sous-éléments
conferences = {}
ind=0
# Ouvrir le fichier d'entrée
with open('articles.json', 'r') as f:
    # Lire chaque ligne du fichier
    for line in f:
        ind+=1
        # Charger un seul objet JSON à partir de la ligne actuelle
        data = json.loads(line)
        print(ind)
 
        # Récupérer le titre de l'article
        article_title = next((sub_element.get('texte') for sub_element in data.get('sous_elements', []) if sub_element.get('tag') == 'title'), None)
            
        # Récupérer la référence de la conférence
        conference_ref = next((sub_element.get('texte') for sub_element in data.get('sous_elements', []) if sub_element.get('tag') == 'crossref'), None)
            
        # Ajouter le titre de l'article à la liste des titres de la conférence correspondante
        if conference_ref:
            if conference_ref not in conferences:
                conferences[conference_ref] = []
            conferences[conference_ref].append(article_title)
    f.close()

# Écrire les données dans un nouveau fichier JSON
with open('conferences.json', 'w') as output_file:
    json.dump(conferences, output_file, indent=4)
    conferences={}
    output_file.close()
"""
################################################ part 2 
#permet de regarder comment le parser
# Ouvrir le fichier d'entrée
indi=0
with open('conferences.json', 'r', encoding='utf-8') as f_in, open('conferences.txt', 'w', encoding='utf-8') as f_out:
    # Lire le contenu du fichier JSON
    conferences_data = json.load(f_in)
    
    # Parcourir chaque conférence dans les données
    for conference_ref, articles in conferences_data.items():
        indi+=1
        print(indi)
        # Pour chaque article dans la conférence
        for article_title in articles:
            # Écrire la conférence avec le titre de l'article dans le fichier de sortie
            f_out.write(f"{conference_ref}: {article_title}\n")
    f_in.close()
    f_out.close()