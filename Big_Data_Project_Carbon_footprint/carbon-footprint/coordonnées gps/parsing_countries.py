import json

def load_city_data(file_path):
    # Charger les données des villes à partir d'un fichier JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        city_data = json.load(file)
    return city_data

def load_country_capitals(json_file_path):
    # Charger les données des capitales des pays à partir du fichier JSON
    with open(json_file_path, 'r', encoding='utf-8') as file:
        country_capitals = json.load(file)
    return country_capitals

def get_country_coordinates(city_data, country_capitals):
    country_coords = {}
    for country, capital in country_capitals.items():
        if country=="France":
            print("on trouve la France")
        # Rechercher les coordonnées de la capitale dans les données des villes
        capital_data = next((city for city in city_data if city.lower() == capital.lower()), None)
        if capital_data:
            latitude = city_data[capital_data]['latitude']
            longitude = city_data[capital_data]['longitude']
            country_coords[country] = {'latitude': latitude, 'longitude': longitude}
            print("tout va bien pour la France")
           
        
    return country_coords

def add_country_entries(city_data, country_coords):
    # Ajouter chaque pays en tant que nouvelle entrée dans le dictionnaire des villes
    for country, coords in country_coords.items():
        
        city_data[country] = {
            'latitude': coords['latitude'],
            'longitude': coords['longitude']
        }
        print(f"Added country {country} with coordinates: {coords['latitude']}, {coords['longitude']}")
    
    return city_data

def save_city_data(city_data, output_file_path):
    # Sauvegarder les données mises à jour dans un fichier JSON
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(city_data, json_file, ensure_ascii=False, indent=4)

# Chemins des fichiers
city_data_file_path = 'copy.json'
country_capitals_file_path = 'codes.json'
output_file_path = 'updated_coordinates_travaux.json'

# Charger les données
city_data = load_city_data(city_data_file_path)
country_capitals = load_country_capitals(country_capitals_file_path)

# Obtenir les coordonnées GPS de la capitale pour chaque pays
country_coords = get_country_coordinates(city_data, country_capitals)

# Ajouter chaque pays en tant que nouvelle entrée dans le dictionnaire des villes
updated_city_data = add_country_entries(city_data, country_coords)

# Sauvegarder les données mises à jour
save_city_data(updated_city_data, output_file_path)

print(f"Les données mises à jour ont été sauvegardées dans {output_file_path}.")
