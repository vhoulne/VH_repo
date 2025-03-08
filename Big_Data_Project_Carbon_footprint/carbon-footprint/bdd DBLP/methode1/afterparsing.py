import json

# Open the file and load the JSON data
with open('save.json', 'r', encoding='utf-8') as file:
    json_lines = file.readlines()

# Parse each JSON object separately
parsed_data = []
for line in json_lines:
    parsed_data.append(json.loads(line))

# Now you can work with the parsed JSON data
print(parsed_data)  # Example: Print the parsed JSON data
