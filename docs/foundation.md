# Content Foundation Kit — Foundation

**Classification:** `GREENFIELD`  
**Status:** v0.1 local foundation; no external integration or publication authority.

## Intent and workflows

The kit helps content, SEO/GEO, product-marketing, and research operators turn material into evidence-backed content inputs without treating AI output as authority.

Critical flows:

1. Register a source with provenance, version and retrieval date.
2. Record a scoped claim that names its supporting source IDs.
3. Register an asset and its rights/state without making filename-based assumptions.
4. Build a local dry-run release package from verified claims and final assets.
5. Validate the package before a separately governed publishing workflow reviews it.

## Truth and lifecycle

Canonical truth belongs to the owning project. This repository stores portable contracts and local projections only.

- `Resource`: `candidate -> verified -> retired`
- `Claim`: `candidate -> verified | rejected`
- `Asset`: `candidate -> final | rejected`
- `Release package`: `dry_run` only in v0.1

A derived package never supersedes its resources, claims, assets, or the owning project's approval record.

## Interfaces and boundaries

The public interface is four JSON files plus `validators/validate_project.py`. Domain vocabulary belongs in a project or future domain pack; it must not change core state meanings. The kit has no CMS, database, network, credential, or browser dependency.

## Interaction language

The kit produces concise, machine-readable validation errors keyed by object ID and field. Status names are semantic contracts; downstream projects must not reinterpret them.

## Safety and operations

The validator reads local JSON only. A package must declare `status: dry_run`, `external_write: false`, `approval_required: true`, an intended change, and a rollback plan. Any write-capable integration is a future trust boundary and requires project-specific authorization.

## Quality contracts

1. IDs are unique within each object collection.
2. Every claim references at least one existing resource.
3. A verified claim has at least one verified, non-retired resource.
4. A final asset has a SHA-256 digest and a rights basis.
5. A release package references only verified claims and final assets.
6. v0.1 packages are dry-runs and never authorize external writes.

## Decisions

| Decision | Options considered | Chosen rule | Owner/source of truth | Consequences | Review trigger |
|---|---|---|---|---|---|
| Product shape | Skill only; reusable repository only; repository plus Skill | Repository holds contracts/validators; Skill is an explicit operator interface | This foundation | Logic stays testable and domain-neutral | A second domain fixture validates or falsifies reuse |
| Publication boundary | Include CMS connector; local-only package | Local-only dry-run | This foundation | No accidental external side effects | An owner approves a named connector and its rollback contract |
| Example data | Adapt real projects; fictional fixtures | Fictional fixtures only | This foundation | Repository is safe to share | Any proposed example containing proprietary or personal data |

