# Q1 What are Intake Primitives, and why are they the core new concept this build tests?

## A1

Intake Primitives are the three kinds of item the operator drops into the harness for later processing: questions, ideas and problems. Each is a blank file in a `_New` folder; the operator writes inside a fence and ticks a ready box, and a `/sweep` skill moves ticked items to a backlog. Only the operator creates them; the assistant only sweeps and later processes them. Questions lead to research and knowledge-base entries, ideas to specs and deliverables, problems to harness improvements.

Why they exist: the harness's core design constraint is that the operator often has low energy and focus. He knows what intent the assistant needs, but struggles to overcome the effort of writing it out. The most damaging failure mode is starting complex tasks without communicating intent in enough detail. Intake Primitives are "an experimental attempt to provide a low friction pipeline to lower the effort threshold of communicating his intent at the level needed" for complex tasks. The workflows that carry each primitive from backlog to its end point were not designed yet; the sessions behind `PROMPTS.md` were designing and testing them, starting with Questions.

Source: `System/System Information/Controlled vocabulary.md` (Intake Primitives entry); `System/System Information/System core principles.md`; `.claude/worktrees/brainstorming-intent-pipelines/System/Brainstorms/Question pipeline - open questions.md` (line 3).

# Q2 What is this repository?

## A2

The bootstrap of the operator's new Claude Code harness, called "Harness seed". The root `CLAUDE.md` says it draws on 1000+ hours of experimenting with harnesses: lessons from collapsed systems, completed projects worth reusing, and lessons "inside my head", always checked against current external research. The assistant is fenced to this working directory unless given permission. Child working directories at the root are called System Components.

Source: `CLAUDE.md` (root, operator-authored); `System/System Information/Lexicon.md` (Harness).

# Q3 What is "Operator RAM"?

## A3

A provisional term for the operator's capacity for concurrent effort: how much intent, context and decision-making he can hold at one time. It caps the rate of effort, not the total. A step fits within Operator RAM when he can read, check and correct it on its own, without holding other steps in mind. In the operator's framing of the question pipeline, each step along the pipeline must fit within it.

Source: `System/System Information/Lexicon.md` (Operator RAM); `System/Snippets/SNIP_2026-10-14_231927.md`.

# Q4 What is a post-threshold snippet, and why are some prompts saved verbatim?

## A4

"Post-threshold" means effortful pushing past Operator RAM. A snippet is one operator message kept verbatim. Post-threshold snippets are saved in `System/Snippets/` (with an index) as save points: if decisions built on them are lost or captured badly, a later session can rebuild from the operator's exact words.

Source: `System/System Information/Lexicon.md` (Post-threshold, Snippet); `System/Snippets/INDEX.md`.

# Q5 What was built in the sessions these prompts come from?

## A5

Two tracks, recorded in an overnight report. (1) The question pipeline: seven pipeline designs tested in three experiments on two of the operator's questions, with a simulated operator doing the ticking (labelled SIMULATED in every file) and two blind judges on different models. (2) A "PMF tester" baseline build: an application built from the operator's stated intent with no follow-up questions, to measure how far a build gets before missing intent becomes the limit. Everything is on a sandbox branch; nothing was merged.

Source: `.claude/worktrees/brainstorming-intent-pipelines/System/Brainstorms/Experiments/2026-10-15/REPORT.md`.

# Q6 What did the question-pipeline experiments find?

## A6

- Experiment A (answer key invented by a model): best/worst picking (P3) recovered the most intent per click; only the hybrid (P5) held up when the simulated operator clicked "yeah, fine"; precision was weakest everywhere, with about five assistant guesses per result stated as the operator's.
- Experiment B (the operator's real intent): the real intent was mostly not recoverable by clicking, because its core is information only the operator holds; experiment A had overstated what pipelines can do.
- Experiment C: one optional line first, "What is this for?", raised capture of the question's core intent to 1.00 (attentive, P3 and P5) and 0.88 (tired, P5), but tired P3 fell from 0.67 to 0.54. Detail the operator never wrote stayed unrecoverable. n = 2 runs per cell: signals, not proof.

Source: `.../Experiments/2026-10-15/RESULTS_A.md`, `RESULTS_B.md`, `RESULTS_C.md` (under `.claude/worktrees/brainstorming-intent-pipelines/System/Brainstorms/`).

# Q7 Which pipeline shape was recommended?

## A7

P5 with a purpose line first: an optional one-line `PURPOSE.md`, then a few lens cards, then forced-choice forks, then one-line yes/no claims, with the final intent written only from the operator's ticks and his own words. Reading load about 1.8-2.8k words over 4-5 rounds, at most about 500 words per round.

Source: `.../Experiments/2026-10-15/RESULTS_C.md` (Recommendation); `REPORT.md`.

# Q8 What is the PMF tester, and how far did the baseline get?

## A8

An application that takes a list of business ideas and, for each, would build a landing page, buy a domain, set up email infrastructure, build lead lists, run cold email and score product-market fit from the outbound metrics. The baseline has 14 modules and 2,992 passing tests; a dry run takes 3 sample ideas end to end over 43 simulated days with 62 vendor writes recorded and 0 live calls. Every vendor and the LLM are mocks and the market is simulated, so the scores prove the plumbing, not any market. Nothing was bought, sent or charged. Of 28 audit findings, 27 were fixed and 1 deferred. The build needed 63 guesses about the operator's intent, 15 of them high impact, and one high-impact guess is really a bug: no email carries the landing-page link.

Source: `.claude/worktrees/brainstorming-intent-pipelines/System/Snippets/SNIP_2026-10-15_014914.md` (the application, in the operator's words); `.claude/worktrees/brainstorming-intent-pipelines/Work/PMF-tester/BASELINE_REPORT.md` (sections 1-2); `REPORT.md`.

# Q9 What was the answer to the operator's captcha questions?

## A9

In the PMF tester's design, a solved problem in practice: its recurring steps use API keys and meet no captcha; captchas appear only at one-time signups, and because some vendors' terms ban bot signups, each is a single human step per vendor. This comes from research and design, not a live test: nothing was signed up for.

Source: `.../Work/PMF-tester/BASELINE_REPORT.md` (section 1); `REPORT.md`.

# Q10 What is still open, and what went wrong?

## A10

- About five of the assistant's guesses per run still end up stated as the operator's intent; the "only what he ticked or wrote" rule reduces but does not stop it.
- 14 open questions are tracked for the pipeline design.
- The operator's own statement of the core failure mode: work done in a sandbox branch escaping to main without a verification that fits within his RAM, because "I am very, very likely to just say 'yeah, fine, that looks close enough'", confounded by his principle that "all delegation of authority over the operator's behavior is theater". How to square this is open.
- The PMF baseline's 63 intent guesses are unanswered, and it has only run on mocks.
- The assistant misread the operator's 70% context rule as automatic compaction; the operator corrected it to a handover to a new session, and how a session detects the threshold is still open.

Source: `.../Experiments/2026-10-15/RESULTS_C.md` (finding 4); `.../System/Brainstorms/Question pipeline - open questions.md`; `System/Snippets/SNIP_2026-10-15_004919.md`; `.../Work/PMF-tester/BASELINE_REPORT.md`; `.../Experiments/2026-10-15/HANDOVER.md` (line 55, the 70% rule); `REPORT.md`.
