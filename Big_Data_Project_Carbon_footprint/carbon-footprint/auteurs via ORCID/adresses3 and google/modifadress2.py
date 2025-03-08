import json
dico={}

indi=0
print("loading...")
with open('adresses1.json', 'r', encoding='utf-8') as file:

    adresses = json.load(file)


    for key,value in adresses.items():
        indi+=1
        if isinstance(value[0],str):
            dico[key]=[float(value[0]),float(value[1])]
        else:
            dico[key]=value
        print(indi)

print("dumping")
print(len(dico))
with open('adresses3.json', 'w', encoding='utf-8') as f2:
    json.dump(dico, f2, ensure_ascii=False,indent=4)


            