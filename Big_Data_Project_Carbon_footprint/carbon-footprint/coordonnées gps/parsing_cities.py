import re
import json

def parse_file(file_path):
    city_data = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            
            tokens = re.split(r'\s+', line.strip())
            
        
            city_name_parts = []
            for i in range(1, len(tokens)):
                if tokens[i] in city_name_parts:
                    break
                city_name_parts.append(tokens[i])
            city_name = ' '.join(city_name_parts)

            # Trouver la première occurrence de latitude et longitude après le nom de la ville
            latitude = None
            longitude = None
            for token in tokens[i:]:
                if re.match(r'^-?\d+\.\d+$', token):
                    if latitude is None:
                        latitude = token
                    elif longitude is None:
                        longitude = token
                        break
            
            if city_name and latitude and longitude:
                if not(city_name in city_data): 
                    city_data[city_name] = {
                        'latitude': latitude,
                        'longitude': longitude
                }

    return city_data

def save_to_json(data, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# on utilise le code pour récupérer les coordonnées 
# GPS des villes à plus de 500, 1000, 5000, 15000 habitants 
json_file_path = 'coordinates.json'
tab=['cities15000.txt','cities5000.txt','cities500.txt','cities1000.txt','allCountries.txt']

for i in range(5):
    file_path = tab[i]
    print('je traite   ', file_path)
    city_data = parse_file(file_path)
    save_to_json(city_data, json_file_path)

print(f"Les données ont été sauvegardées dans {json_file_path}.")
