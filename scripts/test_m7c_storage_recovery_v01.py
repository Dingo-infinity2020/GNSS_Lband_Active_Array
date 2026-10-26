"""Harmless regression tests for storage/authorization failure boundaries."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from collections import namedtuple
from m7c_storage_recovery_preflight_v01 import GIB, storage_check, tree_identity, require_live_grant, sha

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "execution/M7C_STORAGE_RECOVERY_SOLVE_MANIFEST_V01.json"
Usage = namedtuple("Usage", "total used free")


class RecoveryGuards(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.output = self.root / "output"
        self.temp = self.root / "temp"
        self.output.mkdir()
        self.temp.mkdir()
        self.policy = {"output_min_free_bytes": 32 * GIB, "temp_min_free_bytes": 8 * GIB}

    def check_storage(self, free, separate=False):
        return storage_check(self.policy, self.output, self.temp,
                             disk_usage=lambda p: Usage(100 * GIB, 0, free),
                             volume_identity=(lambda p: str(p)) if separate else (lambda p: "one"))

    def test_shared_volume_sums_reservations(self):
        self.assertTrue(self.check_storage(40 * GIB)["status"].startswith("PASS_"))
        self.assertTrue(self.check_storage(40 * GIB - 1)["status"].startswith("HOLD_"))
        self.assertTrue(self.check_storage(32 * GIB)["status"].startswith("HOLD_"))

    def test_separate_volumes_each_need_own_budget(self):
        r = storage_check(self.policy, self.output, self.temp,
                          disk_usage=lambda p: Usage(100 * GIB, 0, (32 if Path(p) == self.output else 7) * GIB),
                          volume_identity=lambda p: str(p))
        self.assertTrue(r["status"].startswith("HOLD_"))
        self.assertTrue(self.check_storage(32 * GIB, separate=True)["status"].startswith("PASS_"))

    def test_invalid_budget_and_probe_failure_fail_closed(self):
        for value in (0, -1, True, "34359738368"):
            self.policy["output_min_free_bytes"] = value
            self.assertTrue(self.check_storage(100 * GIB)["status"].startswith("HOLD_"))
        self.policy["output_min_free_bytes"] = 32 * GIB
        def broken(path):
            raise OSError("probe unavailable")
        self.assertTrue(storage_check(self.policy, self.output, self.temp, disk_usage=broken)["status"].startswith("HOLD_"))

    def test_canonical_tree_global_sort_and_content_drift(self):
        (self.output / "z").write_bytes(b"z")
        (self.output / "a").mkdir()
        (self.output / "a" / "b").write_bytes(b"b")
        records = [("a/b", b"b"), ("z", b"z")]
        payload = b"".join((name + "\0" + "1\0" + hashlib.sha256(data).hexdigest() + "\n").encode() for name, data in records)
        before = tree_identity(self.output)
        self.assertEqual(before["tree_sha256"], hashlib.sha256(payload).hexdigest())
        (self.output / "z").write_bytes(b"changed")
        self.assertNotEqual(before, tree_identity(self.output))

    @unittest.skipIf(sys.platform == "win32", "link creation is privilege-dependent on Windows")
    def test_tree_rejects_symlink(self):
        (self.output / "link").symlink_to(self.temp, target_is_directory=True)
        with self.assertRaises(RuntimeError):
            tree_identity(self.output)

    def test_closed_and_consumed_grants_cannot_launch(self):
        m = json.loads(MANIFEST.read_text())
        c = json.loads((ROOT / "execution/stage_contract.json").read_text(encoding="utf-8-sig"))
        with self.assertRaisesRegex(RuntimeError, "NO_LIVE_SOLVE_GRANT"):
            require_live_grant(c, m, ROOT)
        fixture = copy.deepcopy(c)
        fixture["authorization"]["SOLVE_AUTHORIZED"] = True
        fixture["execution"]["current_stage"] = m["stage"]
        # Synthetic in-memory unit fixture only; never emitted as a production grant.
        fixture["authorization"]["active_grant"] = {"grant_id": "unit-fixture", "kind": "SOLVE", "state": "GRANTED", "stage": m["stage"], "source_commit": c["project"]["source_commit"], "entrypoint_sha256": sha(ROOT / m["execution"]["runner"])}
        fixture["authorization_history"].append({"grant_id": "unit-fixture"})
        with self.assertRaisesRegex(RuntimeError, "GRANT_IDENTITY"):
            require_live_grant(fixture, m, ROOT)

    def test_ungranted_entrypoint_exits_before_import_or_output(self):
        m = json.loads(MANIFEST.read_text())
        evidence = self.root / "never-created"
        result = subprocess.run([sys.executable, "-B", str(ROOT / m["execution"]["runner"]), "--manifest", str(MANIFEST), "--out", str(self.root / "not.cst"), "--evidence", str(evidence)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NO_LIVE_SOLVE_GRANT", result.stderr)
        self.assertNotIn("No module named 'cst'", result.stderr)
        self.assertFalse(evidence.exists())
        self.assertFalse((self.root / "not.cst").exists())

    def test_generator_writes_no_packet_without_grant(self):
        m = json.loads(MANIFEST.read_text())
        packet = self.root / "packet.json"
        result = subprocess.run([sys.executable, "-B", str(ROOT / m["execution"]["packet_generator"]), "--project-root", str(ROOT), "--manifest", str(MANIFEST), "--packet", str(packet), "--state-root", str(self.root / "state"), "--result-packet", str(self.root / "result.json"), "--cst-python", sys.executable], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NO_LIVE_SOLVE_GRANT", result.stderr)
        self.assertFalse(packet.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2, testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
