import csv
import sys


def extract_unique_words(csv_file: str, column_name: str, output_file: str):
    unique_words = set()

    # Open the CSV file and iterate over its rows
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Retrieve the text from the specified column
            text = row.get(column_name, "")
            # Split the text into words (splitting by whitespace)
            words = text.split()
            # Add the words to the set to ensure uniqueness
            unique_words.update(words)

    # Write the unique words to the output file, one word per line
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(unique_words):
            f.write(word + "\n")

    print(f"Extracted {len(unique_words)} distinct words to {output_file}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_csv> <column_name> <output_file>")
        sys.exit(1)

    input_csv = sys.argv[1]
    column = sys.argv[2]
    output_f = sys.argv[3]
    extract_unique_words(input_csv, column, output_f)
