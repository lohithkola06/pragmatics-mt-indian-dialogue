# Pragmatics-Preserving MT for Indian Dialogue

This project studies whether machine translation systems preserve pragmatic meaning in Indian dialogue.

The main focus is not only whether a translation preserves literal meaning, but whether it also preserves the speaker's social meaning in context, including tone, politeness, formality, indirectness, stance, teasing, sarcasm, and code-switching.

## Research Question

Do current machine translation systems preserve pragmatic meaning in Indian dialogue, especially politeness, indirectness, stance, teasing, and code-switching?

## Initial Scope

* Source language: Hindi/Hinglish dialogue
* Target language: English
* Dataset type: Short dialogue snippets with 1 to 3 previous context turns
* Initial benchmark size: 100 pilot examples
* Full benchmark target: 300 examples
* Evaluation: Human evaluation plus automatic checks

## Core Pragmatic Categories

1. Politeness and formality
2. Teasing versus insult
3. Indirect refusal or suggestion
4. Sarcasm or irritation
5. Code-switching for emphasis, identity, intimacy, or humor

## Planned Pipeline

1. Define pragmatic failure
2. Build a small dialogue benchmark
3. Add pragmatic tags and annotation notes
4. Run machine translation systems
5. Evaluate whether translations preserve pragmatic meaning
6. Analyze failures by category
7. Test simple interventions such as context-aware translation

## Repository Structure

```text
docs/           Project scope, annotation guidelines, notes
data/           Raw, pilot, and processed benchmark data
annotations/    Human annotation files
outputs/        MT system outputs
eval/           Evaluation results and score tables
scripts/        Data processing and evaluation scripts
paper/          Final report or paper draft
```
