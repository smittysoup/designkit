import copy, json, shutil, tempfile, unittest, zipfile
from pathlib import Path
from designkit.cli import (
    init,
    install,
    uninstall,
    check,
    bridge,
    reconcile,
    snapshot,
    digest,
    dumps,
    artifact_revision,
    CAPABILITIES,
)

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/caseflow/design/caseflow"


class DesignKitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="designkit space ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def example(self):
        r = self.root / "design/caseflow"
        shutil.copytree(EXAMPLE, r)
        return r

    def mutate(self, r, fn):
        m = json.loads((r / "manifest.json").read_text())
        fn(m)
        (r / "manifest.json").write_text(dumps(m))

    def test_fresh_existing_two_initiatives(self):
        (self.root / "AGENTS.md").write_text("authored")
        (self.root / ".specify").mkdir()
        (self.root / ".specify/custom").write_text("keep")
        init(self.root, "one", "manual intake", "reduce rework", "codex")
        init(self.root, "two", "case review", "retain judgment", "claude")
        self.assertEqual((self.root / "AGENTS.md").read_text(), "authored")
        self.assertEqual((self.root / ".specify/custom").read_text(), "keep")
        for adapter in (".agents", ".claude"):
            for cap in CAPABILITIES:
                txt = (
                    self.root / adapter / "skills" / ("designkit-" + cap) / "SKILL.md"
                ).read_text()
                self.assertIn("name: designkit-" + cap, txt)
                self.assertIn("AI-native agent operating model", txt)
        with self.assertRaises(ValueError):
            init(self.root, "one", "x", "y", "generic")

    def test_rerun_update_and_edited_collision_atomic(self):
        install(self.root, "codex")
        install(self.root, "codex")
        p = self.root / ".designkit/commands/discover.md"
        p.write_text("authored")
        before = {str(f): digest(f) for f in self.root.rglob("*") if f.is_file()}
        with self.assertRaises(ValueError):
            install(self.root, "claude")
        self.assertEqual(
            before, {str(f): digest(f) for f in self.root.rglob("*") if f.is_file()}
        )
        self.assertIn(
            ".designkit/commands/discover.md", uninstall(self.root)["retained_edited"]
        )
        self.assertEqual(p.read_text(), "authored")

    def test_unowned_collision_and_traversal(self):
        p = self.root / ".designkit/commands/discover.md"
        p.parent.mkdir(parents=True)
        p.write_text("unowned")
        with self.assertRaises(ValueError):
            install(self.root, "generic")
        with self.assertRaises(ValueError):
            init(self.root, "../escape", "a", "b", "generic")

    def test_symlink_rejected(self):
        (self.root / ".designkit").symlink_to(
            self.root / "elsewhere", target_is_directory=True
        )
        with self.assertRaises(ValueError):
            install(self.root, "generic")

    def test_example_is_honestly_not_ready(self):
        result = check(self.example())
        self.assertEqual(result["structural_gaps"], ["Blocking question: Q-1"])
        self.assertEqual(len(result["review_gaps"]), 4)
        self.assertEqual(result["readiness"], "not_ready")

    def test_draft_templates_cannot_pass(self):
        init(self.root, "draft", "intake", "outcome", "generic")
        r = check(self.root / "design/draft")
        self.assertTrue(
            any("Incomplete substantive" in x for x in r["structural_gaps"])
        )
        self.assertTrue(
            any("Missing record kind: agent" in x for x in r["structural_gaps"])
        )

    def test_missing_or_heading_only_model(self):
        r = self.example()
        p = r / "architecture/data-model.md"
        p.write_text("# Model\n")
        self.assertTrue(
            any(
                "Incomplete substantive content: architecture/data-model.md" == x
                for x in check(r)["structural_gaps"]
            )
        )
        p.unlink()
        self.assertIn(
            "Missing artifact: architecture/data-model.md", check(r)["structural_gaps"]
        )

    def test_missing_evaluation_plan(self):
        r = self.example()
        (r / "transformation/evaluation-plan.md").unlink()
        self.assertIn(
            "Missing artifact: transformation/evaluation-plan.md",
            check(r)["structural_gaps"],
        )

    def test_authority_and_traceability(self):
        r = self.example()

        def mutate(m):
            a = next(x for x in m["records"] if x["kind"] == "agent")
            a["authority"] = ""
            m["records"].append(copy.deepcopy(a))
            next(x for x in m["records"] if x["kind"] == "flow")["refs"] = []

        self.mutate(r, mutate)
        g = check(r)["structural_gaps"]
        self.assertIn("Duplicate stable IDs", g)
        self.assertIn("Undefined agent boundary: AGENT-Prepare", g)
        self.assertTrue(any("Incomplete trace coverage: FLOW-" in x for x in g))
        self.assertIn("Traceability index differs from manifest records", g)

    def test_unknown_references_redesign_nfr(self):
        r = self.example()

        def mutate(m):
            m["records"][0]["refs"] = ["MISSING"]
            next(x for x in m["records"] if x["kind"] == "future_step")["rationale"] = (
                ""
            )
            next(x for x in m["records"] if x["kind"] == "nfr")["owner"] = ""
            m["questions"][0]["owner"] = ""

        self.mutate(r, mutate)
        g = "\n".join(check(r)["structural_gaps"])
        self.assertIn("Unresolved reference", g)
        self.assertIn("Missing redesign rationale", g)
        self.assertIn("Unowned material NFR", g)
        self.assertIn("Unowned question", g)

    def test_broken_capture_and_stale_source(self):
        r = self.example()
        (r / "experience/screenshots/question.png").unlink()
        (r / "experience/prototype/app.js").write_text("// changed")
        g = check(r)["structural_gaps"]
        self.assertIn("Broken screen capture", g)
        self.assertIn("Stale screen source: SCREEN-Question", g)
        self.assertIn("Stale evidence: EVID-1", g)

    def test_reviews_cannot_be_fictional_or_stale(self):
        r = self.example()
        self.mutate(
            r,
            lambda m: m["reviews"].append(
                {
                    "role": "business",
                    "status": "accepted",
                    "reviewer": "Fictional person",
                    "synthetic": True,
                    "paths": ["brd.md"],
                    "revision": "old",
                    "evidence": "brd.md",
                }
            ),
        )
        self.assertIn(
            "Missing, fictional or stale human review: business",
            check(r)["review_gaps"],
        )

    def test_partial_export(self):
        r = self.example()
        out = self.root / "out.zip"
        report = snapshot(r, out)
        self.assertEqual(report["readiness"], "not_ready")
        with zipfile.ZipFile(out) as z:
            self.assertIn("architecture/data-model.md", z.namelist())
            self.assertIn("experience/prototype/app.js", z.namelist())
            self.assertEqual(
                json.loads(z.read("export.json"))["assessment"]["readiness"],
                "not_ready",
            )
        with self.assertRaises(ValueError):
            snapshot(r, out)

    def test_bridge_preservation_and_reconciliation(self):
        r = self.example()
        f = self.root / "feature space"
        f.mkdir()
        (f / "data-model.md").write_text("existing downstream")
        before = digest(r / "architecture/data-model.md")
        state = bridge(r, f)
        self.assertEqual((f / "data-model.md").read_text(), "existing downstream")
        self.assertFalse(reconcile(f)["conformant"])
        for m in state["mappings"]:
            p = f / m["target"]
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f / "designkit-input" / m["source"], p)
        self.assertTrue(reconcile(f)["conformant"])
        (f / "contracts/operations.json").write_text(
            '{"authority":"agent may approve"}'
        )
        self.assertIn(
            "Unreviewed model/contract difference: contracts/operations.json",
            reconcile(f)["gaps"],
        )
        self.assertEqual(digest(r / "architecture/data-model.md"), before)
        (f / "designkit-input/architecture/data-model.md").write_text("tampered")
        self.assertIn(
            "Frozen source altered: architecture/data-model.md", reconcile(f)["gaps"]
        )
        with self.assertRaises(ValueError):
            bridge(r, f)

    def test_manifest_schema(self):
        r = self.example()
        self.mutate(r, lambda m: m.update(schema_version="unknown"))
        self.assertTrue(check(r)["structural_gaps"][0].startswith("schema"))


if __name__ == "__main__":
    unittest.main()
