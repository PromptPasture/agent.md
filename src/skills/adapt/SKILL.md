---
name: adapt
description: Diagnose when skills, rules, workflows, docs, evals, or memory conventions are mismatched to current conditions — triggered by failures, friction, user feedback, outdated assumptions, or changed constraints — then name the smallest change needed and route to the skill or workflow that should update it. Use when the user says "adapt based on this", "what should change after this?", "this keeps happening", "this failed, what should change?", "the workflow no longer fits", "the constraints changed", or asks what skill, rule, doc, eval, memory, or process should change.
license: MIT
tags:
  - adaptation
  - feedback
  - process
metadata:
  author: Oleg Shulyakov
  version: "1.3.1"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
  references:
    - create-skill
    - create-rule
    - remember
---

# adapt

Diagnose mismatches in skills, rules, workflows, docs, evals, or memory — then name the smallest change and apply it by routing to the right skill.

---

Feature: Diagnose and act on a mismatch signal

  Background:
    Given the user has presented a signal of mismatch
    And the signal is one of: failure, friction, feedback, outdated assumption, or changed constraint

## Guard: skip one-offs

  Scenario: Signal is a one-off with no structural cause
    Given the signal occurred exactly once
    And no structural cause is identifiable
    And the user has not signaled recurrence ("this keeps happening", "again", "always")
    Then explain why no change is warranted
    And stop

## Classify signal and identify target

  Scenario Outline: Classify signal and map to target artifact
    Given the signal is a `<type>`
    Then identify the likely target as `<target>`
    And proceed to scoping the change

    Examples:
      | type                 | target                  |
      | failure              | skill, eval, or test    |
      | friction             | rule, workflow          |
      | explicit feedback    | skill, doc, or memory   |
      | outdated assumption  | memory, doc, or spec    |
      | changed constraint   | rule, PRD, or skill     |

## Scope the change

  Scenario: Target inherits from a governing doc
    Given the artifact is downstream of a template, convention, or spec
    Then route the change to the governing doc first
    And not only to the downstream artifact

  Scenario: Name the smallest change
    Given a target artifact is identified
    Then name exactly one behavioral delta
    And do not propose a full rewrite

## Act: apply the change

  Scenario: Target is a skill
    Given the target artifact is a SKILL.md file
    Then invoke skill-creator to apply the update
    And preserve the original skill name and frontmatter fields
    And copy the skill to a writable location before editing if the source is read-only

  Scenario: Target is a rule
    Given the target artifact is a rule file (`rules/<name>.md`, `CLAUDE.md`, `AGENTS.md`, etc.)
    Then invoke creator-rule to write or update the rule
    And check for conflicts with existing rules before writing
    And scope the rule narrowly — one concern per file

  Scenario: Target is a doc or spec
    Given the target artifact is documentation or a specification
    Then draft the minimal diff — only the section that changed
    And present it to the user for confirmation before writing

  Scenario: Target is memory or context
    Given the target artifact is a memory or convention held in context
    Then state the updated convention explicitly
    And ask the user to confirm before treating it as active

  Scenario: Target artifact or routing is unclear
    Then list the candidate artifacts with supporting evidence for each
    And ask one question to resolve the ambiguity
    And do not act until resolved

## Verify

  Scenario: Confirm the action is complete
    Then state what was changed and where
    And state what must be true for the change to be considered successful
    And confirm the signal maps to a concrete event, not a vague concern
    And confirm the change addresses future occurrences, not only this incident
    And confirm no smaller change would have addressed the same signal

## Boundary

  Scenario: adapt itself is invoked but its own workflow did not fail
    Then do not route changes back to adapt
