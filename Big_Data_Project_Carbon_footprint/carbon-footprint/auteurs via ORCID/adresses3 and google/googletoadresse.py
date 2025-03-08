import json
from itertools import combinations

dico={}

indi=0
cu=0
cp=0
print("loading...")
with open('adresses1.json', 'r', encoding='utf-8') as file:
    with open('resultgoogle.json', 'r', encoding='utf-8') as file2:
        adresses = json.load(file)
        google = json.load(file2)

        for key,value in adresses.items():
            indi+=1
            if value ==[0,0]:
                if key in google:
                    v=google[key]
                    if isinstance(v,dict):
                        dico[key]=[v["lat"],v["lng"]]
                        cu+=1
                    else:
                        dico[key]=[0,0]
                        cp+=1
            else:
                dico[key]=value
            print(indi)

print("dumping")
print(cu+cp)
print(cu)
print(len(dico))
with open('adresses2.json', 'w', encoding='utf-8') as f2:
    json.dump(dico, f2, ensure_ascii=False,indent=4)


            