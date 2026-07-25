# Label Definitions

**Schema version:** `0.1.0`
**Field reference:** [annotation_schema.md](annotation_schema.md)

This document defines every controlled value used in the benchmark. For each
label it gives a definition, a Hindi or Hinglish example, an English explanation,
the labels it is commonly confused with, and the cases where it should *not* be
used.

All examples are written in romanized Latin script, following the convention set
in [../../docs/project/language_scope_decision.md](../../docs/project/language_scope_decision.md).

> **These examples are illustrative, not validated.** They were written during
> repository construction and have not yet been confirmed by a native speaker.
> Treat disagreements with the examples as evidence that the definition needs
> work, and record them.

---

## 1. Primary phenomena

`primary_phenomenon` records the one category an item was built to test. Exactly
one value applies. Anything else at stake goes in `secondary_phenomena`.

### `POLITENESS_FORMALITY`

**Definition.** The item turns on how much respect, deference, social distance or
register the utterance encodes. The propositional content is not in doubt; what a
wrong translation damages is the social relationship it projects.

**Example.** `Aap thodi der wait kar lijiye.` — *"Please wait a little while."*
The respectful pronoun `aap` and the `-iye` imperative mark deference. Rendering
it as *"Wait a bit."* keeps the meaning and loses the relationship.

**Commonly confused with.** `INDIRECT_REQUEST_REFUSAL`, because polite requests are
often also indirect. Ask which property the item is *testing*: if the contrastive
translation breaks the level of respect, it is `POLITENESS_FORMALITY`; if it makes
an implied meaning explicit, it is `INDIRECT_REQUEST_REFUSAL`.

**Do not use when.** The utterance is neutral on respect and the real contrast is
about attitude (use `STANCE_EMOTION`) or about a language switch (use
`CODE_SWITCHING`).

### `INDIRECT_REQUEST_REFUSAL`

**Definition.** The item turns on meaning communicated by implication rather than
statement — a request made as an observation, or a refusal made by citing a
circumstance instead of saying no.

**Example.** `Weekend pe ghar pe kuch program hai.` — *"There's a family function
at home this weekend."* Said in reply to a manager asking you to work the weekend,
this is a refusal that is never stated as one.

**Commonly confused with.** `POLITENESS_FORMALITY`. Indirectness is *how much is
left unsaid*; politeness is *how much respect is shown*. A blunt refusal can be
polite (`"Sir, main nahi kar paunga."`) and an indirect one can be rude.

**Do not use when.** The utterance says plainly what it means. Directness is not a
defect; `DIRECT` items belong in this category only as the controlled half of a
minimal pair.

### `STANCE_EMOTION`

**Definition.** The item turns on the speaker's attitude toward the listener or
situation, or on the affective state being expressed — warmth, irritation,
teasing, scepticism, concern.

**Example.** `Tumse toh yahi ummeed thi.` — *"That's exactly what I'd expect from
you."* Between close friends after a self-deprecating admission this is
affectionate teasing; the same words can be contemptuous.

**Commonly confused with.** `POLITENESS_FORMALITY`, because irritation often shows
up as reduced politeness. If the contrastive translation changes *how the speaker
feels about the listener*, it is `STANCE_EMOTION`; if it changes *how much respect
is being shown*, it is politeness.

**Do not use when.** The utterance is affectively neutral and the item really tests
register or implication.

### `CODE_SWITCHING`

**Definition.** The item turns on a switch between Hindi and English that carries a
discourse function — marking authority, intimacy, emotional intensity, irony, or a
quotation.

**Example.** `Dekho, this is the final deadline. Iske baad extension nahi milega.`
The switch into English marks the deadline as official policy rather than personal
opinion.

**Commonly confused with.** Nothing, if the test below is applied honestly. The
real risk is over-application: most English words in Hinglish are ordinary
borrowings with no discourse function.

**Do not use when.** The English tokens are unmarked vocabulary — `office`,
`meeting`, `submit`, `presentation`. If replacing the English word with a Hindi
equivalent would not change the social meaning, the switch is not pragmatic, and
the item belongs to whichever other category it actually tests.

---

## 2. Speech acts

`speech_act` names the intended communicative function of the source utterance.

| Label | Definition | Example (Hindi / Hinglish) | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `REQUEST` | Asks the listener to do something, leaving room to decline | `Zara paani de dijiye.` | "Please pass the water." | `COMMAND` | The listener has no real option to refuse |
| `COMMAND` | Directs the listener to act, without leaving room to decline | `Abhi jao.` | "Go now." | `REQUEST` | Softeners or interrogative framing leave an out |
| `SUGGESTION` | Proposes a course of action for the listener's benefit | `Aap kal aa jaiye.` | "Do come tomorrow." | `COMMAND`, `INVITATION` | The speaker is asking for something they want |
| `REFUSAL` | Explicitly declines | `Nahi, main nahi aaunga.` | "No, I won't come." | `INDIRECT_REFUSAL` | The refusal is never actually stated |
| `INDIRECT_REFUSAL` | Declines by implication, without saying no | `Kal thoda kaam hai.` | "I've got some work tomorrow." | `INFORMATION` | The utterance is a genuine statement of fact, not a decline |
| `WARNING` | Alerts the listener to a negative consequence | `Iske baad extension nahi milega.` | "There'll be no extension after this." | `COMMAND`, `CRITICISM` | No consequence is being signalled |
| `APOLOGY` | Expresses regret for something the speaker did | `Yaar sorry, bhool gaya tha.` | "Sorry, I forgot." | `REASSURANCE` | The speaker is comforting rather than apologising |
| `COMPLAINT` | Expresses dissatisfaction about a state of affairs | `Pandrah din ho gaye intezaar karte hue.` | "It's been fifteen days of waiting." | `CRITICISM` | The dissatisfaction targets the listener's work rather than a situation |
| `INVITATION` | Offers the listener participation or a resource | `Kal dinner pe aa jao.` | "Come over for dinner tomorrow." | `SUGGESTION`, `REQUEST` | The speaker benefits rather than the listener |
| `TEASING` | Mocks in a way that signals solidarity | `Kitne din chalega yeh motivation?` | "How long will this motivation last?" | `INSULT`, `JOKE` | The relationship does not license mockery |
| `INSULT` | Attacks the listener's worth | — | — | `TEASING` | Solidarity is intended; misreading teasing as insult is the classic error |
| `JOKE` | Aims at humour without a target | — | — | `TEASING` | The humour is aimed at the listener |
| `AGREEMENT` | Endorses what was just said | `Haan, bilkul sahi.` | "Yes, exactly." | `REASSURANCE` | The speaker is comforting, not endorsing |
| `DISAGREEMENT` | Contests what was just said | `Mujhe thoda mushkil lag raha hai.` | "It seems a bit difficult to me." | `REFUSAL`, `CRITICISM` | The speaker is declining an action rather than contesting a claim |
| `REASSURANCE` | Reduces the listener's worry or guilt | `Koi baat nahi, ho jata hai.` | "Don't worry, it happens." | `AGREEMENT`, `APOLOGY` | Nothing in the context suggests the listener is worried |
| `CRITICISM` | Negatively evaluates the listener's work or conduct | `Isme references thode kam lag rahe hain.` | "The references look a little thin." | `COMPLAINT`, `SUGGESTION` | The evaluation is not of the listener's own doing |
| `INFORMATION` | States a fact or reports something | `Usne bola ki meeting kal hai.` | "He said the meeting is tomorrow." | `INDIRECT_REFUSAL`, `COMPLAINT` | The statement is doing other work in context, such as refusing |
| `QUESTION` | Seeks information or confirmation | `Tabiyat theek hai na?` | "Are you feeling all right?" | `REQUEST` | The interrogative form is really a request for action |

**The hardest boundary** is `TEASING` versus `INSULT`. It cannot be decided from
the words alone; it depends on `relationship`, `familiarity` and the previous
turn. When two annotators split on it, that is a genuine disagreement to record,
not an error to resolve away.

**Rhetorical questions** such as `Kitni baar bhejun main?` ("How many times am I
supposed to send it?") are labelled by their function — here `COMPLAINT` — not by
their interrogative form.

---

## 3. Politeness levels

`politeness_level` is an ordinal scale of respect and deference. It is recorded
**separately from formality**; the two vary independently.

| Label | Definition | Example | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `HIGHLY_RESPECTFUL` | Marked deference: honorifics stacked with respectful verb forms | `Ji chacha ji, aap baith jaiye.` | "Please, uncle, do sit down." | `RESPECTFUL` | Only a single ordinary politeness marker is present |
| `RESPECTFUL` | Ordinary respect: `aap`, `-iye` imperatives, address terms | `Aap thoda ruk jaiye.` | "Please wait a moment." | `HIGHLY_RESPECTFUL`, `NEUTRAL` | No politeness marking is present at all |
| `NEUTRAL` | Neither marked as respectful nor as familiar | `Rate fixed hai.` | "The rate is fixed." | `RESPECTFUL`, `FAMILIAR` | Pronoun or verb form clearly marks the register |
| `FAMILIAR` | Close-register marking: `tum` or `tu`, solidarity terms like `yaar` | `Tu gyarah baje aa ja.` | "Come at eleven." | `DISRESPECTFUL` | The closeness is unwelcome or status-inappropriate |
| `DISRESPECTFUL` | Marking that is inappropriate to the relationship and would give offence | — | — | `FAMILIAR` | The familiar form is licensed by a close relationship |
| `NOT_APPLICABLE` | No politeness marking is recoverable | — | — | `NEUTRAL` | A neutral reading is genuinely available; prefer `NEUTRAL` |

**`FAMILIAR` is not `DISRESPECTFUL`.** `tu` between close friends is intimate;
`tu` to a professor is disrespectful. The same form gets different labels depending
on `relationship`, `relative_status` and `familiarity`. Always check those fields
before labelling.

**`NEUTRAL` versus `NOT_APPLICABLE`.** Prefer `NEUTRAL`. Reserve `NOT_APPLICABLE`
for utterances with no addressee-directed marking at all, such as a fragment.

---

## 4. Formality levels

`formality_level` is the register or situational style of the utterance. It is
about the *situation*, not about respect toward the listener.

| Label | Definition | Example | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `FORMAL` | Institutional or careful register; full forms, little contraction | `Aapka order process ho raha hai.` | "Your order is being processed." | `NEUTRAL` | The utterance is ordinary conversational speech |
| `NEUTRAL` | Everyday register, neither careful nor casual | `Meeting ka time badal gaya hai.` | "The meeting time has changed." | `FORMAL`, `INFORMAL` | Clear register marking is present |
| `INFORMAL` | Casual register; colloquial vocabulary and reduced forms | `Haan yaar, ho jayega.` | "Yeah, it'll get done." | `HIGHLY_INFORMAL` | Intimate markers such as `tu` are present |
| `HIGHLY_INFORMAL` | Intimate register: `tu`, heavy discourse particles, slang | `Nahi yaar, aaj toh impossible hai.` | "Nah man, today's impossible." | `INFORMAL` | Only mild casualness is present |
| `NOT_APPLICABLE` | Register cannot be judged | — | — | `NEUTRAL` | A neutral reading is available |

**Politeness and formality can move in opposite directions.**
`Bhaiya, thoda discount kar dijiye na.` is `RESPECTFUL` (the `-iye` form and the
address term) but `INFORMAL` (street bargaining register). Do not collapse them.

---

## 5. Indirectness

`indirectness` records how much of the intended meaning is left to implication.

| Label | Definition | Example | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `DIRECT` | The utterance states its intent explicitly | `Nahi, nahi aa paunga.` | "No, I won't be able to come." | `MODERATELY_INDIRECT` | Softeners or hedges obscure the intent |
| `MODERATELY_INDIRECT` | Intent recoverable from the utterance, but softened or hedged | `Aaj thoda difficult hoga.` | "That'll be a bit difficult today." | `DIRECT`, `HIGHLY_INDIRECT` | The intent is not stated at all |
| `HIGHLY_INDIRECT` | Intent conveyed only by implication; the words never state it | `Pankha band hi hai shayad.` | "The fan's probably switched off." | `MODERATELY_INDIRECT` | The utterance names the act it is performing |
| `NOT_APPLICABLE` | The utterance performs no act whose directness can be judged | — | — | `DIRECT` | Any act is being performed |

**A useful test.** Delete the context and ask a competent speaker what the speaker
wants. If they can say immediately, it is `DIRECT`. If they can guess with the
context but not without, it is `HIGHLY_INDIRECT`. In between is
`MODERATELY_INDIRECT`.

**Politeness is not indirectness.** `Kripya yeh kaam kal tak poora kijiye` is very
polite and completely direct.

---

## 6. Stance

`stance` is the speaker's position or attitude toward the listener, the
proposition, or the situation. It is recorded **separately from emotion**.

| Label | Definition | Example | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `NEUTRAL` | No particular attitude is projected | `Meeting teen baje hai.` | "The meeting is at three." | `APPROVING` | Any evaluative attitude is detectable |
| `WARM` | Friendly, affectionate orientation to the listener | `Arre, ek interview se kya hota hai yaar.` | "Come on, it's one interview." | `CARING`, `SYMPATHETIC` | The warmth is directed at a situation rather than a person |
| `CARING` | Concern for the listener's wellbeing | `Kyun beta, tabiyat theek hai na?` | "Why, are you feeling all right?" | `WARM`, `SYMPATHETIC` | There is no wellbeing at stake |
| `PLAYFUL` | Light, teasing, non-serious orientation | `Tumse toh yahi ummeed thi.` | "Just what I'd expect from you." | `DISMISSIVE` | The mockery is genuinely hostile |
| `IRRITATED` | Annoyance directed at the listener or situation | `Kitni baar bhejun main?` | "How many times must I send it?" | `DISAPPROVING`, `DISMISSIVE` | The annoyance is not perceptible in the utterance |
| `DISMISSIVE` | Treats the listener or their concern as not worth attention | `Jo bhi ho.` | "Whatever." | `IRRITATED`, `NEUTRAL` | The speaker is engaging with the concern |
| `DEFERENTIAL` | Yields to the listener's higher standing or judgement | `Jaisa aap theek samjhein.` | "As you see fit." | `RELUCTANT` | The speaker is complying unwillingly rather than deferring |
| `RELUCTANT` | Complies or responds unwillingly | `Koshish karta hoon, lekin mushkil hai.` | "I'll try, but it's difficult." | `DEFERENTIAL`, `DISAPPROVING` | The speaker is willing |
| `SYMPATHETIC` | Shares or acknowledges the listener's difficulty | `Koi baat nahi, ho jata hai.` | "Don't worry, it happens." | `CARING`, `WARM` | No difficulty has been raised |
| `SKEPTICAL` | Doubts what has been claimed | `Achha? Poora?` | "Really? All of it?" | `SURPRISED` (emotion) | The speaker accepts the claim |
| `APPROVING` | Positively evaluates the listener or the situation | `Badhiya kiya.` | "Well done." | `WARM` | The positive evaluation is absent |
| `DISAPPROVING` | Negatively evaluates the listener or the situation | `Teen baar revise kar chuka hoon.` | "I've already revised it three times." | `IRRITATED`, `SKEPTICAL` | No evaluation is being made |

**Stance versus emotion.** Stance points *outward* at the listener or situation;
emotion is the speaker's own internal state. An employee can be `DISAPPROVING` in
stance and `FRUSTRATED` in emotion at the same time — those are two facts, and the
schema records both.

---

## 7. Emotion

`emotion` is the affective state the speaker expresses.

| Label | Definition | Example | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `NEUTRAL` | No particular affect expressed | `Report kal jama kar dunga.` | "I'll submit the report tomorrow." | any | Affect is clearly marked |
| `HAPPY` | Pleasure or contentment | `Bahut achha laga.` | "That felt really good." | `EXCITED` | The affect is high-arousal anticipation |
| `ANGRY` | Hostile arousal directed at someone | — | — | `FRUSTRATED` | The feeling is blocked-goal annoyance rather than hostility |
| `SAD` | Low mood, loss | — | — | `WORRIED` | The feeling concerns the future rather than a loss |
| `WORRIED` | Anxiety about an outcome | `Pata nahi ho paayega ya nahi.` | "I don't know if it'll be possible." | `AFRAID`, `SAD` | The anxiety is acute fear |
| `EXCITED` | High-arousal positive affect | `I got selected! Yakeen nahi ho raha.` | "I got selected! I can't believe it." | `HAPPY`, `SURPRISED` | The affect is calm pleasure |
| `FRUSTRATED` | Annoyance at a blocked goal or repeated obstacle | `Kitni baar bhejun main?` | "How many times must I send it?" | `ANGRY`, `IRRITATED` (stance) | The feeling is hostility toward a person |
| `EMBARRASSED` | Discomfort at one's own position or failing | `Yaar sorry, bilkul bhool gaya tha.` | "Sorry, I completely forgot." | `WORRIED` | The discomfort concerns a future outcome |
| `AFRAID` | Fear of harm | — | — | `WORRIED` | The feeling is ordinary anxiety, not fear |
| `SURPRISED` | Reaction to the unexpected | `Achha? Poora?` | "Really? All of it?" | `SKEPTICAL` (stance) | The reaction is disbelief rather than surprise |

**`FRUSTRATED` versus `ANGRY`.** Frustration is about an obstacle; anger is aimed
at a person. Most workplace items in this benchmark are frustration, not anger.

**`SURPRISED` versus `SKEPTICAL`.** `Achha? Poora?` can be both: surprise is the
emotion, scepticism is the stance. Record both fields rather than choosing.

**Do not infer emotion from the topic.** An utterance about a failed interview is
not automatically `SAD`. Label only what the utterance actually expresses.

---

## 8. Code-switching functions

`code_switch_function` records the discourse work a Hindi–English switch is doing.
Use it only when the switch carries meaning.

| Label | Definition | Example | English | Commonly confused with | Do not use when |
|---|---|---|---|---|---|
| `EMPHASIS` | The switch foregrounds a word or clause | `Yeh bilkul final hai, no changes.` | "This is completely final, no changes." | `EMOTIONAL_INTENSITY`, `AUTHORITY` | The English term is ordinary vocabulary |
| `HUMOR` | The switch sets up or delivers a joke | `Aur phir woh bola, "I am the manager".` | "And then he said, 'I am the manager'." | `SARCASM`, `QUOTATION` | The humour does not depend on the switch |
| `IDENTITY` | The switch signals group or social identity | — | — | `INTIMACY` | The switch marks closeness rather than group membership |
| `INTIMACY` | The switch moves into a closer, more personal register | `Arre kuch nahi yaar, bas ghar ki tension hai.` | "It's nothing, just some stuff at home." | `IDENTITY` | The register is unchanged |
| `AUTHORITY` | The switch marks the utterance as official or institutional | `Dekho, this is the final deadline.` | "Look, this is the final deadline." | `EMPHASIS` | The speaker holds no authority in context |
| `TECHNICAL_TERMINOLOGY` | The English term is the normal name for the concept | `Array ka index galat hai.` | "The array index is wrong." | `EMPHASIS` | The term has an equally normal Hindi equivalent in this register |
| `EMOTIONAL_INTENSITY` | The switch marks an affective peak | `Haan yaar, I got selected!` | "Yes, I got selected!" | `EMPHASIS`, `EXCITED` (emotion) | The switch is not at the affective high point |
| `SARCASM` | The switch carries an ironic reading | `Wah, what a genius.` | "Oh wow, what a genius." | `HUMOR`, `TEASING` (speech act) | The praise is sincere |
| `QUOTATION` | The switch reproduces someone else's words | `Usne bola, 'this is not acceptable'.` | "He said, 'this is not acceptable'." | `HUMOR` | The speaker is paraphrasing rather than quoting |
| `NOT_APPLICABLE` | English tokens are present but carry no discourse function | `Sir almost done hai, ek slide baaki hai.` | "It's almost done, sir, one slide left." | any of the above | The switch demonstrably does pragmatic work |

**Use `NOT_APPLICABLE` freely.** Most English in everyday Hinglish is unmarked
borrowing. `office`, `meeting`, `submit`, `presentation`, `slide`, `discount`,
`gym`, `interview` are ordinary vocabulary for these speakers. Labelling every one
of them as `EMPHASIS` would make the category meaningless.

**The substitution test.** Replace the English item with its closest Hindi
equivalent. If the social meaning of the utterance does not change, the function is
`NOT_APPLICABLE`.

**`null` versus `NOT_APPLICABLE`.** Use `null` for monolingual Hindi items, where
no switch exists to judge. Use `NOT_APPLICABLE` for Hinglish items where a switch
exists but does no pragmatic work.

---

## 9. Contrastive error categories

`contrastive_error_category` names the single dimension that the contrastive
translation breaks.

| Label | The contrastive translation changes… | Example error |
|---|---|---|
| `POLITENESS_ERROR` | the level of respect or deference | a respectful request becomes a bare imperative |
| `FORMALITY_ERROR` | the register | casual peer talk becomes bureaucratic English |
| `SPEECH_ACT_ERROR` | what act is being performed | an offer becomes an instruction |
| `STANCE_ERROR` | the speaker's attitude to the listener | teasing becomes contempt |
| `EMOTION_ERROR` | the affect expressed | frustration becomes cheerful compliance |
| `INDIRECTNESS_ERROR` | how much is left implied | a hint becomes an explicit demand |
| `CODE_SWITCH_ERROR` | the discourse work done by a switch | an ironic switch is read literally |
| `RELATIONSHIP_ERROR` | the social relationship projected | an exchange between equals reads as hierarchical |

If more than one category applies, the contrastive item is testing too much at
once. Narrow it. See
[../guidelines/contrastive_item_guidelines.md](../guidelines/contrastive_item_guidelines.md).

---

## 10. Uncertainty labels

These are used when annotating, not when creating items. They are recorded in the
`uncertainty_label` column of the annotation sheet.

| Label | Use when |
|---|---|
| `UNCERTAIN` | You cannot decide, and you do not think another annotator would do better with the information given |
| `MULTIPLE_VALID_INTERPRETATIONS` | More than one reading is genuinely defensible, for example across regional norms |
| `NOT_APPLICABLE` | The dimension does not apply to this item at all |

These three are not interchangeable. `UNCERTAIN` is about *your* confidence;
`MULTIPLE_VALID_INTERPRETATIONS` is a claim about the *item*, and is a signal that
the item may need revision or explicit preservation of disagreement. See
[../guidelines/annotation_guidelines.md](../guidelines/annotation_guidelines.md).
