import json
dico={}
ind=0
with open('conf_per_year.json', 'r', encoding='utf-8') as file:
    conf = json.load(file)
    print("starting")
    for key,value in conf.items():
        ind+=1
        dico[key]={}
        for year, fotprint in value.items():
            if len(year)==2:
                y=0
                try:
                    y=int(year)
                    if y > 24:
                        y+=1900
                    if y <=24:
                        y+=2000
                except Exception as e:
                    y+=year
                    print(key,year)
                dico[key][y]=fotprint
            else:
                dico[key][year]=fotprint
print(ind)
print("dumping")
print(len(dico))
with open('conf_per_year2.json', 'w', encoding='utf-8') as f:
    json.dump(dico, f, ensure_ascii=False, indent=4)