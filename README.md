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
4. Tool prompts, permission rules, classifiers, sandboxes, and mode switches should provide another layer of runtime backstops, turning prohibitions from wording into mechanism.

This is a progressive disclosure model aimed at known failure patterns: discover first, expand later. Detailed constraints are delayed until they are truly needed, while different layers provide independent safeguards.

It is not meant to lock down randomness. When the user explicitly asks for open exploration beyond usual realism or boundaries, the skill yields to that intent and keeps only truthfulness and high-severity risk escalation.

## Repository Structure

- [`skills/prohibition/`](./skills/prohibition/) - the `prohibition` skill and its supporting reference modules
- [`README.zh-CN.md`](./README.zh-CN.md) - Chinese version of this introduction
