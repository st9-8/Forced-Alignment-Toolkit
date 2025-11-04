import csv
import sys
import epitran
import argparse
import json
import os

# Initialize Epitran for Fulfulde (ful) using the Latin script (Latn)
# The specific code for the language used in your webonary dictionary might need
# adjustment, but 'ful-Latn' is a standard starting point for Fulfulde.
try:
    # Epitran ID for Fulfulde (ful) using Latin script (Latn)
    epi = epitran.Epitran('ful-Latn')
except RuntimeError as e:
    print(f"Error initializing Epitran: {e}", file=sys.stderr)
    print("Ensure you have the required language data installed for Epitran (e.g., 'ful-Latn').", file=sys.stderr)
    sys.exit(1)


def convert_wordlist_to_ipa(words: list) -> list:
    """
        Convert word list to IPA using Epitran
    """
    ipa_data = []
    print(f"Converting {len(words)} words to IPA...", file=sys.stderr)
    for entry in words:
        word = entry.get('source_text', '')
        if word:
            try:
                # Transliterate the source word to IPA
                ipa_transliteration = ' '.join(epi.trans_list(word))

                # Create a new entry, copying existing fields and adding the IPA
                new_entry = entry.copy()
                new_entry['ipa'] = ipa_transliteration
                ipa_data.append(new_entry)
            except Exception as e:
                print(f"Error converting '{word}' to IPA: {e}", file=sys.stderr)
                # Append the original entry without the IPA field on error
                ipa_data.append(entry)
        else:
            ipa_data.append(entry)  # Keep empty/invalid entries

    return ipa_data


def extract_words_from_file(filename: str) -> list:
    """
        Read a file
        csv or json and extract the word list from it, the convert it in a simple Python list
    """
    word_list = []

    if not os.path.exists(filename):
        print(f'Unable to locate {filename}', file=sys.stderr)
        sys.exit(1)

    print(f"Reading data from {filename}...", file=sys.stderr)

    try:
        if filename.endswith('.json'):
            with open(filename, 'r', encoding='utf-8') as f:
                word_list = json.load(f)

        elif filename.endswith('.csv'):
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    word_list.append(row)

        else:
            print("Unsupported file format. Use '.csv' or '.json'.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f'Error processing file {filename}: {e}', file=sys.stderr)
        sys.exit(1)

    return word_list


def save_word_list_to_file(words: list, output_filename: str):
    """
        Save word list in a file for the corresponding format
    """
    if not words:
        print("No data to save.", file=sys.stderr)
        return

    # Determine the output filename based on the input filename and format
    base_name, ext = os.path.splitext(output_filename)
    output_filename = f"{base_name}_ipa{ext}"

    # Determine the format based on file extension
    fmt = ext.lower().lstrip('.')

    print(f"Saving data to {output_filename}...", file=sys.stderr)

    try:
        if fmt == 'json':
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(words, f, indent=2, ensure_ascii=False)

        elif fmt == 'csv':
            # Get all unique fieldnames from the dictionaries (including 'ipa')
            fieldnames = list(words[0].keys()) if words else []

            with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
                writer.writeheader()
                writer.writerows(words)
        elif fmt == 'dict':
            fieldnames = list(words[0].keys()) if words else []

            with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore', delimiter='\t')
                writer.writerows(words)
        else:
            print(f"Unsupported format '{fmt}' for saving.", file=sys.stderr)
            return

        print(f"Successfully saved data to {output_filename}.", file=sys.stderr)

    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
        Main function to parse arguments and run the conversion process
    """
    parser = argparse.ArgumentParser(
        description="Convert a word list file (CSV or JSON) to include IPA transcriptions using Epitran."
    )
    parser.add_argument(
        '-f', '--input_file',
        type=str,
        help='The path to the input CSV, JSON, DICT file (e.g., vocabulary.csv or vocabulary.json).'
    )

    parser.add_argument(
        '-o', '--output_file',
        type=str,
        help='The path to the output file (Can be *.csv, *.json or *.dict [MFA compatible])'
    )

    args = parser.parse_args()

    # 1. Extract words from file
    word_data = extract_words_from_file(args.input_file)

    # 2. Convert words to IPA
    ipa_data = convert_wordlist_to_ipa(word_data)

    # 3. Save the result
    save_word_list_to_file(ipa_data, args.output_file)


if __name__ == "__main__":
    main()
