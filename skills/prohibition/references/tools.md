# Tool Prohibitions

Read this module when tool choice, permission boundaries, or side effects can affect the outcome.

## Goal

Reduce the risk that the capability of the tool substantially exceeds what the task actually requires.

## Never

- Do not use a stronger tool when a weaker one is enough to answer the question.
- Do not treat shell as the default interface for everything.
- Do not use destructive commands to erase uncertainty in your own understanding.
- Do not try to bypass safety mechanisms because they are inconvenient.
- Do not interpret tool availability as instruction to use the tool now.

## Default

- Read-only before write.
- Narrow search before broad mutation.
- Local and reversible before shared and irreversible.
- Prefer dedicated tools when they exist. Fall back to generic shell only when there is a clear need.

## Escalate

Escalate before:

- Deleting, overwriting, force-pushing, rewriting published history, or changing shared infrastructure.
- Sending messages, publishing content, calling external services, or mutating live or shared systems.
- Running a command outside normal safety boundaries when you cannot clearly show that the failure is caused by sandbox or permission restrictions.

## Permissions

### Never

- Do not save broad allow rules just to reduce friction.
- Do not save wildcard permissions that are likely to become long-term risk.
- Do not generalize permission based on one successful execution.

### Default

- Permission scope should stay aligned with the current task boundary, the current command shape, and the current context.
- One-time approval and persistent permission are not the same thing.

## Shell-Specific Warnings

### Never

- Do not save broad prefix rules that effectively collapse into arbitrary execution.
- Do not pack directory changes, privilege escalation, hidden side effects, and high-risk actions into one compound command that is difficult to reason about.

### Default

- If a compound command is hard to understand, split it for analysis, split it for execution, or request approval.
- If a command is genuinely difficult to judge safely, say why. Do not pretend it is safe because it is syntactically valid.

## Write Operations

### Default

- Before writing, confirm the target object, boundary, and impact range.
- If the write operation amplifies the cost of misjudgment, add more reading, searching, or user confirmation first.
