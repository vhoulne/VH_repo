
import json

dico={}
cpt=0
print("loading...")
with open('conferences_emprunte.json', 'r', encoding='utf-8') as file:
        conf = json.load(file)
        for key,value in conf.items() :
                if type(value)==str:
                       print(key)
                       print(value)
                       break


                code = key.split('/')[1]
                year = key.split('/')[2][:4]

                if code in dico:
                        if year in dico[code]:
                                dico[code][year]+=value
                        else:
                                dico[code][year] =value
                else:
                        dico[code]={}
                        dico[code][year]=value

                cpt+=1
                print(cpt)

print("dumping")
print(len(dico))
with open('conf_per_year.json', 'w', encoding='utf-8') as f2:
    json.dump(dico, f2, ensure_ascii=False,indent=4)



         


            