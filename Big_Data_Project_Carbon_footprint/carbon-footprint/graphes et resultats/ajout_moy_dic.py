

import json


val = 51.75
dico={}
cpt=0
cpu=0
print("loading...")
with open('empreinte_carbone_avec_vide.json', 'r', encoding='utf-8') as file:
    with open('conferences_finales.json', 'r', encoding='utf-8') as file2:
        conf = json.load(file)
        conf_name=json.load(file2)

        for key,value in conf.items() :
            if value=="":
                nom=conf_name[key][1]
                if "Virtual" in nom:
                    dico[key]=0
                    cpu+=1
                else:
                    dico[key]=val
            else:
                dico[key]=value
            cpt+=1
            print(cpt)

print("dumping")
print(len(dico))
print(cpu)
with open('conferences_emprunte.json', 'w', encoding='utf-8') as f2:
    json.dump(dico, f2, ensure_ascii=False,indent=4)