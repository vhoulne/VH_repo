import json

############################################ créer un fichier crossreff    #########################
# Ouvrir le fichier d'entrée
"""
with open('t2.json', 'r') as f:
    # Lire chaque ligne du fichier
    for line in f:
        # Charger un seul objet JSON à partir de la ligne actuelle
        data = json.loads(line)
        
        # Filtrer les objets qui contiennent la catégorie "crossref" dans leur sous-élément
        if any(sub_element.get('tag') == 'crossref' for sub_element in data.get('sous_elements', [])):
            # Écrire l'objet filtré dans un autre fichier JSON
            with open('elements_crossref.json', 'a') as output_file:
                output_file.write(json.dumps(data) + '\n')
    f.close()
"""

########################################   créer le fichier des auteurs   ##########################
"""
# Ouvrir le fichier d'entrée
with open('t2.json', 'r') as f:
    # Lire chaque ligne du fichier
    for line in f:
        # Charger un seul objet JSON à partir de la ligne actuelle
        data = json.loads(line)
        
        # Vérifier si le premier élément est "www"
        if data.get('texte') == 'www':
            # Écrire l'objet filtré dans un autre fichier JSON
            with open('elements_www.json', 'a') as output_file:
                output_file.write(json.dumps(data) + '\n')
    f.close()
"""
####################### garder les articles utiles     #############################################
    
# Ouvrir le fichier d'entrée
with open('elements_crossref.json', 'r') as f:
    # Lire chaque ligne du fichier
    for line in f:
        # Charger un seul objet JSON à partir de la ligne actuelle
        data = json.loads(line)
        
        # Rechercher la sous-catégorie "crossref"
        for sub_element in data.get('sous_elements', []):
            if sub_element.get('tag') == 'crossref':
                # Vérifier si la valeur de la sous-catégorie commence par "conf"
                if sub_element.get('texte', '').startswith('conf'):
                    # Écrire l'objet filtré dans un autre fichier JSON
                    with open('articles.json', 'a') as output_file:
                        output_file.write(json.dumps(data) + '\n')
                    break  # Sortir de la boucle une fois qu'un élément est trouvé
    f.close()
