import json
import csv

# File paths
json_file = 'questions.json'  # Replace with your JSON file name
csv_file = 'google_form_mcq.csv'

# Read JSON data
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return questions
# Convert JSON to CSV format
def json_to_csv(json_data, csv_filename):
    with open(csv_filename, mode='w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header for Google Form CSV (Question Title, Option 1, Option 2, ...)
        writer.writerow(['Question Title', 'Option 1', 'Option 2', 'Option 3', 'Option 4'])
        
        # Write each question and its options
        for entry in json_data:
            row = [entry['question']] + entry['options']
            writer.writerow(row)

    print(f"CSV file '{csv_filename}' created successfully!")

# Main logic
if __name__ == "__main__":
    data = load_json(json_file)
    json_to_csv(data, csv_file)
