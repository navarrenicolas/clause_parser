#code adapted from: https://www.geeksforgeeks.org/convert-csv-to-json-using-python/

import csv
import json

# What we want: {“sentence”: “”, “embedded clauses”: [{“predicate”: [], “type”: “”, “clause”: “”, “embedded clauses”: []}]}
# Function to convert a CSV to JSON, takes the file paths as arguments

def make_json(csvFilePath, jsonFilePath):
	data = {}
	
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		
		# Convert each row into a dictionary and add it to data
		for rows in csvReader:
			new_rows = {}
			
			predicate = [{"str": rows["predicate"], "lemma": "", "POS": ""}]    
			emb = [{"predicate": predicate, "type": rows["type"], "clause": "", "embedded clauses": []}]
			new_rows["sentence"] = rows["sents"]
			new_rows["embedded clauses"] = emb
			
			key = rows['line_number']
			data[key] = new_rows
			

	# Open a json writer, and use the json.dumps() 
	# function to dump data
	with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
		jsonf.write(json.dumps(data, indent=4))
		
# Driver Code

# Decide the two file paths according to your 
# computer system
csvFilePath = r'polar_golden_set_checked.csv'
jsonFilePath = r'polar_golden_set_07_2024.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)