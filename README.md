# Content Foundation Kit

`content-foundation` is a local-first kit for turning source material into an auditable, approval-gated content input. It is intentionally not a content generator, search crawler, CMS connector, or publishing system.

## v0.1 scope

- Record versioned resources, scoped claims, governed assets, and dry-run release packages.
- Enforce source, lifecycle, approval, and no-write invariants with a dependency-free validator.
- Provide a fictional end-to-end example and an explicit-use Codex Skill.

It does **not** ingest proprietary content, crawl the web, call external APIs, send data to a CMS, or perform external writes.

## Quick start

```powershell
python validators/validate_project.py examples/fictional-homecare
python -m unittest discover -s tests -v
```

The validator accepts only a local `dry_run` release package. A real publication requires a project-specific integration, explicit approval, a target-state plan, and a rollback plan outside this kit.

## Repository map

- `docs/foundation.md` — operating foundation and decision record.
- `spec/` — object contracts and lifecycle rules.
- `templates/` — empty starting points for a new project.
- `validators/` — deterministic local validation.
- `examples/` — fictional fixtures only.
- `skills/` — an explicit-use Codex operating skill.

## Safety boundary

Do not commit customer material, unpublished content, credentials, private CMS IDs, regulated claims, or governed media. Keep those in the owning private project and import only their approved, minimal metadata when appropriate.

