# Framing Interview

Loaded by `SKILL.md` at the start of Phase 1 and revisited per-section in Phase 2. Every section below maps to a section in `framing-template.md`.

For each section: ask the opening question, evaluate the answer against the quality bar, push back when it falls into a named anti-pattern, and capture the final answer in the user's own language.

## Overall Rules

1. **Ask, don't prescribe.** Do not offer menu options for open answers (problem, approach, persona). Use free-form responses. Reserve multi-select for routing decisions.
2. **Push back once, maybe twice.** If the first answer is weak, name the specific issue and ask a sharper question. If the second answer is still weak, capture what the user has given and note in the draft that the section is worth revisiting. Do not let the interview spiral.
3. **Quote the user back at them.** When challenging an answer, use the user's own words verbatim. Paraphrasing softens the challenge and is easier to dismiss.
4. **Keep each answer to 1-3 sentences.** Longer answers are usually hiding something vague. If the user writes a paragraph, ask them to pick the sentence that matters most.
5. **Don't leak the anti-pattern names.** The user does not need to hear "that's a vanity metric" - just ask the sharper question that follows.

---

## 1. Target Problem

**Opening question:** "What's the core problem this project solves - and what makes that problem hard?"

Strong answers name a specific situation the target user is in, identify what makes the situation hard *right now* (a crux, a constraint, something that isn't easy to route around), and are falsifiable - you could imagine the problem being absent and know the difference.

**Anti-patterns and pushback:**

- **Goal stated as problem** ("the problem is we need to grow revenue") -> "That's a goal, not a problem. What's in the world that's making that goal hard to achieve? Whose situation are you changing?"
- **Vague wish** ("people need better tools for X") -> "Whose situation specifically? Doing what? What do they try today, and why doesn't it work?"
- **Symptom, not cause** ("users churn after 30 days") -> "That's a symptom. What's happening in their world that makes them stop caring? What's the underlying condition?"
- **Too broad** ("communication at work is broken") -> "That's a civilization-scale problem. Narrow it to a situation you can actually affect - which users, doing what, when does it hurt most?"
- **Feature-shaped** ("there's no good way to do [specific workflow] with AI") -> "That's a missing feature, not the underlying problem. What outcome do users want that the feature would give them?"

**Capture:** One or two sentences naming the user's situation and the crux. No solution language.

---

## 2. Our Approach

Two things matter here, and only two: the goal (the outcome you're after, tied to the target problem) and the means (the choice or commitment you're making to get there). A good approach states both and makes the line between them obvious. Judge every answer on their consistency - do the means actually serve the goal, and are they sized to it rather than under-powered or absurd?

**Opening question:** "What's the goal here, and by what means do you reach it? The approach is the means you've chosen so the goal becomes reachable."

Strong answers name a clear goal tied to the target problem, name concrete means (a choice, a commitment, a bet) rather than a slogan, and make it obvious that the means serve and are proportionate to the goal.

**Anti-patterns and pushback:**

- **Goal with no means** ("our approach is to become the category leader") -> "That's the goal, not the approach. By what means? What choice are you making that gets you there?"
- **Goal pulling in two directions** ("grow as fast as possible while keeping the team tiny and unstressed") -> "Those pull against each other. Which one wins when they collide? A goal that points two ways can't guide a single decision - pick the direction the approach serves."
- **Means with no goal** ("we're rebuilding everything in Rust") -> "That's a means with no goal attached. What does rebuilding get you that matters? If you can't name the goal, you can't judge whether it's the right means."
- **Means that don't serve the goal** (goal: "earn the trust of risk-averse buyers"; means: "ship features faster than anyone") -> "How does shipping faster earn trust? Speed and trust can pull against each other. Name the means that actually serves this goal."
- **Means too weak for the goal** (goal: "cut enterprise onboarding from six weeks to two days"; means: "write better docs") -> "Better docs won't take six weeks down to two days. Either the goal is smaller than you said or the means is bigger than you've named. Which is it?"
- **Fluff / values** ("we're customer-obsessed and move fast") -> "Those are values, not means. What are you doing *differently* from the obvious alternative? If it applies to any project, it's not your approach."
- **Feature list** ("we're building AI-powered X, Y, and Z") -> "That's a list of features, not a means. What's the underlying bet that makes you pick those over others?"

**Capture:** One or two sentences naming the goal and the means, with the line between them explicit. Ideally reads "we reach [goal] by [means]".

---

## 3. Who It's For

Two dimensions: the customer we are framing for, and the business that carries the outcome. Capture both.

### Customer

**Opening question:** "Who is the primary user, and what job are they hiring this project to do?"

Jobs-to-be-done framing - the user isn't a demographic, they're someone in a situation trying to make progress.

Strong answers name one primary persona (additional personas allowed but secondary), identify them by role or situation rather than demographic, and state a concrete job as a verb phrase.

**Anti-patterns and pushback:**

- **Too many primary personas** ("it's for founders, PMs, engineers, and designers") -> "If it's for everyone, it's for no one. Who matters most? The others can still benefit, but one of them drives the decisions."
- **Demographic framing** ("25-45 year old professionals") -> "That's a demographic, not a user. What are they trying to do that makes them pick up this project?"
- **Role without situation** ("PMs") -> "PMs doing what? Running a roadmap review? Writing a spec at midnight? Convincing a skeptical eng lead? The situation is where the project matters."
- **Generic job** ("they want to be more productive") -> "Productive at what specifically? They're hiring this project to do *what*? The more specific, the better the decisions downstream."

**Capture:** Persona name plus JTBD sentence. Example: "Solo founders running their own roadmap. They're hiring the project to keep strategy and execution aligned without a PM on staff."

### Business

**Opening question:** "Whose business does this serve, and what outcome are they accountable for?"

Strong answers name a specific sponsor, team, or unit (not "the company"), state the outcome that person or group owns, and make clear why the project is worth their budget and attention.

**Anti-patterns and pushback:**

- **The whole company** ("it's good for the whole business") -> "Too diffuse. Who specifically sponsors this or carries the result if it works? Name the person or the unit."
- **Customer benefit restated as business value** ("customers will be happier") -> "That's the customer's win. What does the business get from it - revenue, cost, risk, a capability?"
- **Vague strategic alignment** ("it's strategic") -> "Strategic how? What result does someone own because of this project?"

**Capture:** The sponsor, team, or unit, plus the outcome they own and why it justifies the project.

---

## 4. What Success Means

Two dimensions: what success looks like for the customer, and what it looks like for the business. Capture both. 3-5 measures total across the two.

### For the customer

**Opening question:** "In the customer's own words, what can they do after this project that they couldn't before - and how would you know?"

Measures are the feedback loop. Bad measures create the illusion of progress while the project gets worse.

Strong answers state an ability or change we cause, phrased the way the customer would phrase it, and could plausibly regress if the project got worse.

**Anti-patterns and pushback:**

- **Vanity metrics** ("total signups, total pageviews, cumulative users") -> "Those can all go up while the customer gets nothing. What moves when users actually get value?"
- **Unmeasurable** ("user delight") -> "How specifically? If you can't define how you'd check it on a Tuesday, it's aspirational, not a measure."
- **Internal metric dressed as customer value** ("daily active users") -> "That's your dashboard, not their words. What can the customer now do that they couldn't? Say it as they would."

**Capture:** 1-3 customer measures, each in the customer's language, with a one-line note on how and where it's observed.

### For the business

**Opening question:** "What business result makes this project worth doing, and over what time frame?"

Strong answers name a concrete result - revenue, cost, risk, profit, or a capability - owned by the business, mix leading and lagging (something that moves weekly and something that moves quarterly), and carry a time frame.

**Anti-patterns and pushback:**

- **Outputs, not outcomes** ("ship velocity, deploys per week") -> "Those measure the team, not the result. If velocity doubled but the business gained nothing, would you call it a win?"
- **Too many** ("here are 12 metrics we watch") -> "A dashboard isn't a framing. Pick the ones you'd stake the quarter on. What are the others telling you that those don't?"
- **Can only go up** ("cumulative hours saved") -> "A metric that can only go up doesn't tell you much. What's the rate, the ratio, or the thing that can regress?"
- **No time frame** ("increase revenue") -> "By when, and by roughly how much? A result with no horizon can't tell you if you're on track."

**Capture:** 1-3 business measures. Each names a result and a time frame, with a note on where it's measured. If measurement is undefined, ask: "Where does this live today? If nowhere, can you start measuring it?"

---

## 5. Tracks

**Opening question:** "What are the 2-4 tracks of work you're investing in to execute the approach?"

Tracks are the coherent-actions half of the strategy kernel - concrete areas of investment that flow from the approach. They are not feature lists and not personal todo items. Each track is a named *domain of work*.

Strong answers stay at 2-4 (not 8, not 1), connect clearly back to the approach, and are broad enough that multiple features live inside each one.

**Anti-patterns and pushback:**

- **Feature list in disguise** ("track 1: Slack integration; track 2: mobile app; track 3: dark mode") -> "Those are features. What's the *investment area* each one lives inside? 'Integrations' might be one track, with Slack, Teams, and Discord as candidates inside it."
- **Too many tracks** ("we have 7 tracks this quarter") -> "With 7 tracks, every track is starved for attention. Which 3 are load-bearing? The others either fold in or drop."
- **Doesn't connect to approach** (approach: "win by being the easiest to onboard"; track: "enterprise SSO") -> "How does that track serve the approach? If it's a separate bet, name it as one. If it's load-bearing for onboarding, explain the link."
- **Too vague** ("improve the product") -> "Every track is 'improve the product.' What's the specific investment area that's different from the others?"
- **One track only** -> "With one track, there's no real choice being made. What are the 2-3 things the project needs to be good at, and how are they different?"

**Capture:** 2-4 tracks. For each: a name, a one-line purpose, and a short note on why this serves the approach.

---

## 6. Not Working On (optional)

**Opening question:** "Is there anything you've explicitly decided *not* to do right now that's worth naming? This is for things the team keeps being tempted by."

Clarity tool, not a blocker list. Skip by default. If the user names items, one sentence each. Do not encourage a long list.

---

## After the Interview

Once the required sections (1-5) are captured (and Not working on if the user engaged it), read `framing-template.md` and fill it in. Present the full draft in chat before writing. Offer one edit round. Then write to `FRAMING.md`.
