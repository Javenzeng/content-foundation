#!/usr/bin/env python3
"""Validate a local Content Foundation Kit project without network or write access."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SOURCE_STATES = {"candidate", "verified", "retired"}
CLAIM_STATES = {"candidate", "verified", "rejected"}
ASSET_STATES = {"candidate", "final", "rejected"}
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing required file: {path.name}") from None
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path.name}: {error.msg}") from None


def require(record: dict[str, Any], field: str, label: str, errors: list[str]) -> Any:
    value = record.get(field)
    if value is None or value == "" or value == []:
        errors.append(f"{label}: missing {field}")
    return value


def index_records(records: Any, id_field: str, filename: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        errors.append(f"{filename}: expected a JSON array")
        return {}
    indexed: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"{filename}[{position}]: expected an object")
            continue
        identifier = require(record, id_field, f"{filename}[{position}]", errors)
        if not isinstance(identifier, str):
            continue
        if identifier in indexed:
            errors.append(f"{filename}: duplicate {id_field} {identifier}")
        indexed[identifier] = record
    return indexed


def validate(project_dir: Path) -> list[str]:
    errors: list[str] = []
    sources = index_records(load_json(project_dir / "sources.json"), "source_id", "sources.json", errors)
    claims = index_records(load_json(project_dir / "claims.json"), "claim_id", "claims.json", errors)
    assets = index_records(load_json(project_dir / "assets.json"), "asset_id", "assets.json", errors)
    package = load_json(project_dir / "release-package.json")

    for source_id, source in sources.items():
        for field in ("title", "canonical_url", "source_type", "retrieved_on", "status"):
            require(source, field, source_id, errors)
        if source.get("status") not in SOURCE_STATES:
            errors.append(f"{source_id}: invalid source status")

    for claim_id, claim in claims.items():
        for field in ("statement", "claim_type", "scope", "source_ids", "status"):
            require(claim, field, claim_id, errors)
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids:
            errors.append(f"{claim_id}: source_ids must be a non-empty array")
            source_ids = []
        for source_id in source_ids:
            if source_id not in sources:
                errors.append(f"{claim_id}: unknown source {source_id}")
        if claim.get("status") not in CLAIM_STATES:
            errors.append(f"{claim_id}: invalid claim status")
        if claim.get("status") == "verified" and not any(
            sources.get(source_id, {}).get("status") == "verified" for source_id in source_ids
        ):
            errors.append(f"{claim_id}: verified claim needs a verified source")

    for asset_id, asset in assets.items():
        for field in ("role", "status", "rights_basis"):
            require(asset, field, asset_id, errors)
        if asset.get("status") not in ASSET_STATES:
            errors.append(f"{asset_id}: invalid asset status")
        if asset.get("status") == "final" and not SHA256.fullmatch(str(asset.get("sha256", ""))):
            errors.append(f"{asset_id}: final asset needs a 64-character SHA-256")

    if not isinstance(package, dict):
        errors.append("release-package.json: expected an object")
        return errors
    for field in ("package_id", "status", "external_write", "approval_required", "intended_change", "rollback_plan", "claim_ids", "asset_ids"):
        require(package, field, "release-package.json", errors)
    if package.get("status") != "dry_run":
        errors.append("release-package.json: v0.1 only permits status=dry_run")
    if package.get("external_write") is not False:
        errors.append("release-package.json: external_write must be false")
    if package.get("approval_required") is not True:
        errors.append("release-package.json: approval_required must be true")
    for claim_id in package.get("claim_ids", []):
        claim = claims.get(claim_id)
        if claim is None:
            errors.append(f"release-package.json: unknown claim {claim_id}")
        elif claim.get("status") != "verified":
            errors.append(f"release-package.json: claim {claim_id} is not verified")
    for asset_id in package.get("asset_ids", []):
        asset = assets.get(asset_id)
        if asset is None:
            errors.append(f"release-package.json: unknown asset {asset_id}")
        elif asset.get("status") != "final":
            errors.append(f"release-package.json: asset {asset_id} is not final")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="folder containing the four v0.1 JSON files")
    args = parser.parse_args()
    try:
        errors = validate(args.project_dir)
    except ValueError as error:
        print(f"INVALID: {error}")
        return 1
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: local dry-run package; no external write is authorized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

