import sys
import csv
import json
import time
import requests
import argparse
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# --- Configuration ---
BASE_URL = "https://www.webonary.org/fulfuldeburkina/browse/fulfulde-english/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# A small delay to be polite to the server
SCRAPE_DELAY = 1


def get_soup(url):
    try:
        print(f"Fetching: {url}", file=sys.stderr)
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        time.sleep(SCRAPE_DELAY)
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def get_letter_links(soup):
    """
        Finds all links corresponding to the starting letters (a, b, c, etc.)
        on the main browse page.
    """
    if not soup:
        return []

    letter_links = []

    # Target the container div for each letter
    letter_containers = soup.find_all('div', class_='lpTitleLetterCell')

    if letter_containers:
        letter_links = [
            (container.find('a').text, container.find('a').get('href'))
            for container in letter_containers
            if container.find('a') and container.find('a').get('href')
        ]
    else:
        # Fallback if no letter navigation is found (e.g., if we are already on a letter page)
        print("Could not find letter navigation. Proceeding with current page.", file=sys.stderr)
        canonical_link = soup.find('link', {'rel': 'canonical'})
        if canonical_link and canonical_link.get('href'):
            letter_links.append(canonical_link['href'])

    return letter_links


def get_page_urls(initial_letter_url, soup):
    """
        Finds all pagination links for a given letter.
    """
    page_urls = [initial_letter_url]

    # Target: div with id wp_page_numbers > ul > li
    pagination_list = soup.select('#wp_page_numbers ul li')

    # The links are typically inside <a> tags within the <li>
    for li in pagination_list:
        link = li.find('a')
        if link:
            href = link.get('href')
            if href and href not in page_urls:
                full_url = urljoin(initial_letter_url, href)
                page_urls.append(full_url)

    # Filter out duplicates and keep order
    return list(dict.fromkeys(page_urls))


def scrape_page(soup, include_translation):
    """
        Extracts dictionary entries from a single page of results.
    """
    if not soup:
        return []

    entries = []
    # Dictionary entries are typically contained within a larger container,
    # which is '.post'

    # Locate all entry containers. We'll iterate over these to find the content.
    # The structure suggests the content is nested under this:
    # .post -> ... -> lang_=ffm-Latn-BF
    entry_containers = soup.select('.post')

    for container in entry_containers:
        # 1. Extract Source Text (required)
        # Target: span with lang ffm-Latn-BF
        source_span = container.select_one('span', lang_='ffm-Latn-BF')
        source_text = source_span.get_text(strip=True) if source_span else "N/A"

        entry = {
            'source_text': source_text
        }

        if include_translation:
            # 2. Extract French Translation
            # Target: span.sense > span with lang fr
            fr_span = container.select_one('span.sense').select_one('span', lang_='fr')
            entry['french_translation'] = fr_span.get_text(strip=True) if fr_span else ""

            # 3. Extract English Translation
            # Target: span.sense > span  with class en
            en_span = container.select_one('span.sense').select_one('span', lang_='en')
            entry['english_translation'] = en_span.get_text(strip=True) if en_span else ""

        entries.append(entry)

    return entries


def main():
    """
        Main function to parse arguments and run the scraping process.
    """
    parser = argparse.ArgumentParser(
        description="Scrape dictionary entries from webonary.org and output as CSV or JSON."
    )
    parser.add_argument(
        '-o', '--output-format',
        choices=['csv', 'json'],
        default='csv',
        help='The format for the output data (default: csv).'
    )
    parser.add_argument(
        '--include-translation',
        action='store_true',
        help='Include French and English translations in the output (default: False/only source text).'
    )

    args = parser.parse_args()
    all_data = []
    output_filename = f"output.{args.output_format}"

    print("Starting Web Scraper...", file=sys.stderr)

    # 1. Get the main browse page to find the starting letters
    initial_soup = get_soup(BASE_URL)
    if not initial_soup:
        print("Could not retrieve initial page. Exiting.", file=sys.stderr)
        return

    # 2. Find all initial letter links
    letter_urls = get_letter_links(initial_soup)

    if not letter_urls:
        print("No letter links found. Scraper cannot proceed.", file=sys.stderr)
        return

    # 3. Loop through each starting letter
    for letter, letter_url in letter_urls:
        # Use urljoin to ensure the letter URL is absolute before fetching
        full_letter_url = urljoin(BASE_URL, letter_url)

        print(f"\n--- Scraper: Starting letter {letter} ---", file=sys.stderr)

        # A. Fetch the first page of the letter
        letter_soup = get_soup(full_letter_url)
        if not letter_soup:
            continue

        # B. Get all page URLs for this letter
        page_urls = get_page_urls(full_letter_url, letter_soup)

        # C. Loop through all pages for the current letter
        for i, page_url in enumerate(page_urls):
            print(f"Scraping page {i + 1} of {len(page_urls)} for letter {letter}...", file=sys.stderr)

            # If it's the first page, we already have the soup (letter_soup)
            if i == 0:
                current_soup = letter_soup
            else:
                current_soup = get_soup(page_url)

            if current_soup:
                page_data = scrape_page(current_soup, args.include_translation)
                all_data.extend(page_data)

    print("\n--- Scraper: Finished. Outputting data. ---", file=sys.stderr)

    # 4. Output results
    try:
        if args.output_format == 'json':
            print(f"Writing {len(all_data)} entries to {output_filename}...", file=sys.stderr)
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)

        elif args.output_format == 'csv':
            print(f"Writing {len(all_data)} entries to {output_filename}...", file=sys.stderr)
            fieldnames = ['source_text']
            if args.include_translation:
                fieldnames.extend(['french_translation', 'english_translation'])

            with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
                writer.writeheader()
                writer.writerows(all_data)

        print(f"Successfully saved data to {output_filename}.", file=sys.stderr)

    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
