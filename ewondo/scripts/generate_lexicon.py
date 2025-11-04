import requests
import sys


def process_words(input_file: str, output_file: str):
    # Open the input file and output file
    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        # Process each word (each word is expected on a separate line)
        for line in fin:
            word = line.strip()
            if not word:
                continue  # Skip empty lines

            url = f"http://127.0.0.1:2045/syll-word/{word}/"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for non-200 responses
                data = response.json()

                # Skip the word if the API indicates an error
                if data.get("error"):
                    print(f"Skipping word '{word}' due to API error.")
                    continue

                # Retrieve the AllFeats value from the response
                all_feats = data.get("data", {}).get("AllFeats", "")

                # Write the word and AllFeats value separated by a tab into the output file
                fout.write(f"{word}\t{all_feats}\n")
                print(f"Processed word: {word}")

            except Exception as e:
                print(f"Failed to process word '{word}': {e}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_words_file> <output_file.dict>")
        sys.exit(1)

    input_f = sys.argv[1]
    output_f = sys.argv[2]
    process_words(input_f, output_f)
