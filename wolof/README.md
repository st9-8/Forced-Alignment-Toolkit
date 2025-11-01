## Wolof G2P Resources

This folder documents the steps for preparing an IPA grapheme-to-phoneme (G2P) model for Wolof with Montreal Forced Aligner (MFA).

## Current Focus
- Reuse the G2P model published with the [Kallaama speech dataset](https://github.com/gauthelo/kallaama-speech-dataset/tree/master/data/lexicons/wolof).
- Validate the imported pronunciations against project word lists.
- Package the dictionary for downstream forced alignment experiments.

## Suggested Workflow
1. Download the Wolof MFA G2P resources from the Kallaama repository and place them here.
2. Spot-check pronunciations and adjust any entries needed for our datasets.
3. Train or fine-tune the MFA G2P model if new lexicon data becomes available.

Status: External Wolof G2P resources identified; evaluation of their coverage is the next step.
