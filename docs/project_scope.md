# Project Scope

## Title

Pragmatics-Preserving Machine Translation for Indian Dialogue

## Problem

Machine translation systems often preserve the surface meaning of a sentence but fail to preserve the social meaning in context. This project calls that kind of error pragmatic failure.

A pragmatic failure occurs when the translated utterance says roughly the same thing as the original, but no longer conveys the same tone, relationship, stance, implication, politeness level, indirectness, or code-switching effect.

## Research Question

Do current machine translation systems preserve pragmatic meaning in Indian dialogue?

## Initial Language Pair

Hindi/Hinglish to English.

This is the initial scope because Hindi-English code-mixed dialogue is common in Indian conversational settings and contains pragmatic signals such as respect, teasing, informality, sarcasm, and identity-marked code-switching.

## Benchmark Design

The benchmark will contain short dialogue snippets. Each item will include:

* 1 to 3 previous context turns
* source utterance
* literal meaning
* pragmatic tags
* annotation note
* what the translation must preserve

## Initial Pragmatic Categories

1. Politeness and formality
2. Teasing versus insult
3. Indirect refusal or suggestion
4. Sarcasm or irritation
5. Code-switching for emphasis, identity, intimacy, or humor

## Dataset Targets

Pilot version:

* 100 examples
* 5 categories
* 20 examples per category

Full version:

* 300 examples
* 5 categories
* 60 examples per category

## Systems to Evaluate

Initial systems:

1. Google Translate
2. IndicTrans2
3. Optional open-source baseline such as NLLB

## Evaluation Plan

The project will use human evaluation as the primary signal. Automatic checks will be used only as supporting signals.

Evaluation dimensions:

1. Semantic adequacy
2. Pragmatic preservation
3. Fluency
4. Category-specific failure type

## Expected Contribution

The project aims to produce:

1. A working definition of pragmatic failure for Indian dialogue MT
2. A small benchmark for evaluating pragmatic preservation
3. An analysis of where current MT systems fail
4. Evidence about which evaluation methods are useful
5. Initial experiments with context-aware or tag-aware translation
