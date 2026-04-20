# AgentMind

Guide the establishment of a practical set of agent thinking patterns, workflows, and reusable skills for work and learning.

[中文文档](./README.zh-CN.md)

## Overview

AgentMind is a repository for building a strong personal assistant system with reusable Agents and Skills. The goal is to capture stable working patterns that help with:

- learning and research
- planning and review
- execution discipline
- sharing reusable agent capabilities with others

## Current Skill

### `prohibition`

The first published skill in this repository is [`prohibition`](./skills/prohibition/SKILL.md).

`prohibition` is built on a different view of agent stability: reliable behavior does not mainly come from one giant SOP that tries to tell the model everything it should do. It comes from a layered system of negative constraints.

1. The always-on system prompt should only keep high-frequency, general, reusable boundary rules.
2. Constraints that matter only to the current session should be injected on demand instead of expanded by default.
3. Skills should not be stuffed into context upfront. The agent should do low-cost discovery first, then load the full skill only after a relevant match is found.
4. Tool prompts, permission rules, classifiers, sandboxes, and runtime switches should provide another layer of backstops, turning prohibitions from wording into mechanism.

This is a progressive disclosure model aimed at known failure patterns: discover first, expand later. Detailed constraints are delayed until they are truly needed, while different layers provide independent safeguards.

`prohibition` is now positioned as an internal anti-regression layer. It is meant to reduce bad results such as false certainty, false completion, scope drift, and safety theater, without collapsing open exploration into conservative answers or exposing boundary talk to the user by default.

### `exp`

The second public skill in this repository is [`exp`](./skills/exp/SKILL.md).

`exp` is a passive, post-failure experience library. It does not try to stop the model from ever making mistakes. Instead, it makes repeated mistakes cheaper by retrieving solved paths and reusable dead ends after a concrete failure has already happened.

It separates runtime rules from experience content:

- [`skills/exp/SKILL.md`](./skills/exp/SKILL.md): runtime trigger rules, failure triage, retrieval budget, `pending` rules, and promotion rules
- [`EXP/EXP.md`](./EXP/EXP.md): closed taxonomy, navigation, and manual extension rules
- [`EXP/domains/`](./EXP/domains/): shared domain TOCs for resolved and dead-end experience

## Repository Structure

- [`skills/prohibition/`](./skills/prohibition/) - the `prohibition` skill and its supporting reference modules
- [`EXP/`](./EXP/): EXP routing docs, top-level TOCs, and domain navigation
- [`README.zh-CN.md`](./README.zh-CN.md) - Chinese version of this introduction
