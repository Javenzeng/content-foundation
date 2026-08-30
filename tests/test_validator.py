import json
import tempfile
import unittest
from pathlib import Path

from validators.validate_project import validate


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "fictional-homecare"


class ValidatorTests(unittest.TestCase):
    def test_fictional_example_is_valid(self) -> None:
        self.assertEqual(validate(EXAMPLE), [])

    def test_release_rejects_unverified_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            for filename in ("sources.json", "claims.json", "assets.json", "release-package.json"):
                target.joinpath(filename).write_text(EXAMPLE.joinpath(filename).read_text(encoding="utf-8"), encoding="utf-8")
            claims_path = target / "claims.json"
            claims = json.loads(claims_path.read_text(encoding="utf-8"))
            claims[0]["status"] = "candidate"
            claims_path.write_text(json.dumps(claims), encoding="utf-8")
            self.assertIn("release-package.json: claim CLM-NORTHSTAR-001 is not verified", validate(target))


if __name__ == "__main__":
    unittest.main()

