## Forced Alignment Toolkit for Low-Resource Languages

This repository gathers tools and datasets to support building forced alignment systems for low-resource languages. Our
current focus is producing grapheme-to-phoneme (G2P) models in IPA
using [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/).

## Languages

- Baca — collecting and curating lexicon data prior to MFA G2P training.
- Ewondo — preparing orthographic resources and cleaning pronunciation data.
- Fulfulde —
  scraping [Webonary](https://www.webonary.org/fulfuldeburkina/browse/fulfulde-english/?key=ffm-Latn-BF&letter=a&lang=en)
  lexicons and converting entries to IPA.
- Wolof — adapting an existing MFA-compatible G2P model from
  the [Kallaama dataset](https://github.com/gauthelo/kallaama-speech-dataset/tree/master/data/lexicons/wolof).

## Getting Started

1. Install Montreal Forced Aligner following the official instructions.
2. Review each language folder for data preparation notes and scripts.
3. Use MFA to train or adapt language-specific IPA G2P models as resources become available.

## Roadmap

- Gather and normalize lexicons for every target language.
- Train and validate MFA G2P models.
- Package pronunciation dictionaries for downstream forced alignment experiments.
