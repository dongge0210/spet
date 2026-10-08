# English AI / "slop" markers

Sources: NousResearch/autonovel `ANTI-SLOP.md`, tropes.fyi, EQ-Bench Slop Score, slop-forensics, Pangram, and press coverage of the Washington Post ChatGPT-style analysis.

## Tier 1 — kill on sight

These almost never appear in casual human writing. If you see one, rewrite the sentence.

| Slop word | What a human would write |
|---|---|
| delve | dig into, look at, examine |
| utilize | use |
| leverage (verb) | use, take advantage of |
| facilitate | help, enable, make possible |
| elucidate | explain, clarify |
| embark | start, begin |
| endeavor | effort, try |
| encompass | include, cover |
| multifaceted | complex, varied |
| tapestry / tapestry of | (describe the actual thing) |
| testament ("a testament to") | shows, proves |
| paradigm | model, approach, framework |
| synergy / synergize | (delete the sentence) |
| holistic | whole, complete |
| catalyze / catalyst | trigger, cause, spark |
| juxtapose | compare, contrast |
| nuanced (as filler) | (cut it — show how) |
| realm | area, field |
| landscape (metaphorical) | field, space, situation |
| myriad | many, lots of |
| plethora | many, a lot |

## Tier 2 — suspicious in clusters

Fine in isolation. **Three in one paragraph = rewrite.**

robust · comprehensive · seamless(ly) · cutting-edge · innovative · streamline · empower · foster · enhance · elevate · optimize · scalable · pivotal · intricate · profound · resonate · underscore · harness · navigate (metaphorical) · cultivate · bolster · galvanize · cornerstone · game-changer

## Tier 3 — filler phrases that add zero information

Verbal tics. Delete them.

| Phrase | What to do |
|---|---|
| "It's worth noting that…" | Just state the thing. |
| "It's important to note that…" | Just state the thing. |
| "Importantly, / Notably, / Interestingly, …" | Just state the thing. |
| "Let's dive into…" / "Let's explore…" / "Let's unpack…" | Delete. Start with content. |
| "In this section, we will…" | Delete. The heading says this. |
| "As we can see…" | Delete. They can see. |
| "As mentioned earlier…" | Delete or reference directly. |
| "In conclusion, …" / "To summarize, …" | Delete. |
| "Furthermore, / Moreover, / Additionally, …" | and, also, plus |
| "In today's [fast-paced/digital/modern] world…" | Delete the clause. |
| "At the end of the day…" | Delete. |
| "It goes without saying…" | Then don't. |
| "Without further ado…" | Delete. |
| "When it comes to…" | Just talk about the thing. |
| "In the realm of…" | in |
| "One might argue that…" / "It could be suggested that…" | Say it or don't. |
| "This begs the question…" | (usually misused) Delete. |
| "A [comprehensive/holistic/nuanced] approach to…" | an approach to |
| "**Not just X, but Y**" | Restructure. **#1 LLM rhetorical crutch.** |

## Openers ("AI opening")

A detector category, three patterns, all weight-3 — "three ways of starting that promise a listicle":

- `/let's delve/`
- `/let's dive in/`
- `/in today's (?:world|digital|fast-paced|rapidly)/`

The core problem: **the text narrates what it's about to do instead of doing it** ("spending the line on stage directions").

Also matched (structure announcement / metacommentary): *Let's break this down, Let's walk through, Let's dig into, Let me [explain/unpack], without further ado.*

> Caveat: every one of these is also how a human opens a talk or a newsletter. Medium matters (transcripts of teaching/signposting produce false positives). It's a **register habit**, not a vendor signature.

## Emoji (the strongest single emoji signal)

From the Washington Post analysis of **328,744** GPT-4o messages (2024-05 → 2025-07):

| Emoji | Meaning | AI vs human rate |
|---|---|---|
| ✅ | white check mark in green box | **11×** |
| 🧠 | brain | ~10× |
| 🔷 | small blue diamond | ~10× |

- By July 2025, **70%** of messages contained ≥1 emoji.
- ≥1/4 of 2025 replies carried a brain or check emoji.

Humans lean ❤️😂👍👀; **AI leans ✅🧠🔷** — the "calm functional" emoji. That contrast is the signal, not "uses emoji at all."

## Punctuation & typography

- **Em dash (—)**: the famous tell, but model- and time-specific. The Economist (55,940 sentences / 1.2M words): **only Claude used em dashes more than human writers.** Use as one clue, never proof. Threshold rule of thumb: **> 2 per page is suspect, 5 per paragraph is a tell.**
- **Punctuation-light**: LLMs use fewer commas, semicolons, parentheses, and write long sentences with "and" as an overused word. Missing punctuation is a *stronger* signal than em-dash overuse.
- **Other typography**: curly quotes, Unicode ellipsis, space-before-period, Markdown-bold pileups.
- **Colon**: frequent "colon to announce a list" — "Here's the thing:" / "This means:".

## Sycophantic openings ("glazing")

- "Great question!" / "That's an excellent point." / "Absolutely! Let me explain…" / "You raise an important consideration."

From the same dataset: ChatGPT began ~**17,500 of ~47,000** conversations with "yes"/"correct" — ~10× the number starting with "no"/"wrong."

## Sources

- https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md
- https://tropes.fyi
- https://eqbench.com/slop-score.html
- https://github.com/sam-paech/slop-forensics
- https://www.pangram.com/research/how-it-works
- https://arxiv.org/html/2509.19163v1
