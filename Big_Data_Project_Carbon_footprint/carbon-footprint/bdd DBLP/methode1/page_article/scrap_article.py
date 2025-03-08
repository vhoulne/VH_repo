##  scrapping d'une page présentant un article pour avoir toutes les infos sur les auteurs


import requests
from bs4 import BeautifulSoup
import json

headers = {
   'User-Agent': 'M',
   }

URL = 'https://ieeexplore.ieee.org/document/6374970'
add="/authors#authors"
url= URL + add

response = requests.get(url,headers=headers)
html = response.text

# Utiliser BeautifulSoup pour trouver le script contenant la variable JavaScript
soup = BeautifulSoup(html, 'html.parser')

S=str(soup)
balise="xplGlobal.document.metadata="
res=S.find(balise)
passage=""
for i in range(0,3000):            #3000 pris arbitrairement mais à priori aucun soucis
    passage+=S[res+i]
d_au=passage.find("authors")
f_au=passage.find("isbn")
PAS=passage[d_au+9:f_au-2]

infos = json.loads(PAS)    # données sous forme de liste de dictionnaires

#############################################################################################################
def get_coordinates(place_name):
    """quand il y a des problèmes dans les données rentrées par le site web, ça retourne None"""
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    response = requests.get(url)
    data = response.json()

    if data:
        # Assuming the first result is the most relevant
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return latitude, longitude
    else:
        return None
    
##############################################################################################################

for elem in infos:
    elem["coordinates"]=get_coordinates(elem["affiliation"][0])

"""
test=infos[1]["affiliation"]
res1=test[0]
print(res1)
print(get_coordinates(res1))
print(infos)
"""