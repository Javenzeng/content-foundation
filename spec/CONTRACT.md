# v0.1 object contract

Each project folder contains these JSON arrays/files:

- `sources.json`: resources with `source_id`, title, canonical URL, type, retrieval date and status.
- `claims.json`: scoped statements with a lifecycle state and source references.
- `assets.json`: governed assets with lifecycle state, rights basis and final digest where applicable.
- `release-package.json`: one local, approval-gated dry-run package.

The validator is the executable contract. JSON schemas document the portable shape; project-specific domain rules should be added as a domain pack, not by changing core status meanings.

