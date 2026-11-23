"""Local, explicit-scope DesignKit CLI. No network or agent runtime."""

from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from importlib.resources import files
from jsonschema import Draft202012Validator
from . import __version__

ASSETS = Path(str(files("designkit") / "assets"))
CAPABILITIES = (
    "discover",
    "envision",
    "prototype",
    "validate",
    "model",
    "contract",
    "handoff",
)
PIN = "5fd2d2a97bac4f449cdb4efff4d64a12804d7b36"
REQUIRED = {
    "brd.md": [
        "Outcomes",
        "Functional requirements",
        "Non-functional requirements",
        "Rules",
        "Acceptance",
    ],
    "decisions.md": ["Decisions"],
    "open-questions.md": ["Questions"],
    "transformation/current-process.md": ["Baseline", "Actors", "Work", "Exceptions"],
    "transformation/agentic-process.md": ["Redesign", "Authority", "Recovery"],
    "transformation/agent-catalog.md": [
        "Outcome",
        "Knowledge",
        "Tools",
        "State",
        "Completion",
        "Intervention",
    ],
    "transformation/evaluation-plan.md": ["Scenarios", "Measures", "Verification"],
    "experience/journeys.md": ["Journey", "Alternatives"],
    "experience/design-guidance.md": ["Interaction", "Responsive", "Accessibility"],
    "architecture/data-model.md": [
        "Entities",
        "Relationships",
        "Ownership",
        "Invariants",
        "Lifecycle",
        "Data movement",
    ],
    "architecture/state-transitions.md": ["Transitions"],
    "architecture/contracts/README.md": [
        "Operations",
        "Authority",
        "Errors",
        "Versioning",
    ],
    "validation/report.md": ["Observed", "Simulated", "Limitations"],
    "handoff/speckit-input.md": ["Scope", "Inputs", "Reconciliation"],
    "handoff/reconciliation.md": ["Mappings", "Differences"],
    "constitution.md": ["Principles"],
    "architecture/diagrams/entity-model.mmd": [],
    "architecture/diagrams/data-flow.mmd": [],
    "architecture/diagrams/process-flows/current-process.mmd": [],
    "architecture/diagrams/process-flows/agentic-process.mmd": [],
    "architecture/contracts/operations.json": [],
    "experience/screens.json": [],
    "handoff/traceability.json": [],
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dumps(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe(root, relative):
    root = root.resolve()
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise ValueError(f"Unsafe relative path: {relative}")
    p = root / rel
    for part in [p, *p.parents]:
        if part == root:
            break
        if part.is_symlink():
            raise ValueError(f"Symlink not allowed: {relative}")
    if not p.resolve().is_relative_to(root):
        raise ValueError("Path escapes root")
    return p


def write_new(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        f.write(content)


def initiative(root, name):
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", name):
        raise ValueError("Initiative must be a lowercase slug")
    return safe(root, f"design/{name}")


def install(root, adapter):
    """Preflight entire managed set before any changes; preserve edited files."""
    root = root.resolve()
    ledger_path = safe(root, ".designkit/installed.json")
    ledger = read(ledger_path) if ledger_path.exists() else {}
    desired = {}
    for cap in CAPABILITIES:
        body = (ASSETS / "commands" / f"{cap}.md").read_text()
        desired[f".designkit/commands/{cap}.md"] = body
        if adapter != "generic":
            prefix = ".agents" if adapter == "codex" else ".claude"
            desired[f"{prefix}/skills/designkit-{cap}/SKILL.md"] = (
                f'---\nname: designkit-{cap}\ndescription: Transform business processes through {cap}; select an initiative explicitly.\nmetadata:\n  version: "{__version__}"\n---\n\n'
                + body
            )
    desired[".designkit/AGENTS.designkit.md"] = (ASSETS / "consumer.md").read_text()
    conflicts = []
    for rel, content in desired.items():
        p = safe(root, rel)
        if (
            p.exists()
            and digest(p) != hashlib.sha256(content.encode()).hexdigest()
            and digest(p) != ledger.get(rel)
        ):
            conflicts.append(rel)
    if conflicts:
        raise ValueError(
            "Edited or unowned file collision; preserved: " + ", ".join(conflicts)
        )
    for rel, content in desired.items():
        p = safe(root, rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        ledger[rel] = digest(p)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(dumps(ledger))
    return {"installed": len(desired), "adapter": adapter, "version": __version__}


def uninstall(root):
    p = safe(root, ".designkit/installed.json")
    ledger = read(p)
    kept = []
    for rel, h in list(ledger.items()):
        f = safe(root, rel)
        if f.exists() and digest(f) == h:
            f.unlink()
            del ledger[rel]
        elif f.exists():
            kept.append(rel)
        else:
            del ledger[rel]
    p.write_text(dumps(ledger))
    return {"retained_edited": kept, "initiative_files": "preserved"}


def init(root, name, process, outcome, adapter):
    dest = initiative(root, name)
    if dest.exists():
        raise ValueError(
            "Initiative already exists; use status or update. Nothing overwritten."
        )
    install(root, adapter)
    manifest = read(ASSETS / "manifest.template.json")
    manifest["initiative"] = {
        "id": name,
        "process": process,
        "outcome": outcome,
        "scope": process,
        "synthetic": False,
    }
    for rel in REQUIRED:
        source = ASSETS / "templates" / rel
        write_new(safe(dest, rel), source.read_text())
    write_new(dest / "manifest.json", dumps(manifest))
    return {"initiative": str(dest), "readiness": "not_ready"}


def artifact_revision(root, paths):
    return hashlib.sha256(
        dumps(
            {p: digest(safe(root, p)) for p in sorted(paths) if safe(root, p).is_file()}
        ).encode()
    ).hexdigest()


def check(root):
    m = read(root / "manifest.json")
    gaps = []
    schema = read(ASSETS / "manifest.schema.json")
    for e in Draft202012Validator(schema).iter_errors(m):
        gaps.append("schema " + ".".join(map(str, e.path)) + ": " + e.message)
    if gaps:
        return {"readiness": "not_ready", "structural_gaps": gaps, "review_gaps": []}
    for rel, schema_file in (
        ("experience/screens.json", "screens.schema.json"),
        ("handoff/traceability.json", "traceability.schema.json"),
    ):
        candidate = safe(root, rel)
        if candidate.exists():
            for error in Draft202012Validator(read(ASSETS / schema_file)).iter_errors(
                read(candidate)
            ):
                gaps.append("schema " + rel + ": " + error.message)
    if gaps:
        return {"readiness": "not_ready", "structural_gaps": gaps, "review_gaps": []}
    arts = m["artifacts"]
    paths = {a["path"] for a in arts}
    ids = [a["id"] for a in arts]
    for rel, heads in REQUIRED.items():
        if rel not in paths:
            gaps.append("Unindexed required artifact: " + rel)
        p = safe(root, rel)
        if not p.is_file():
            gaps.append("Missing artifact: " + rel)
            continue
        txt = p.read_text()
        if rel.endswith(".md"):
            if (
                len(
                    " ".join(
                        l for l in txt.splitlines() if not l.startswith("#")
                    ).strip()
                )
                < 100
                or "TODO" in txt
            ):
                gaps.append("Incomplete substantive content: " + rel)
            for h in heads:
                if not re.search(r"^## " + re.escape(h) + r"\s*$", txt, re.M):
                    gaps.append("Missing section " + h + ": " + rel)
    for a in arts:
        p = safe(root, a["path"])
        if not p.is_file():
            gaps.append("Broken artifact: " + a["path"])
        elif a["sha256"] != digest(p):
            gaps.append("Stale artifact hash: " + a["path"])
        if a["review_state"] not in ("draft", "in_review", "accepted"):
            gaps.append("Invalid review state: " + a["id"])
    trace_path = root / "handoff/traceability.json"
    if trace_path.exists() and read(trace_path) != m["records"]:
        gaps.append("Traceability index differs from manifest records")
    for diagram in ("entity-model", "data-flow", "current-process", "agentic-process"):
        rel = "architecture/diagrams/rendered/" + diagram + ".svg"
        if rel not in paths or not safe(root, rel).is_file():
            gaps.append("Missing rendered diagram: " + diagram)
    render_sources = root / "architecture/diagrams/rendered/sources.json"
    if not render_sources.exists():
        gaps.append("Missing diagram source provenance")
    else:
        for item in read(render_sources):
            source = safe(root, item["source"])
            if not source.is_file() or digest(source) != item["sha256"]:
                gaps.append("Stale diagram render: " + item["source"])
            if not safe(root, item["output"]).is_file():
                gaps.append("Missing diagram render: " + item["output"])
    operations_path = root / "architecture/contracts/operations.json"
    if operations_path.exists():
        ops = read(operations_path)
        if not isinstance(ops, dict) or not ops.get("operations"):
            gaps.append("Missing callable operation schemas")
        else:
            for op in ops["operations"]:
                if not all(
                    op.get(k)
                    for k in (
                        "id",
                        "caller",
                        "input",
                        "output",
                        "errors",
                        "idempotency",
                    )
                ):
                    gaps.append("Incomplete callable operation schema")
    records = m["records"]
    ids += [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        gaps.append("Duplicate stable IDs")
    known = set(ids)
    byid = {r["id"]: r for r in records}
    for r in records:
        if r["path"] not in paths:
            gaps.append("Unindexed record home: " + r["id"])
        elif (
            safe(root, r["path"]).exists()
            and r["id"] not in safe(root, r["path"]).read_text()
        ):
            gaps.append("ID absent from canonical home: " + r["id"])
        for ref in r["refs"]:
            if ref not in known:
                gaps.append("Unresolved reference " + ref + " from " + r["id"])
    for kind in (
        "outcome",
        "current_step",
        "future_step",
        "requirement",
        "nfr",
        "agent",
        "human",
        "tool",
        "flow",
        "entity",
        "operation",
        "evaluation",
        "screen",
    ):
        if not any(r["kind"] == kind for r in records):
            gaps.append("Missing record kind: " + kind)
    for r in records:
        linked = {byid[x]["kind"] for x in r["refs"] if x in byid}
        required = {
            "current_step": {"future_step"},
            "requirement": {"evaluation", "screen"},
            "flow": {"entity", "operation"},
            "agent": {"tool", "evaluation"},
            "evaluation": {"requirement"},
        }.get(r["kind"], set())
        if not required <= linked:
            gaps.append("Incomplete trace coverage: " + r["id"])
        if r["kind"] == "agent" and not all(
            r.get(k)
            for k in ("authority", "completion", "intervention", "knowledge", "state")
        ):
            gaps.append("Undefined agent boundary: " + r["id"])
        if r["kind"] == "operation" and not all(
            r.get(k) for k in ("authority", "input", "output", "errors", "idempotency")
        ):
            gaps.append("Undefined operation contract: " + r["id"])
        if r["kind"] == "human" and not r.get("authority"):
            gaps.append("Unowned human authority: " + r["id"])
        if r["kind"] == "future_step" and not all(
            r.get(k) for k in ("disposition", "rationale")
        ):
            gaps.append("Missing redesign rationale: " + r["id"])
        if r["kind"] == "nfr" and not all(
            r.get(k) for k in ("acceptance", "owner", "verification")
        ):
            gaps.append("Unowned material NFR: " + r["id"])
    screens = (
        read(root / "experience/screens.json")
        if (root / "experience/screens.json").exists()
        else []
    )
    for s in screens:
        for field in (
            "id",
            "state",
            "route",
            "fixture",
            "viewport",
            "captured_at",
            "capture",
            "source",
            "source_sha256",
            "requirements",
        ):
            if not s.get(field):
                gaps.append("Missing screen metadata " + field)
        if s.get("id") not in known:
            gaps.append("Unresolved screen ID")
        for key in ("capture", "source"):
            if not s.get(key) or not safe(root, s[key]).is_file():
                gaps.append("Broken screen " + key)
        if (
            s.get("source")
            and safe(root, s["source"]).is_file()
            and digest(safe(root, s["source"])) != s.get("source_sha256")
        ):
            gaps.append("Stale screen source: " + s["id"])
    if not screens:
        gaps.append("Missing captured screens")
    for e in m["evidence"]:
        if e["status"] != "passed":
            gaps.append("Evidence not passed: " + e["id"])
        if e["evaluation"] not in byid:
            gaps.append("Unknown evidence evaluation: " + e["id"])
        if not safe(root, e["path"]).is_file():
            gaps.append("Missing evidence: " + e["id"])
        for rel, h in e["sources"].items():
            if not safe(root, rel).is_file() or digest(safe(root, rel)) != h:
                gaps.append("Stale evidence: " + e["id"])
    for r in records:
        if r["kind"] == "evaluation" and not any(
            e["evaluation"] == r["id"] for e in m["evidence"]
        ):
            gaps.append("Evaluation not executed: " + r["id"])
    for q in m["questions"]:
        if not q["owner"]:
            gaps.append("Unowned question: " + q["id"])
        if q["blocking"] and q["status"] != "resolved":
            gaps.append("Blocking question: " + q["id"])
    # Review hashes are scoped: unrelated changes need not invalidate every review.
    review_gaps = []
    for role in ("business", "product", "experience", "engineering"):
        rs = [r for r in m["reviews"] if r["role"] == role]
        if not rs:
            review_gaps.append("Missing human review: " + role)
        for r in rs:
            role_paths = {
                "business": [
                    "transformation/current-process.md",
                    "transformation/agentic-process.md",
                    "transformation/agent-catalog.md",
                ],
                "product": ["brd.md", "transformation/evaluation-plan.md"],
                "experience": [
                    "experience/journeys.md",
                    "experience/screens.json",
                    "experience/prototype/app.js",
                ],
                "engineering": [
                    "architecture/data-model.md",
                    "architecture/contracts/operations.json",
                ],
            }[role]
            if not set(role_paths) <= set(r["paths"]):
                review_gaps.append("Incomplete review scope: " + role)
            if (
                r["status"] != "accepted"
                or not r["reviewer"]
                or r["synthetic"]
                or not r["paths"]
                or r["revision"] != artifact_revision(root, r["paths"])
            ):
                review_gaps.append("Missing, fictional or stale human review: " + role)
            if not r["evidence"] or not safe(root, r["evidence"]).is_file():
                review_gaps.append("Missing review evidence: " + role)
    return {
        "readiness": "ready" if not gaps and not review_gaps else "not_ready",
        "structural_gaps": sorted(set(gaps)),
        "review_gaps": sorted(set(review_gaps)),
        "scope": m["initiative"]["scope"],
        "revision": artifact_revision(root, paths),
    }


def snapshot(root, destination):
    report = check(root)
    m = read(root / "manifest.json")
    paths = {a["path"] for a in m["artifacts"]}
    # Export only declared initiative artifacts, never arbitrary repository files.
    paths.add("manifest.json")
    for s in read(root / "experience/screens.json"):
        paths.update([s["source"], s["capture"]])
    for e in m["evidence"]:
        paths.add(e["path"])
    if destination.exists():
        raise ValueError("Export exists; choose a new versioned destination")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "x", zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(paths):
            p = safe(root, rel)
            if p.is_file():
                z.write(p, rel)
        z.writestr(
            "export.json",
            dumps(
                {
                    "schema_version": "1.0",
                    "toolkit": __version__,
                    "source_hashes": {
                        p: digest(safe(root, p))
                        for p in paths
                        if safe(root, p).is_file()
                    },
                    "assessment": report,
                }
            ),
        )
    return report


def bridge(root, target):
    if target.is_symlink():
        raise ValueError("Symlink target not allowed")
    target.mkdir(parents=True, exist_ok=True)
    dest = safe(target, "designkit-input")
    if dest.exists():
        raise ValueError(
            "Bridge input exists; use a new feature or version. Source preserved."
        )
    report = check(root)
    m = read(root / "manifest.json")
    # Immutable copy, with explicit downstream mappings, never overwrites model/contracts.
    dest.mkdir()
    mapping = []
    for a in m["artifacts"]:
        src = safe(root, a["path"])
        if src.is_file():
            out = safe(dest, a["path"])
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, out)
            if a["path"] == "architecture/data-model.md" or a["path"].startswith(
                "architecture/contracts/"
            ):
                downstream = a["path"].removeprefix("architecture/")
                mapping.append(
                    {
                        "source": a["path"],
                        "source_sha256": digest(src),
                        "target": downstream,
                    }
                )
    state = {
        "schema_version": "1.0",
        "spec_kit_commit": PIN,
        "initiative": m["initiative"]["id"],
        "readiness": report["readiness"],
        "mappings": mapping,
    }
    (dest / "bridge.json").write_text(dumps(state))
    (dest / "manifest.json").write_text(dumps(m))
    write_new(
        dest / "speckit-input.md",
        "# Explicit DesignKit context\n\nRead manifest.json and all linked transformation, BRD, experience, architecture and validation inputs before specification/planning. Preserve stable IDs and human authority. Canonical data-model.md is architecture/data-model.md. Derive downstream data-model.md and contracts/ without changing these inputs. Record every refinement in reconciliation.json; human semantic changes require a named decision and evidence. Run designkit reconcile after planning.\n\nReadiness: "
        + report["readiness"]
        + "\n",
    )
    return state


def reconcile(target):
    dest = safe(target, "designkit-input")
    state = read(dest / "bridge.json")
    decisions = (
        read(target / "reconciliation.json")
        if (target / "reconciliation.json").exists()
        else []
    )
    gaps = []
    rows = []
    for m in state["mappings"]:
        src = safe(dest, m["source"])
        out = safe(target, m["target"])
        if not src.exists() or digest(src) != m["source_sha256"]:
            gaps.append("Frozen source altered: " + m["source"])
            continue
        if not out.exists():
            gaps.append("Missing downstream: " + m["target"])
            continue
        h = digest(out)
        same = h == m["source_sha256"]
        accepted = any(
            d.get("target") == m["target"]
            and d.get("source_sha256") == m["source_sha256"]
            and d.get("target_sha256") == h
            and d.get("status") == "accepted"
            and d.get("reviewer")
            and d.get("reason")
            and d.get("affected_ids")
            and d.get("evidence")
            and safe(target, d["evidence"]).is_file()
            and not d.get("synthetic", True)
            for d in decisions
        )
        if not same and not accepted:
            gaps.append("Unreviewed model/contract difference: " + m["target"])
        rows.append(
            {
                "target": m["target"],
                "source_sha256": m["source_sha256"],
                "target_sha256": h,
                "state": "identical"
                if same
                else "accepted_refinement"
                if accepted
                else "conflict",
            }
        )
    return {
        "conformant": not gaps,
        "gaps": gaps,
        "mappings": rows,
        "semantic_review": "Human responsibility; hashes cannot establish meaning",
    }


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Transform business processes into AI-native agent operating models"
    )
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    for cmd in (
        "init",
        "update",
        "uninstall",
        "check",
        "status",
        "export",
        "bridge",
        "guide",
    ):
        c = sub.add_parser(cmd)
        c.add_argument("--root", type=Path, default=Path.cwd())
        if cmd in ("init", "check", "status", "export", "bridge", "guide"):
            c.add_argument("--initiative", required=True)
        if cmd in ("init", "update"):
            c.add_argument(
                "--adapter", choices=("generic", "codex", "claude"), default="generic"
            )
        if cmd == "init":
            c.add_argument("--process", required=True)
            c.add_argument("--outcome", required=True)
        if cmd == "export":
            c.add_argument("--output", required=True, type=Path)
        if cmd == "bridge":
            c.add_argument("--feature-dir", required=True, type=Path)
        if cmd == "guide":
            c.add_argument("capability", choices=CAPABILITIES)
    c = sub.add_parser("reconcile")
    c.add_argument("--feature-dir", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        cmd = args.command
        if cmd == "init":
            result = init(
                args.root, args.initiative, args.process, args.outcome, args.adapter
            )
        elif cmd == "update":
            result = install(args.root, args.adapter)
        elif cmd == "uninstall":
            result = uninstall(args.root)
        elif cmd == "reconcile":
            result = reconcile(args.feature_dir)
        else:
            root = initiative(args.root, args.initiative)
            if cmd == "guide":
                print(
                    f"Initiative: {root}\n"
                    + (ASSETS / "commands" / f"{args.capability}.md").read_text()
                )
                return 0
            if cmd in ("check", "status"):
                result = check(root)
            elif cmd == "export":
                result = snapshot(root, args.output)
            elif cmd == "bridge":
                result = bridge(root, args.feature_dir)
        print(dumps(result))
        if cmd == "check" and result["readiness"] != "ready":
            return 2
        if cmd == "reconcile" and not result["conformant"]:
            return 2
        return 0
    except (ValueError, OSError, KeyError, TypeError) as e:
        print(f"designkit: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
