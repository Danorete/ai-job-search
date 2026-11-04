---
name: token-efficiency
description: >
  Rules for minimizing token usage across all workflows in this repo (setup,
  scrape, apply, interview). Apply automatically during any multi-step task;
  invoke explicitly when the user mentions token usage, context limits, session
  limits, running out of context, or cost. Triggers on: token usage, tokens,
  context limit, session limit, reduce cost, /token-efficiency
allowed-tools: Read, Glob, Grep
---

# Token Efficiency Rules

Why this exists: a full `/apply` run for multiple roles can exhaust a session's
token budget, killing subagents mid-review. Most of the waste comes from a few
repeatable mistakes. Follow these rules in every workflow.

## 1. Never re-read what is already in context

- A file read once this session is still in context. Do not Read it again
  before editing it or quoting it.
- After Write/Edit succeeds, do not Read the file back to "verify" - the tool
  errors if the change failed.
- The candidate profile, behavioral profile, evaluation framework, and style
  guide change rarely. One read per session, ever.

## 2. Subagents are the biggest single cost - use them surgically

- Each subagent starts cold and re-reads everything you don't hand it. Pass
  drafts, profile excerpts, and posting text **inline in the prompt** instead
  of telling the agent to Read files.
- Prefer ONE reviewer agent per `/apply` run. For multi-role batches, run the
  first role through an agent review, then apply the same critique patterns
  inline to the remaining roles yourself (overclaim softening, keyword
  surfacing, verified-claims-only). Four parallel reviewers quadruple cost for
  mostly duplicated findings.
- Scope the agent's file reads to the minimum (the four content-critique files,
  never the LaTeX template guides).

## 3. Quiet tool output

- Compile LaTeX with output suppressed and grep only the verdict:
  `lualatex -interaction=nonstopmode file.tex >/dev/null 2>&1; grep -o 'Output written on.*' file.log | tail -1`
- Pipe long command output through `tail`/`grep` - never dump raw compile logs,
  apt output, or full search pages into context.
- Batch shell steps: one loop over four CVs, not four separate calls.

## 4. Search and fetch discipline

- One WebSearch per fact you need to verify; stop when verified. Do not
  re-research a company already researched this session.
- Skip WebFetch on domains that already returned 403 this session (careers
  pages, Glassdoor, Indeed) - go straight to WebSearch snippets.

## 5. Draft once, edit in place

- Keep draft text in working memory; revise with targeted Edit calls, not
  full-file rewrites.
- When only one sentence changes, Edit that sentence. Reserve Write for new
  files.

## 6. Answer at the right length

- Fit evaluations: the scoring table plus 3-5 bullets, not an essay.
- Status updates between tool calls: one line.
- Do not restate file contents the user already received as a PDF or diff.

## 7. When the budget is nearly gone

- Finish and deliver the current document before starting the next role.
- Prefer inline work over spawning anything.
- Tell the user what remains undone rather than starting work that will be
  cut off mid-task.
