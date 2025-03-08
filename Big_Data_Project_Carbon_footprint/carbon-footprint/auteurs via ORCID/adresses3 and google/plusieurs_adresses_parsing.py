import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
import json


liste=[]
ind=0
with open('adresses1.json', 'r', encoding='utf-8') as file:
    adresses = json.load(file)
    for key, value in adresses.items():
        ind+=1
        print(ind)
        #if value==[0,0]:
        liste.append(key)

print("geocoding")    
def geocode_address(api_key, address):
    """Fonction pour géocoder une adresse."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': api_key}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Will raise an exception for 4XX/5XX errors
        json_response = response.json()
        if json_response['results']:
            location = json_response['results'][0]['geometry']['location']
            return address, location
        else:
            return address, "No results found"
    except requests.RequestException as e:
        return address, f"Failed to geocode: {str(e)}"

def geocode_addresses_in_batch(api_key, addresses, max_workers=50):
    """Fonction pour géocoder un lot d'addresses en utilisant des requêtes parallèles."""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_address = {executor.submit(geocode_address, api_key, address): address for address in addresses}
        for future in as_completed(future_to_address):
            address, result = future.result()
            results[address] = result
            sleep(0.02)  # Respect the QPS limit by adding a slight delay between submissions
    return results


api_key = "AIzaSyB9E4rC_EMkrir_E3rPqDOCDtLNqxIOX3Y "

# Appel de la fonction de géocodage en lot
geocoded_results = geocode_addresses_in_batch(api_key, liste)
print("dumping....")
print(len(geocoded_results))
# Affichage des résultats
with open('resultgoogle2.json', 'w', encoding='utf-8') as f3:
    json.dump(geocoded_results, f3, ensure_ascii=False,indent=4)

