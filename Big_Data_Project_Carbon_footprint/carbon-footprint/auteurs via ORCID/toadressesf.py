import json



dico={}
indi=0
cpt=0

print("loading...")
with open('adresses3.json', 'r', encoding='utf-8') as file:
    with open('resultgoogle2.json', 'r', encoding='utf-8') as file2:
        adresses = json.load(file)
        google = json.load(file2)

        for key,value in google.items() :
            indi+=1
            if isinstance(value,dict):
                dico[key]=[value["lat"],value["lng"]]
                cpt+=1
            else:
                dico[key]=adresses[key]
            print(indi)



        
print("dumping")
print(len(dico))
print("fromgoogle : ",cpt)
with open('adresses_f.json', 'w', encoding='utf-8') as f2:
    json.dump(dico, f2, ensure_ascii=False,indent=4)


            