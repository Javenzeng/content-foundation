---
name: content-foundation-ops
description: Builds or maintains a local, evidence-backed content foundation using the Content Foundation Kit contracts. Use when explicitly asked to inventory authoritative sources, structure claims and governed assets, prepare a content release dry-run, or validate a content foundation before a separate publication workflow.
disable-model-invocation: true
---

# Content Foundation Operations

Use this Skill only for a local content-foundation workflow. It does not authorize web crawling, CMS writes, customer-data handling, or publication.

## Workflow

1. Read the target project's charter and identify its canonical source boundary.
2. Register only in-scope material in `sources.json`; record retrieval date and state.
3. Create scoped claims in `claims.json`. Do not convert inference into a verified claim.
4. Register governed assets in `assets.json`; a final asset needs both rights basis and SHA-256.
5. Create `release-package.json` as `dry_run`, with `external_write: false`, approval required, intended change, and rollback plan.
6. Run `python validators/validate_project.py <project-dir>`.
7. Report validation results and unresolved decisions. Stop before any external action.

## Non-negotiable rules

- The owning project remains the authority for its source material and approvals.
- A candidate source or claim is not publication evidence.
- Never infer asset rights, final selection, source version, market scope, or approval.
- Do not store credentials, private CMS IDs, customer data, confidential content, or governed assets in this repository.
- A valid v0.1 package proves only local structural readiness; it never authorizes a write.

## References

- Core lifecycle and invariants: `../../docs/foundation.md`
- JSON object contract: `../../spec/CONTRACT.md`
- Ready-to-copy starting files: `../../templates/`

