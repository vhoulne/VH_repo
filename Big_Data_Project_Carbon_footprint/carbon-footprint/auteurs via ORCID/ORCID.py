import os
import sqlite3
import xml.etree.ElementTree as ET

# Fonction pour créer la base de données et la table
def create_database():
    conn = sqlite3.connect('orcid_profiles.db')
    cursor = conn.cursor()
    
    # Création de la table orcid_profiles si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcid_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orcid_id TEXT NOT NULL,
            full_name TEXT NOT NULL,
            address TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Fonction pour insérer un profil ORCID dans la base de données
def insert_orcid_profile(orcid_id, full_name, address):
    conn = sqlite3.connect('orcid_profiles.db')
    cursor = conn.cursor()
    
    # Insérer les données dans la table
    cursor.execute('''
        INSERT INTO orcid_profiles (orcid_id, full_name, address)
        VALUES (?, ?, ?)
    ''', (orcid_id, full_name, address))
    
    conn.commit()
    conn.close()

# Fonction pour parser un fichier XML et extraire les informations pertinentes
def parse_xml_file(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        orcid_id = xml_file.split('/')[-1].split('.')[0]
        
        # Récupérer le nom complet
        full_name = root.find('.//{http://www.orcid.org/ns/personal-details}credit-name')
        if full_name is not None:
            full_name = full_name.text
        else:
            given_name = root.find('.//{http://www.orcid.org/ns/personal-details}given-names')
            family_name = root.find('.//{http://www.orcid.org/ns/personal-details}family-name')
            if given_name is not None and family_name is not None:
                full_name = given_name.text + ' ' + family_name.text
            else:
                full_name = "xxx"

        # Récupérer l'adresse sans tenir compte des namespaces
        address_element = None
        for elem in root.iter():
            if elem.tag.endswith('address'):
                address_element = elem
                break

        address = None
        if address_element is not None:
            city, region, country = None, None, None
            for child in address_element:
                if child.tag.endswith('city'):
                    city = child.text
                elif child.tag.endswith('region') or child.tag.endswith('name'):
                    region = child.text
                elif child.tag.endswith('country'):
                    country = child.text

            address_parts = []
            if city:
                address_parts.append(city)
            if region:
                address_parts.append(region)
            if country:
                address_parts.append(country)
                
            address = ', '.join(address_parts)
        
        if address is None:
            address = "yyy"
            

        return (orcid_id, full_name, address)
    
    except Exception as e:
        print(f"Erreur lors du traitement du fichier {xml_file}: {e}")
        return None

# Fonction récursive pour parcourir tous les fichiers XML dans un répertoire et ses sous-répertoires
def process_xml_files(directory):
    create_database()
    cpt = 0
    doss000 = os.listdir(directory)
    for dossier in doss000:  # dossier : 000, 010, 910 etc
        chemin_dossier = os.path.join(directory, dossier)
        chercheurliste = os.listdir(chemin_dossier) 
        for file in chercheurliste:
            xml_file = os.path.join(chemin_dossier, file)
            profile_data = parse_xml_file(xml_file)      
            if profile_data:
                cpt += 1
                insert_orcid_profile(*profile_data)
                # print(f"Profil ORCID {profile_data[0]} inséré dans la base de données.")
                print(cpt)

    print("Traitement des fichiers XML terminé.")

# Exemple d'utilisation
if __name__ == '__main__':
    directory_path = '/data/vhoulne-23/ORCID_2023_10_summaries'
    process_xml_files(directory_path)
