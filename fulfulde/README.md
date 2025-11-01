## Fulfulde G2P Resources

This folder contains assets for producing an IPA grapheme-to-phoneme (G2P) model for Fulfulde with Montreal Forced
Aligner (MFA).

## Available Tools

- `scrape_fulfulde_from_webonary.py` – harvests lexical entries
  from [Webonary](https://www.webonary.org/fulfuldeburkina/browse/fulfulde-english/?key=ffm-Latn-BF&letter=a&lang=en) to
  bootstrap the pronunciation dictionary.
  ```commandline
    usage: scrape_fulfulde_from_webonary.py [-h] [-o {csv,json}] [--include-translation]

    Scrape dictionary entries from webonary.org and output as CSV or JSON.
    
    options:
      -h, --help            show this help message and exit
      -o {csv,json}, --output-format {csv,json}
                            The format for the output data (default: csv).
      --include-translation
                            Include French and English translations in the output (default: False/only source text).
    ```

## Suggested Workflow

1. Use the scraping script to build a raw Fulfulde word list.
2. Normalize spelling and derive IPA pronunciations for every entry using [Epitran](https://github.com/dmort27/epitran)
3. Export a tab-separated word ↔ IPA file and train the MFA G2P model.

Status: Automated lexicon collection is ready; normalization and IPA validation remain to be completed.
