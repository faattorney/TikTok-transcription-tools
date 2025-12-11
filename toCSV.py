import csv
import os

input_folder = "Downloaded_Audio"
output_file = "merged_for_sheets.csv"

sections = []

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    
    if not os.path.isfile(filepath):
        continue
    
    if filename.lower().endswith(".txt"):
        with open(filepath, 'r', encoding='utf-8') as infile:
            content = infile.read()
            sections.append([content]) 

sections.reverse()

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerows(sections)

print(f"Output written to: {output_file}")