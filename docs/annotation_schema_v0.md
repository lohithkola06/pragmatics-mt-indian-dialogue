# Annotation Schema v0

Each benchmark item should contain the following fields.

## Required Fields

### id

Unique example ID.

Example:

```text
hi_prag_0001
```

### source_language

The language or language variety of the source utterance.

Example:

```text
hi-en
```

### target_language

The target translation language.

Example:

```text
en
```

### context

One to three previous dialogue turns.

Each context turn should include:

* speaker
* utterance

### source_utterance

The utterance to be translated.

### literal_meaning

A rough literal explanation of the source utterance.

### pragmatic_tags

A list of pragmatic features present in the utterance.

Possible initial tags:

* POLITENESS
* FORMALITY
* TEASING
* INSULT
* INDIRECT_REFUSAL
* INDIRECT_SUGGESTION
* SARCASM
* IRRITATION
* CODE_SWITCH_EMPHASIS
* CODE_SWITCH_INTIMACY

### annotation_note

A short explanation of the pragmatic meaning.

### must_preserve

A list of pragmatic aspects that the translation should preserve.

## Example JSONL Item

```json
{
  "id": "hi_prag_0001",
  "source_language": "hi-en",
  "target_language": "en",
  "context": [
    {
      "speaker": "A",
      "utterance": "Kal assignment submit karna hai na?"
    },
    {
      "speaker": "B",
      "utterance": "Haan, par mera abhi tak complete nahi hua."
    }
  ],
  "source_utterance": "Sir se bol de, thoda time de denge shayad.",
  "literal_meaning": "Tell sir, maybe he will give some time.",
  "pragmatic_tags": ["INDIRECT_SUGGESTION", "POLITENESS"],
  "annotation_note": "The utterance is a softened suggestion, not a direct command. The reference to 'sir' marks an academic respect relation.",
  "must_preserve": [
    "The suggestion should remain indirect",
    "The respectful academic relationship should remain visible"
  ]
}
```
