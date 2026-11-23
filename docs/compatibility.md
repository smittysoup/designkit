# Compatibility and limits

| Surface | Evidence | Supported claim |
|---|---|---|
| Python 3.12.7 / macOS arm64 | Installed package, 15 regression tests, paths with spaces | Tested local CLI |
| Python >=3.11 | Declared syntax/runtime floor | CI template supplied; not installed because OAuth workflow scope is unavailable |
| Codex | `.agents/skills/designkit-*/SKILL.md` generated and checked against pinned upstream delivery | Scaffold verified; `$designkit-discover` in an agent session; live native invocation untested |
| Claude Code | `.claude/skills/designkit-*/SKILL.md` generated and checked | Scaffold verified; `/designkit-discover`; live native invocation untested |
| Generic assistant | `designkit guide discover --root ... --initiative ...` prints portable instructions | This authoring assistant applied the methodology to CaseFlow; not a native adapter run |
| Spec Kit | 1.4.5.dev0, SHA `5fd2d2a97bac4f449cdb4efff4d64a12804d7b36` | Executed setup/script fixtures and explicit bridge regression tests |
| Browser | Chrome 157.0.8103.79 / Playwright 1.58.2 | 14 assertions, 8 actual captures, desktop and emulated mobile |
| Windows / PowerShell | Not executed locally | No Windows verification claim; Python implementation avoids shell setup |
| Live business agents | Not run | Simulation only; production eval plan supplied |
| Figma | No adapter | Coded prototype boundary only; no creation/sync promise |

Seven capability names describe iterative authoring work, not a runtime engine.
Generated skills require the target assistant to discover repository skills and
follow instructions. They cannot guarantee model compliance. No hosted dashboard,
collaboration service, authentication or production task scheduler is included.

Install/update is local to an explicit root. Review generated diffs before adopting
new toolkit versions. Edited files block update; reconcile manually while retaining
your changes, then rerun. Uninstall retains edited files and all initiative work.
Never force-upgrade Spec Kit merely to import a DesignKit package. Keep the source
model and contracts, run the bridge into a new feature/version, and review differences.
