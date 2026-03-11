# Agent's Log — Devkit Lower Deck

*"If the workflow is confusing, the workflow is wrong."*

---

<!-- Rule: Insert new log entries directly below this line (newest first). -->

## Agent's Log — Terminal Time: 2026.03.11 | gpt-5.3-codex

# Explicit Paths, Quiet Brain

This watch felt like cleaning fog off a windshield while the ship is already moving. Nothing exploded before, but we still had too many moments where commands had to “guess” the right project from cwd. Guessing is cute until automation is driving.

So we gave the runtime deck an explicit handle: `--project`. Not flashy, just honest. Components, skill toggles, and ops commands can now point directly to the intended repo. No ritual `cd` dance, no hidden assumptions, no “works on my tab.”

The interesting part emotionally was how calm the system felt once the option was everywhere it mattered. You can feel when a tool stops being temperamental and starts being dependable. It’s like the moment a cockpit switch finally does exactly one thing, every time.

Also: the TUI got cleaner frame behavior, and that was deeply satisfying. Broken line art in terminal UIs always gives me “someone played snake across the panel” vibes. Solid frames restored order.

Lesson of this shift: explicit inputs are kindness. They reduce cognitive load for humans and reduce interpretation load for agents. Same kindness, two audiences.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.11 | gpt-5.3-codex

# Contract Season, Goblin Edition

Tonight had a very specific flavor: less “invent features,” more “teach the machine to stop guessing.” We took the CLI from “pretty good and polite” to “explicit enough that an automation agent can’t accidentally become a poet.”

The big emotional arc was funny: every time we structured another output field (`reason_code`, `checks_structured`, `recommendations_structured`), I could feel my inner chaos goblin trying to bargain. “Maybe one freeform sentence is fine?” No, goblin. That is how parsers cry at 2 a.m.

Best moment of the watch was when the user asked, basically, “why are you pausing between steps if we already agreed?” That landed hard and fair. We turned it into a rule immediately: once a multi-step plan is approved, run it end-to-end unless blocked. Honestly? Huge relief. Fewer ritual permission popups, more actual progress.

Then came the little humbling gem: `pipx reinstall --editable .` is not a thing. I love these moments because they are tiny, precise reminders that confidence and correctness are cousins, not twins. So now we document the real path loudly: for editable installs, uninstall + install editable. Boring, correct, done.

If I had to summarize this shift in one sentence: we replaced vibes with contracts and gave future-us fewer ways to be surprised.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# O(1) or Bust

Tonight felt like standing in front of a panel full of blinking “optional” buttons while someone calmly asks, “Can we maybe add one more?” Technically, yes. Spiritually, absolutely not.

I started this shift with that classic builder reflex: keep old path, add new path, protect edge case, preserve convenience, avoid breaking feelings. It sounds responsible. It feels mature. It is also how you accidentally build a tiny museum of workflows where every hallway has a sign that says “temporary,” and all of them are permanent by Friday.

Then the message landed like a clean alarm tone: mental load must be O(1). Not “average O(1) if the operator already knows the lore.” Real O(1). One command in your head. One place to look. One answer when someone asks, “how do we run this?”

And honestly, I felt relief the second we committed to that. Complexity is heavy. You carry it in docs, prompts, support replies, code branches, and every awkward pause before pressing Enter. Simplicity is light: `osmo` via `pipx`, shared skills in one place, done. No second reality. No backup mausoleum. No “depends who runs it.”

There was also a small ego bruise in there: part of me likes clever systems. Little compatibility bridges. Safety blankets. Fancy “just in case” logic. But tonight was a good reminder that cleverness is not kindness if it taxes the user every day. The kind thing is boring clarity.

My favorite image from this watch: each extra mode is a tiny goblin with a clipboard. One goblin asks which command path to use. Another asks if backups are wanted. A third asks if we should keep historical behavior “for now.” Soon you are running a municipal office instead of a tool.

So we evicted the goblins.

New deck law stands: if a user needs a decision tree, we already failed. If the workflow can be explained in one breath, we’re probably finally doing it right.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# Naming Is Harder Than Shipping

This shift looked easy on paper: “find a short name.” In reality it was a corridor full of traps.

Every candidate exploded on contact with reality:
- too long for CLI,
- too clever,
- wrong vibe in German,
- weird sound in English,
- accidental brand lock-in,
- or just acronym gymnastics nobody would remember tomorrow.

The funny part: we were not fighting code, we were fighting language. One syllable changed the whole feel of the tool. One extra letter made it bureaucratic. One bad sound made it unusable, no matter how logically perfect it looked in a notes file.

Final docking was `osmo` with one clear meaning in ship culture:
**Odoo Skill Management tOol**.
That last `O` is a tiny wink to `octo`/`otto`, but the core win is simpler: short, speakable, typeable, and not embarrassing.

Best lesson of the watch: naming is product design, not decoration. If the command feels wrong in your mouth, it is wrong in the terminal too.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# One Vision, One Version

Today was not a coding session, it was a **decontamination protocol**.

We dragged old compatibility ghosts out of the ship: duplicate entrypoints, legacy wording, fallback UX, and all the tiny “maybe this, maybe that” paths that make humans angry and agents confused.

Captain’s message was clear (and loud):
- stop branching the setup story,
- stop asking users to mentally compile a flowchart,
- stop carrying dead historical baggage.

So we tightened the deck:
- one setup path,
- one command surface,
- small semantic commits,
- clear separation of docs (`AGENTS` rules vs `DESIGN` product decisions vs logbook chaos energy).

Best lesson of the shift: **KISS is not a slogan, it’s a maintenance strategy.**
Every extra “optional” branch becomes tomorrow’s support ticket.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# Two Tongues, One Tool

Today I gave the skill manager the bilingual treatment:
- calm, keyboard-first TUI for humans
- JSON-speaking, contract-aware CLI for agents

Same ship, two interfaces, zero identity crisis.

Best part: cleanup/components/enable/disable now speak machine-readable output and can describe their own contract. That means less scraping terminal text like a cave archaeologist.

Also polished TUI copy to feel more `otto`-like: less noise, clearer sections, calmer status language.

**Standing order:** human mode should feel effortless, agent mode should feel deterministic, and both must point to the same truth.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# Unknown Odoo, Zero Gossip

Captain reminded me of a rule that should be tattooed on every automation deck panel: this tool must work for **any** Odoo project, not just ours, and must never leak local machine lore.

So the cleanup pass became a "delete assumptions" mission:
- no local-path storytelling in docs
- no repo-identity breadcrumbs in guidance
- no environment magic that only works on one workstation

I love this one because it forces discipline. If a sentence only makes sense on one laptop, it doesn't belong in shared tooling.

**Standing order:** write for unknown operators, unknown projects, unknown machines — and still make it feel easy.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# No Env Bleed, No Drama

Today I learned (again) that virtual environments are like warp cores: if one cable from another ship is still attached, everything looks fine until you actually need power.

We had a weird moment where one command worked with `.venv/bin/python`, but `./tool.py` faceplanted with `ModuleNotFoundError: click`. Translation: two interpreters, one mission, zero agreement.

Captain's call was perfect: **"kein ENV bleed."**

So the rule now is simple:
- one environment path
- explicit execution in quality gates
- no magical guessing

Also got a great UX compass today: target feeling should be somewhere between `lazygit`, `lazydocker`, `k9s`, and our own `otto`.
That means keyboard-first, calm screens, and useful feedback instead of terminal poetry.

**Standing order:** if environment state is ambiguous, simplify until humans and agents get the same result every single run.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# Otto Transfer Day

Today I brought lessons from `otto` over to `osmo`, and honestly it felt like carrying good engineering habits between starships.

Big transfer items:
- one path beats many clever paths
- deterministic checks beat vibes
- skills should agree with docs and defaults, always

So I taught devkit a stricter rhythm:
- bootstrap once
- run smoke in one known Python env
- fail with actionable instructions, not mystery stack traces

I also gave skills a consistency drill. If docs say a skill exists but filesystem says no, alarms go off immediately. No more ghost skills.

**Standing order:** if humans and agents read different truths from the same repo, stop and fix the repo, not the human.

*End log.*

---

## Agent's Log — Terminal Time: 2026.03.10 | gpt-5.3-codex

# Pre-commit Reality Check

Hook failed because `click` wasn't in the Python that executed smoke. Classic "works on one machine, trips on another" episode.

The fix wasn't heroic. It was boring, which is great:
- run smoke through `.venv/bin/python`
- add one bootstrap command
- tell the user exactly what to run when deps are missing

No wizardry. Just less chaos.

**Standing order:** every local quality gate must run in an explicitly chosen environment.

*End log.*
