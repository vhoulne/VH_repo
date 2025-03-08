import json

liste=[]
ind=0
with open('adresses1.json', 'r', encoding='utf-8') as file:
    adresses = json.load(file)
    for key, value in adresses.items():
        ind+=1
        print(ind)
        if value==[0,0]:
            liste.append(key)
    

print( len(liste))
