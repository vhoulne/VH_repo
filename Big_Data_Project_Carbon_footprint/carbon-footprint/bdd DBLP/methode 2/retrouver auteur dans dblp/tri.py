import json

############################################ créer un fichier crossreff    #########################
# Ouvrir le fichier d'entrée
"""print("opening")
with open('t2.json', 'r') as f:
    with open('elements_crossref.json', 'a') as output_file:
        print("starting")
        # Lire chaque ligne du fichier
        for line in f:
            # Charger un seul objet JSON à partir de la ligne actuelle
            data = json.loads(line)
            dump=0
            for key, value in data.items():
                for sub_element in value:
                    if 'crossref' in sub_element:
                        dump+=1
                        break
            if dump>0:
                output_file.write(json.dumps(data) + '\n')
"""
#attention on prend ici que les articles ayant un crossref, à voir si ça suffit

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
print("opening")
with open('elements_crossref.json', 'r') as f: #3,5million d'articles
    with open('articles.json', 'a') as output_file:  #finalment 3,4 million d'articles
        print("starting")
        for line in f:
            # Charger un seul objet JSON à partir de la ligne actuelle
            data = json.loads(line)
            dump=0
            for key, value in data.items():
                for sub_element in value:
                    if 'crossref' in sub_element:
                        if sub_element["crossref"].startswith("conf"):
                            dump+=1
                            break
            if dump>0:
                output_file.write(json.dumps(data) + '\n')
