import json

# Load JSON data from sample.json
with open('sample.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Read configuration from config.txt
with open('config.txt', 'r', encoding='utf-8') as config_file:
    config_lines = config_file.readlines()

# Extract configuration values
json_file_name = config_lines[0].strip().split('=')[1].strip()  # Extracts "sample.json"
password = config_lines[1].strip().split('=')[1].strip().strip('"')  # Extracts "Schulung24!" and removes surrounding quotes
excluded_usernames = [line.strip() for line in config_lines[2:] if line.strip()]  # Extracts excluded usernames

# Function to filter users based on excluded usernames
def filter_users(users, excluded_usernames):
    filtered_users = []
    for user in users:
        if user['userName'] not in excluded_usernames:
            filtered_users.append(user)
    return filtered_users

# Filter users based on excluded usernames
filtered_users = filter_users(data['Resources'], excluded_usernames)

# Prepare output operations
operations = []
for user in filtered_users:
    operation = {
        "method": "PATCH",
        "path": f"/Users/{user['id']}",
        "bulkId": "clientBulkId1",
        "data": {
            "schemas": ["urn:scim:schemas:core:2.0:User"],
            "password": password
        }
    }
    operations.append(operation)

# Prepare output JSON structure
output_json = {"Operations": operations}

# Write output JSON to a file
with open('output.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_json, outfile, indent=2)

# Print required information counts
input_count = len(data['Resources'])
excluded_count = len(data['Resources']) - len(filtered_users)
output_count = len(filtered_users)

print(f"Number of IDs from the source: {input_count}")
print(f"Number of excluded IDs: {excluded_count}")
print(f"Number of output IDs: {output_count}")
