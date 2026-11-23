# Verification and release checks

Local evidence on 2026-11-23: macOS arm64, Python 3.12.7; 15 focused unittest
cases passed. Chrome 157.0.8103.79 driven by Playwright 1.58.2 passed 14 browser
assertions and produced eight real desktop/mobile captures. The rendered entity,
data-flow and current/future process diagrams and desktop/mobile captures were
visually inspected for readable labels, layout and control visibility.

```sh
python -m pip install .
python -m unittest discover -s tests -v
npm ci --ignore-scripts
# Either install the bundled browser:
npx playwright install chromium
npm run test:browser
# Or use local Chrome on macOS:
CHROME_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' npm run test:browser
npm run diagrams
python scripts/refresh-example.py
```

Diagram rendering uses local Chrome by default; set CHROME_PATH for another
reviewed executable. The example index refresh records artifact hashes but never
refreshes evidence source hashes. Regenerate captures/renders after relevant
changes. Tests intentionally reject the synthetic example as ready while accepting
its structural evidence; Q-1 and four human reviews remain outstanding.

Coverage includes fresh/existing setup, two initiatives, spaces, collisions,
reruns, edited-file retention, symlink/traversal rejection, missing/heading-only
models, missing evaluation plan, authority gaps, duplicate/unresolved IDs, flow
coverage, stale captures/evidence, fictional/stale reviews, partial export and
model/contract drift. Browser execution covers question/answer/resume, reload,
role controls, human decision, requirement revision, phase inspection, tool outage,
retry/cancellation, keyboard focus and mobile overflow.

The inactive template `docs/checks-workflow.yml` defines core tests/build on Ubuntu
Python 3.11/3.12 and browser tests on Ubuntu Chromium. Initial publication could
not install it: the connected GitHub OAuth credential lacks `workflow` scope.
No CI run is claimed. An authorized credential with that scope can copy it to
`.github/workflows/checks.yml`. Only a completed run establishes CI success. Windows and live
native coding agents are not verified. No live business agent or production service
was tested. Hash gates cannot prove prose semantics or genuine human review.

Release from a reviewed commit: `python -m build`; inspect wheel/sdist contents,
install the wheel into a fresh environment and exercise init/guide/status. Use
`designkit export` for a versioned CaseFlow ZIP. Keep source briefs, dependencies,
credentials and local working environments outside the public commit.
