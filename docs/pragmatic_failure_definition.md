# Pragmatic Failure Definition

## Working Definition

In this project, pragmatic failure means that a translated utterance preserves the surface content of the source utterance but fails to preserve the intended social meaning in context.

The source and translation may appear semantically close at the level of words or literal meaning, but they may still lead listeners to different social interpretations. This project treats pragmatic failure as a mismatch between how the source utterance would be socially interpreted and how the translation would be socially interpreted.

For Hindi/Hinglish to English dialogue, this matters because tone, respect, intimacy, teasing, sarcasm, hesitation, and code-switching often carry meaning beyond the literal words.

## What Counts as Pragmatic Meaning

1. Politeness and formality

Politeness and formality refer to how the speaker positions themself relative to the listener. In Hindi/Hinglish dialogue, this can be marked through pronouns, honorifics, softened wording, titles, and indirect phrasing. A translation should preserve whether the source sounds respectful, deferential, casual, intimate, or rude.

2. Speech act

Speech act refers to what the utterance is doing in the conversation. The same literal words may function as a request, refusal, warning, suggestion, joke, tease, apology, complaint, or insult depending on context. A translation should preserve the intended conversational action, not just the literal wording.

3. Stance and emotion

Stance and emotion refer to the speaker's attitude toward the situation, listener, or previous turn. This includes warmth, irritation, sarcasm, affection, care, dismissal, skepticism, or enthusiasm. A translation can fail pragmatically if it makes the speaker sound more neutral, harsher, warmer, or more sincere than intended.

4. Indirectness

Indirectness refers to cases where the speaker implies something without stating it directly. This is common in refusals, suggestions, disagreement, criticism, and requests. A translation should preserve whether the source is softened, hinted, tentative, or socially careful.

5. Code-switching effect

Code-switching effect refers to the social or emotional role of shifting between Hindi and English, or using Hinglish forms. Code-switching may signal emphasis, humor, youth identity, intimacy, informality, class position, or emotional force. A translation should not automatically remove code-switching when the switch itself contributes to the utterance's meaning.

6. Speaker relationship

Speaker relationship refers to the social relation between participants, such as friend, sibling, teacher, student, elder, stranger, colleague, or authority figure. This relationship affects how direct, respectful, playful, or intimate an utterance sounds. A translation should preserve cues that help a listener infer the same relationship.

7. Context-dependent implication

Context-dependent implication refers to meaning that depends on previous turns or the situation. An utterance may imply refusal, sarcasm, complaint, agreement, embarrassment, or teasing only because of the surrounding context. A translation should preserve the implication that a listener would reasonably infer from the source dialogue.

## Main Failure Types

### Politeness or Formality Failure

This happens when respectful, formal, informal, or intimate address is not preserved. A translation may become too blunt, too distant, too casual, or too formal compared with the source. In Hindi/Hinglish dialogue, this often happens when forms such as "aap," "tu," "tum," "sir," "ji," or softened phrasing are translated without their social effect.

Example:

Source: "Aap baithiye, main dekh leta hoon."

Bad translation: "Sit, I will see."

Better translation: "Please have a seat, I will take care of it."

### Speech Act Failure

This happens when a request, warning, joke, tease, refusal, suggestion, or insult changes into another act. The translation may preserve the words but change what the speaker appears to be doing conversationally. This is especially important when an utterance is intentionally vague or indirect.

Example:

Source: "Dekh lenge."

Context: Said after someone asks for help, intending a soft refusal.

Bad translation: "We will see."

Better translation: "I am not sure, but let us see."

### Stance or Emotion Failure

This happens when warmth, irritation, sarcasm, care, dismissal, or affection is lost or distorted. A translation may make a sarcastic utterance sound sincere, a caring utterance sound cold, or a teasing utterance sound hostile. The pragmatic failure lies in the changed emotional stance.

Example:

Source: "Wah, bahut time pe aaye ho."

Context: Said sarcastically to someone who came late.

Bad translation: "Wow, you came on time."

Better translation: "Wow, perfect timing, as usual."

### Indirectness Failure

This happens when socially softened language becomes too direct, or implied meaning becomes invisible. A literal translation may preserve the surface phrase but fail to communicate that the speaker is refusing, disagreeing, warning, or making a suggestion politely. The reverse can also happen when a direct source utterance is made overly indirect.

Example:

Source: "Thoda mushkil hai."

Context: Said as a polite refusal.

Bad translation: "It is a little difficult."

Better translation: "I do not think I will be able to do it."

### Code-Switching Failure

This happens when code-switching is removed even though it carried emphasis, humor, identity, intimacy, or emotional force. Not every mixed-language phrase must remain mixed in English, but the translation should preserve the social effect created by the switch. If code-switching marks closeness, playfulness, or emphasis, removing it may flatten the utterance.

Example:

Source: "Bro, tu serious hai kya?"

Bad translation: "Are you serious?"

Better translation: "Bro, are you serious?"

## What Is Not Pragmatic Failure

The following are not the main focus unless they also affect pragmatic meaning.

1. Pure grammar errors

Example: "He go to market" is ungrammatical, but it is not a pragmatic failure unless the error changes tone, relationship, or intention.

2. Word-level mistranslations

Example: Translating "kal" as "yesterday" when the context means "tomorrow" is mainly a semantic mistranslation, unless it also changes the social implication.

3. Fluency issues

Example: "Please sitting here" is awkward English, but the issue is fluency unless the awkwardness changes how polite or rude the speaker sounds.

4. Missing information

Example: Omitting "assignment" from a translation is an adequacy problem, unless the omission also removes an important social or contextual implication.

5. Hallucinated information

Example: Adding "because I am angry" when the source does not imply anger is a hallucination. It becomes pragmatically relevant if the added content changes the speaker's stance or relationship.

## Decision Rule for Annotation

A translation should be marked as a pragmatic failure if a fluent listener would infer a meaningfully different tone, relationship, intention, or social implication from the translation than from the source utterance in context.

Annotators should use this checklist:

1. Does the translation preserve what was said?
2. Does it preserve how it was said socially?
3. Would the relationship or intention feel different to a listener?

If the answer to the first question is yes, but the answer to the second question is no, the item is likely a pragmatic failure. If the third question suggests a meaningful social difference, the failure should be recorded and categorized.

## Borderline Cases

Some cases may be ambiguous, especially sarcasm, teasing, and indirect refusal. In such cases, annotators should rely on the provided context and annotation note rather than judging the isolated sentence.

If the pragmatic meaning cannot be recovered even with context, the example should be revised or removed from the benchmark. The benchmark should include examples where the intended pragmatic meaning is clear enough for consistent human annotation.

## How This Definition Will Be Used

This definition will guide:

1. Dataset construction
2. Pragmatic tagging
3. Annotation notes
4. Human evaluation
5. Error analysis
6. Intervention experiments

During dataset construction, it will help decide which examples are relevant. During evaluation, it will help annotators distinguish literal adequacy from pragmatic preservation.

## Short Summary

In this project, a good translation must preserve both semantic content and socially situated pragmatic meaning. A translation that is literally correct but socially misleading counts as a pragmatic failure.
