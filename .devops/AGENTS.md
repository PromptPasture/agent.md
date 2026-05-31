# AGENTS.md

## Devops Tooling

- Run JavaScript tooling from `.devops/js-tools` unless a script documents a different working directory.
- Treat files under `.devops/js-tools/dist/` as generated outputs. Do not hand-edit them without also updating or rerunning the source script that produces them.
- Keep operational scripts narrow and explicit. Prefer small project-local scripts over broad shell glue.
- When changing package scripts, lockfiles, or workflow-facing output, verify the command that downstream automation will run.
