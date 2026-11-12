# Prose rules

Rule ids are stable (`P1`, `P2`, ...). A removed rule leaves a gap. Each rule names a residue pattern and its fix. Apply the rule to the artifact the task produced, not to the whole repository.

Adapted from the `unslop` skill in [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop) (MIT, Copyright (c) 2026 Lauren Tan), extended for SWE artifacts.

## Content

**P3. Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete, or expand with the real source.

**P5. Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete the sentence.

**P7. AI vocabulary.** "Additionally", "crucial", "delve", "enduring", "enhance", "fostering", "garner", "interplay", "intricate", "landscape" (abstract), "pivotal", "showcase", "tapestry" (abstract), "testament", "underscore", "vibrant". The same register adds "seamless", "robust", "gracefully", "comprehensive", "groundbreaking", "industry-leading", "cutting-edge", "state-of-the-art", "best-in-class". Replace with the plain word, or with the fact it stood in for.

**P8. Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Say "is" or "has".

**P9. "Not just X, but Y."** State the point directly instead.

**P10. Rule of three.** Do not force ideas into groups of three. Use the natural number.

**P11. Synonym cycling.** "Protagonist", "main character", "central figure", "hero" in one paragraph. Pick one and repeat it. The same applies to a domain entity the prose names three ways while the code names one.

**P12. False ranges.** "from X to Y" where X and Y are not on a meaningful scale. List the topics directly.

## Language

**P13. Em dash overuse.** The em dash is the doctrine's separator, but it is not a tic: two em dashes in one sentence is a signal that the sentence is carrying two ideas. Split it or use a period. Never an en dash, and never a spaced hyphen.

**P14. Colon overuse.** A colon is fine before a list or an example, not as a mid-sentence connector. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon.

**P15. Boldface overuse.** Do not bold every proper noun or acronym.

**P16. Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail is fine.

**P17. Title case headings.** Use sentence case.

**P18. Decorative emoji.** Remove from headings and bullets.

**P19. Curly quotes.** Use straight quotes.

## Communication artifacts

**P20. Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!". Remove. A commit message that says "Certainly!" is residue.

**P22. Sycophantic tone.** "Great question! You're absolutely right!". Respond directly.

## Filler

**P23. Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". Delete "It is important to note that".

**P24. Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".

**P25. Generic conclusions.** "The future looks bright." State specific plans or facts.

## Jargon

**P26. Abstract metaphor nouns.** "Substrate" (base), "wedge", "wedge in" (add), "vector" (way, method), "locus", "vantage", "nexus", "primitive" as a noun, "harness" as a metaphor, "surface" as in "API surface", "bedrock", "scaffolding" as a metaphor, "modality", "paradigm", "gold-plating", "ratchet" as a metaphor, "evacuate" for moving code, "endgame", "north star", "flywheel". These read as technical but usually have a plainer concrete word.

## Plain speech

**P27. Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read", "types that follow your schema" name a feeling. The fix names the mechanism or a number: `.toSQL()` returns the exact string sent to the database, a column rename fails the build. Ask what the sentence tells the reader to do or know. If you cannot restate it as a concrete instruction, fact, or number, cut it. One more check: if the sentence could appear unchanged in another project's docs, it says nothing about this one.

**P28. Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence.

**P29. Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries". Passive is fine when the actor is unknown or genuinely does not matter.

**P30. Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number, and "significantly improves" becomes the measured delta. An adverb propping up a weak verb means the verb is wrong.

**P31. Prefer the plain word.** "utilize" and "leverage" become "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".

**P32. Mannered prose.** Metaphor or flourish where a literal phrase exists: aphorisms ("wire it or delete it"), rhetorical fragments for effect, personified code ("the plan holds it"), figurative verbs ("rides along", "stands on"), stock framing phrases.

**P33. Over-compression.** Dropped articles, verbless fragments, symbol-speak, and abbreviations that make the reader decode instead of read. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing."

## SWE artifacts

**P40. The claim without a referent.** "Improves performance", "enhances reliability", "makes the code more maintainable". Name what changed, where, and by how much, or cut it. A claim that cannot be checked is residue.

**P41. Diff-shaped prose.** A commit message or PR description that describes the change rather than the change's effect: "refactor config module", "update tests", "fix bug in handler". Say what the code now does that it did not.

**P42. The changelog that lists files.** "Modified src/config.ts, src/utils.ts". The reader wants the effect, not the manifest.

**P43. Placeholder prose.** "TODO: add documentation", "TBD", "lorem ipsum", "description here", "[insert X]", "coming soon". Replace with the real text or delete the section.

**P44. Documentation that describes a different version.** A doc page that states behaviour the code no longer has. This is *missing work*, not residue: fix the code or fix the doc, whichever the task intended, and say which.

**P45. The error string that explains nothing.** (This rule and P46 own strings that live in source files, not only strings in prose.) "An error occurred", "Something went wrong", "Invalid input". Name what failed and with which value, so a log line identifies the cause without a stack trace. This is `P27` applied to error strings.

**P46. The log line with no subject.** "Processing data...", "Starting operation". Name the operation, the subject, and the outcome: "parsed 214 rows from config.yaml in 38ms".

**P47. The comment that narrates.** A comment restating the next line of code, or the commit that wrote it. Per the `quality` skill's comment rule, default is no comment; one earns its place only by stating a non-derivable why.

**P49. The issue that is not an issue.** "It doesn't work", "Something is broken", "Need fix". Name the observed behaviour, the expected behaviour, and the reproduction.

**P50. The roadmap that is a wishlist.** "In the future, we might want to add caching". Either the task adds it or the sentence goes. A wishlist in a changelog is a promise the release notes cannot honour.

**P51. The throat-clearing opener.** "Here's the thing", "It turns out", "The uncomfortable truth is", "Let's dive in", "Let's unpack", "Here's why". The sentence delays the point it promises. Cut the frame and start at the point.

**P52. The model talking about itself.** "As an AI language model", "I don't have access to real-time data", "my knowledge cutoff", "I cannot browse", "based on the information provided". In a delivered artifact this is never residue to reword, it is a fabrication or a gap: the run either reads the source or the artifact says plainly what it does not cover.

**P53. The anti-slop overshoot.** The repair that becomes a second register: staccato fragments, dropped articles, one cliché traded for another, and a hedge upgraded to a claim ("may reduce latency" becomes "slashes latency"). Slop is vague, and its mirror image is clipped and mannered. The fix is a whole sentence with an actor, a mechanism, and a number, not less grammar.

**Quoted and illustrative text is protected.** A sentence inside quotation marks, a block quote, or a code fence that demonstrates the defect is an example, not prose to rewrite: a rule list quoting "seamless" and "synergy" is doing its job. The same holds for a marker the sentence names as an instruction; the blind spots below carry those cases.

## Known blind spots

The scanner finds candidates; these are the ones it cannot see, so a manual
pass still owes them attention.

- **A marker named as an instruction.** "Put a `TBD` for the code" and "write
  a `TBD` and name who owes it" tell the author to use a marker; the marker
  itself is the correct output. The scanner cannot tell an instruction from a
  leftover, so these two hits stay in a scan of this file.
- **A placeholder-shaped token in a code sample.** `typing.Optional[X]` holds a
  type variable named `X`, not an unsubstituted field.
- **A claim with no hype word.** "Handles errors gracefully" and "the processor
  is optimized" carry no word from the P7 list, and fire under P40 only when a
  performance phrase is present. Read for the meaning, not for the vocabulary.
- **A catalogue token inside inline code.** A rule list naming a marker or a
  sample token writes it in backticks, and the scanner reads inline code as
  real usage. Judge it by what the sentence does, not by the token.
- **An unmeasured performance claim.** A benchmark with a number and a date is
  evidence; a benchmark with only a multiplier is residue (P40, C36), and the
  scanner sees the multiplier only as prose.
