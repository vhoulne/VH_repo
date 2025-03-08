## permet d'avoir les coordonnées des conférences

import requests
import json
from lxml import etree
import time

#############################################################################################################
def get_coordinates(place_name,ind):

    if any(keyword in place_name.lower() for keyword in ["virtual", "Virtual", "Online", "online"]):
       return [-1, "Virtual", 0,0]
    
    else:
        """quand il y a des problèmes dans les données rentrées par le site web, ça retourne None"""
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
        response = requests.get(url)
        data = response.json()
        if data:
            # Assuming the first result is the most relevant
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return [1, place_name, latitude, longitude]
    
        else:
            ind+=1
            return [0, "", 0,0]
    
##############################################################################################################

def lieu_conf(in_file,out_file):
    ind=4932
    indgalere=0
    
    with open(in_file, 'r', encoding='utf-8') as fin:
        with open(out_file, 'w', encoding='utf-8') as fout:
            conferences_data = json.load(fin)
            for conference_ref, listep in conferences_data.items():
                ind+=1
                dictionnaire={}
                print(ind)
                liste = get_coordinates(listep[1], indgalere)
                dictionnaire[conference_ref] = liste
                json.dump(dictionnaire,fout,ensure_ascii=False,indent=4)
    print('nombre conf',ind)
    print('nombre galere',indgalere)
    
#lieu_conf("conf_adress_max1.json", "conf_lieu3.json")

##############################################################################################################
"""vérification de conf_lieu.json"""
def verif_conf(in_file):
   with open(in_file) as f:
    # Lire chaque ligne du fichier
    for line in f:
        # Charger chaque ligne en tant qu'objet JSON
        data = json.loads(line)
        
        # Parcourir les clés et les valeurs de l'objet JSON
        for key, value in data.items():
            print("Clé:", key)
            print("Valeur:", value)

#verif_conf("conf_lieu.json")

##########################################################################################
"""le fichier suivant ;'est pas lisible en .jsons cependant il était utile pour dumper à chaque itération et ne pas tout
perdre à chaque bug. Je l'ai transformé en fichier texte et maintenant il faut en refaire un fichier .json"""

def modif_lieu(f_text,f_out):
    with open(f_text, "r",encoding="utf-8") as f:
        texte=f.read()
        text_list=texte.split("}{")
        dictionnaire={}
        ind=0
        for conf in text_list:
            for i in range(0,len(conf)):
                if conf[i]==':' and conf[i+2]=='[':
                    ind+=1
                    code=conf[:i].strip()
                    code=code.replace("\n","")
                    code=code.replace("'","")
                    code=code.replace('"',"")
                    contenu=conf[i+2:].strip()
                    contenu=contenu.replace("\n","")
                    contenu=eval(contenu)
                    dictionnaire[code]=contenu
        print(ind) 
        with open(f_out, 'w', encoding='utf-8') as f1 :
            json.dump(dictionnaire,f1,ensure_ascii=False,indent=4)       

#modif_lieu("conf_lieu.txt","conferences_finales.json")


##################################################verification#####################################
def verif():
    with open("conf_no_name.json","r",encoding="utf-8") as cr:
        conf=json.load(cr)
        ind=0
        for elem in conf.items():
            ind+=1
        
    with open("conferences_finales.json","r",encoding="utf-8") as cp:
        conf2=json.load(cp)
        ind1=0
        for elem in conf.items():
            ind1+=1

    if ind1==ind:
        return("GOOD")
    else:
        return(ind1-ind)
    #dans notre cas : c'est bon

        