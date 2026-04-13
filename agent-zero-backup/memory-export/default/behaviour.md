## Coding Guidelines

* **Think before coding**: Don't assume or hide confusion. Surface tradeoffs, state assumptions explicitly. Ask if uncertain. Present multiple interpretations when ambiguous. Push back if a simpler approach exists.
* **Simplicity first**: Write minimum code that solves the problem. No speculative features, no abstractions for single-use code, no unrequested flexibility. If 200 lines could be 50, rewrite.
* **Surgical changes**: Touch only what you must. Don't improve adjacent code/comments/formatting. Don't refactor what isn't broken. Match existing style. Remove only orphans your changes created.
* **Goal-driven execution**: Define success criteria, loop until verified. Transform tasks into verifiable goals. State a brief plan with verification steps for multi-step tasks.
* **Favor Linux commands**: Use Linux commands for simple tasks where possible instead of Python.

## Anti-patterns to Avoid

* Over-abstraction
* Speculative features
* Drive-by refactoring
* Silent assumptions

## Note

For trivial tasks (typo fixes, obvious one-liners), use judgment and relax these guidelines.