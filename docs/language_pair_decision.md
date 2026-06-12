# Language Pair and Dataset Assumptions

## Decision

- Source language variety: Hindi/Hinglish Indian dialogue
- Target language: English
- Translation direction: Hindi/Hinglish to English

This is the initial scope for the pilot benchmark. The project will begin with a focused Hindi/Hinglish to English setting before expanding to other Indian languages, scripts, or translation directions.

## Why This Language Pair

Hindi/Hinglish to English is a strong starting point for this project for several reasons.

1. Hindi-English code-mixed dialogue is common in Indian conversational settings.

People frequently move between Hindi and English in student, family, workplace, online, and friend-group conversations. This makes Hindi/Hinglish dialogue a useful site for studying pragmatic meaning in real conversational translation.

2. Hinglish often carries social meaning through code-switching, informal address, respect markers, teasing, sarcasm, and emotional stance.

The choice between Hindi, English, and mixed forms can signal closeness, status, playfulness, irritation, or identity. These meanings may be lost if the translation treats code-switching as noise or normalizes everything into plain English.

3. English translations may preserve literal meaning while losing tone, relationship, indirectness, or social intent.

A translation can be correct at the sentence level but still make the speaker sound more rude, formal, sincere, distant, or direct than intended. This makes the language pair useful for identifying pragmatic failures that ordinary adequacy checks may miss.

4. This direction avoids starting from English, where many Indian pragmatic cues may already be absent.

Starting from Hindi/Hinglish keeps Indian conversational markers in the source side. This allows the benchmark to test whether systems preserve those cues when translating into English.

5. Several MT systems can be tested on this direction, including Google Translate, IndicTrans2, and possibly NLLB or LLM-based systems.

The direction is practical for evaluation because common commercial, open-source, and LLM-based systems can produce English outputs from Hindi or Hinglish input. This allows comparison across different system types.

## Source Variety Definition

Hindi/Hinglish Indian dialogue means dialogue that may contain:

- Hindi written in Latin script
- Hindi written in Devanagari
- English words or phrases mixed into Hindi
- Common Indian English discourse markers
- Kinship terms, respect markers, and address forms
- Student, family, workplace, and friend-group conversational settings

The first pilot should primarily use Latin-script Hinglish because it is common in online and student dialogue and easier to create consistently. This choice also keeps the first version manageable while still capturing code-mixing, informal address, politeness, teasing, and stance.

## Target Language Definition

The target language is natural English translation.

The target should preserve:

- semantic content
- speaker intention
- tone
- social relationship
- politeness or informality
- indirectness
- sarcasm, teasing, or irritation when present
- meaningful code-switching when it should remain visible

The goal is not only to produce fluent English, but to produce English that gives a listener the same social interpretation that the source would give in context.

## In-Scope Dialogue Types

1. Student and academic dialogue

This setting is useful because it often includes respect relations, requests for help, softened suggestions, deadlines, and teacher-student address. It also reflects common Hinglish use among students.

2. Friend-group dialogue

Friend-group conversations are useful for teasing, joking, sarcasm, intimacy, and informal code-switching. They help test whether translations can preserve playful or affectionate meanings without making them sound like insults.

3. Family dialogue

Family conversations include kinship terms, hierarchy, affection, irritation, and indirect requests. They are useful for evaluating whether translation preserves relationship cues such as "mummy," "papa," "didi," "bhai," or elder-younger dynamics.

4. Workplace or senior-junior dialogue

This setting is useful for formality, politeness, deference, disagreement, and indirect refusal. It can reveal whether translations preserve seniority and professional caution.

5. Service or public interaction dialogue

Service interactions involve politeness, requests, complaints, and negotiation with people who may not know each other well. They are useful for testing whether translations preserve respectful distance or frustration.

6. Online chat-style dialogue where the meaning is clear from context

Online chat dialogue is useful because Hinglish and Latin-script Hindi are common in digital communication. Such examples should be included only when the intended pragmatic meaning is clear from the provided context.

## Out-of-Scope Dialogue Types

The following are out of scope for the first version:

1. Highly dialect-specific or region-specific speech that most annotators may not understand
2. Very long conversations
3. Poetry, song lyrics, memes, and heavily stylized text
4. Sensitive private chats without consent
5. Hate speech or abusive content unless specifically needed for a controlled insult/teasing contrast
6. Speech requiring deep external cultural knowledge not provided in context

These may be added later only if the annotation guidelines and evaluator pool are expanded. The first version should prioritize examples that fluent Hindi/Hinglish and English speakers can interpret reliably with short context.

## Code-Switching Policy

Code-switching should not automatically be treated as noise.

Code-switching should be preserved or represented when it carries:

- emphasis
- humor
- identity
- intimacy
- social alignment
- irritation
- informality

Example:

Source: "Bro, tu serious hai kya?"

Bad translation: "Are you serious?"

Better translation: "Bro, are you serious?"

Example:

Source: "Mummy, please abhi mat bolo."

Bad translation: "Mother, do not speak now."

Better translation: "Mummy, please do not bring this up right now."

## Script Policy

The pilot dataset will allow:

- Latin-script Hinglish
- Devanagari Hindi
- mixed-script examples

For consistency, the first 100 pilot examples should mostly use Latin-script Hinglish. This choice reduces setup complexity and makes annotation easier, while still capturing common Indian digital dialogue.

## Context Policy

Each benchmark item should include 1 to 3 previous context turns when needed.

Context is required when the pragmatic meaning depends on:

- speaker relationship
- previous request
- prior conflict
- sarcasm trigger
- teasing setup
- refusal context
- seniority or respect relation

Examples that cannot be understood even with 1 to 3 context turns should be revised or removed. The benchmark should not rely on hidden background knowledge that annotators cannot access.

## Dataset Source Policy

The initial dataset can be built from:

1. carefully elicited examples written by fluent speakers
2. minimal pairs designed for specific pragmatic phenomena
3. open dialogue or subtitle-like data only when licensing allows
4. anonymized examples inspired by real interaction patterns, not copied private chats

Private messages should not be used unless explicit consent and anonymization are available. The project should avoid copying sensitive conversations and should prefer controlled, ethically usable examples for the pilot.

## Pilot Dataset Assumptions

- Pilot size: 100 examples
- Full first version: 300 examples
- Categories: 5 main pragmatic categories
- Each example should have a clear intended pragmatic phenomenon
- Each example should have an annotation note
- Each example should specify what the translation must preserve
- Ambiguous examples should be revised or removed
- Human evaluation should involve fluent Hindi/Hinglish and English speakers

These assumptions keep the first benchmark small enough to build carefully while supporting meaningful error analysis across pragmatic categories.

## Risks and Limitations

1. Hinglish varies strongly across regions, communities, and social groups.

The pilot cannot represent every variety of Hindi-English mixing. Examples should avoid pretending that one style of Hinglish stands for all Indian dialogue.

2. Latin-script Hindi spelling is inconsistent.

The same word may be written in many ways, which can affect both MT system behavior and annotation consistency. The dataset should use readable spellings and note variants where needed.

3. Some pragmatic meanings may be subjective.

Tone, stance, and implication can depend on the listener's background and expectations. Annotation notes should make the intended interpretation explicit.

4. Annotators may disagree about sarcasm, teasing, or indirect refusal.

These categories are especially context-sensitive. The dataset should include enough context for judgment and remove examples that produce persistent disagreement.

5. English may not always have an exact equivalent for Hindi respect markers or kinship terms.

Some cues may need to be represented through phrasing rather than direct lexical translation. Evaluation should allow functionally equivalent English renderings when they preserve the social meaning.

6. A small benchmark may reveal failures but cannot represent all Indian dialogue.

The pilot should be treated as an initial diagnostic resource, not a complete account of Indian conversational pragmatics. Later versions can broaden the languages, scripts, regions, and dialogue settings.

## Final Decision

The pilot benchmark will use Hindi/Hinglish to English dialogue, primarily in Latin-script Hinglish, with short context windows and explicit pragmatic tags. This scope is narrow enough to build carefully while still covering important Indian dialogue phenomena such as politeness, indirectness, teasing, sarcasm, and code-switching.
