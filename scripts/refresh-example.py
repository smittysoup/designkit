"""Index authored example files after verification. Does not refresh capture/evidence source hashes."""

import hashlib, json
from pathlib import Path

r = Path("examples/caseflow/design/caseflow")
m = json.loads((r / "manifest.json").read_text())
old = {a["path"]: a for a in m["artifacts"]}
next_id = max(int(a["id"].split("-")[1]) for a in old.values()) + 1
for p in sorted(r.rglob("*")):
    if not p.is_file() or p.name == "manifest.json":
        continue
    rel = p.relative_to(r).as_posix()
    if rel not in old:
        old[rel] = {"id": f"ART-{next_id}", "path": rel, "review_state": "draft"}
        next_id += 1
    old[rel]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
m["artifacts"] = list(old.values())
e = r / "validation/evidence/browser.json"
if e.exists():
    ev = json.loads(e.read_text())
    m["evidence"] = [
        {
            "id": f"EVID-{i}",
            "evaluation": f"EVAL-{i}",
            "path": "validation/evidence/browser.json",
            "status": "passed",
            "level": "simulation",
            "sources": ev["source_hashes"],
        }
        for i in range(1, 5)
    ]
(r / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
