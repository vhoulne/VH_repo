import json
from itertools import combinations

def sous_phrases(phrase, max_mots=4):
    mots = phrase.split()
    sous_phrases = []
    
    for longueur in range(1, max_mots + 1):
        for i in range(len(mots) - longueur + 1):
            sous_phrases.append(' '.join(mots[i:i + longueur]))
    
    return sous_phrases

dico={}
indi=0
cpt=0
print("loading...")
with open('cities+countries+codes_countries.json', 'r', encoding='utf-8') as file:
    with open('location_counts.json', 'r', encoding='utf-8') as file2:
        adresses = json.load(file2)
        latlong = json.load(file)

        for key in adresses :
            indi+=1
            l_phrases=sous_phrases(key)
            ind=0
            for mot in l_phrases:
                if mot in latlong:
                    coo=latlong[mot]
                    dico[key]=(coo["latitude"],coo["longitude"])
                    ind+=1
                    cpt+=1
                    break
            if ind==0:
                dico[key]=(0,0)
            print("nbr :",indi,"ajout : ",cpt)

        
print("dumping")
with open('adresses1.json', 'w', encoding='utf-8') as f2:
    json.dump(dico, f2, ensure_ascii=False,indent=4)


            