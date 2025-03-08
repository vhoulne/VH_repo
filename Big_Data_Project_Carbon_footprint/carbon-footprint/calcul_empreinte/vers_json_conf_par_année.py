import json
import re

def extract_year(conference_string):
    """
    Extract the year from the conference string.
    The year is assumed to be the first 4-digit number after a slash or a dash.
    If a 2-digit year is found, it is assumed to be in the 20th century.
    Handles specific formats like "conf/dimacs/dimacs74", "conf/dimacs/dimacs9", and "conf/birthday/Bibel2000".

    Parameters:
    conference_string (str): The conference string in various formats.

    Returns:
    int: The extracted year, or None if no valid year is found.
    """
    # Try to find a 4-digit year first
    match = re.search(r'[-/](?P<year>\d{4})', conference_string)
    if match:
        return int(match.group('year'))
    
    # If no 4-digit year is found, try to find a 2-digit year
    match = re.search(r'[-/](?P<year>\d{2})', conference_string)
    if match:
        year = int(match.group('year'))
        # Assuming the 2-digit year is in the 20th century if it's less than 100
        if year < 21:
            return 2000 + year
        else:
            return 1900 + year

    # Handle specific cases like "conf/dimacs/dimacs74", "conf/dimacs/dimacs9", and "conf/birthday/Bibel2000"
    match = re.search(r'dimacs(?P<year>\d{2})$', conference_string)
    if match:
        year = int(match.group('year'))
        return 1900 + year
    
    match = re.search(r'dimacs(?P<year>\d{1})$', conference_string)
    if match:
        year = int(match.group('year'))
        return 2000 + year
    
    match = re.search(r'\D(?P<year>\d{4})$', conference_string)
    if match:
        return int(match.group('year'))
    
    # If no valid year is found, return None
    return None

def transform_json_to_dict(json_file_path):
    """
    Transform a JSON file to a dictionary of dictionaries organized by year,
    conference codes, and articles. Excludes conferences without a valid year.

    Parameters:
    json_file_path (str): The path to the JSON file.

    Returns:
    dict: A dictionary organized by years, conference codes, and articles.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    result = {}
    
    for conf_code, articles in data.items():
        year = extract_year(conf_code)
        if (year is not None) :
            if year not in result:
                result[year] = {}
            
            if conf_code not in result[year]:
                result[year][conf_code] = {}
            
            for article, author in articles.items():
                result[year][conf_code][article] = author
    
    return result

def save_dict_to_json(data, output_file_path):
    """
    Save a dictionary to a JSON file.

    Parameters:
    data (dict): The dictionary to save.
    output_file_path (str): The path to the output JSON file.
    """
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
json_file_path = 'articles__.json'
output_file_path = 'par_année_classement.json'

# Transform the JSON data
transformed_dict = transform_json_to_dict(json_file_path)

# Save the transformed data to a new JSON file
save_dict_to_json(transformed_dict, output_file_path)
print(f"Transformed data saved to {output_file_path}")
