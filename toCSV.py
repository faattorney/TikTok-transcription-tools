import csv

input_file = "merged_output.txt"
output_file = "merged_for_sheets.csv"

sections = []
current = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("----- START"):
            current = []
        elif line.startswith("----- END"):
            cell_text = "\n".join(l.rstrip("\n") for l in current)
            sections.append([cell_text])
        else:
            current.append(line)

sections.reverse()

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerows(sections)

print("Output written to:", output_file)
