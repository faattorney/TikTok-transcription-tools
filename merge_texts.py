import os

def merge_text_files(input_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(input_folder)):
            filepath = os.path.join(input_folder, filename)

            if not os.path.isfile(filepath):
                continue

            if filename.lower().endswith(".txt"):
                separator_start = f"\n----- START {filename} -----\n"
                separator_end   = f"\n----- END {filename} -----\n"

                outfile.write(separator_start)

                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())

                outfile.write(separator_end)
            else:
                print(f"Skipping non-text file: {filename}")

    print(f"Merged text saved to: {output_file}")

if __name__ == "__main__":
    input_folder = "Downloaded_Audio"       
    output_file = "merged_output.txt"

    merge_text_files(input_folder, output_file)
