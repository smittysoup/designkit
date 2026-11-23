# Spec Kit mechanics audit

Investigated 2026-11-23, before choosing DesignKit packaging. Canonical repository:
[github/spec-kit](https://github.com/github/spec-kit), MIT (Copyright GitHub, Inc.).
Pinned current main **5fd2d2a97bac4f449cdb4efff4d64a12804d7b36**, package
**1.4.5.dev0**, `git describe`: `v0.1.10-1933-g5fd2d2a9`. This is a development
commit, not a claim of compatibility with every release. Host: Darwin 23.4.0 arm64,
Python 3.12.7. Upstream requires Python >=3.11.

## Evidence and source map

The upstream AGENTS.md and CONTRIBUTING.md were read; no upstream code was edited.
There was no upstream `.agents/` instruction directory. Official
[core CLI docs](https://github.github.com/spec-kit/overview/core.html) and
[integrations index](https://github.github.io/spec-kit/integrations/index.html)
were consulted. The following paths are relative to this
[immutable tree](https://github.com/github/spec-kit/tree/5fd2d2a97bac4f449cdb4efff4d64a12804d7b36).

| Concern | Inspected source | Finding |
|---|---|---|
| CLI/distribution | `pyproject.toml`, `src/specify_cli/command_init.py` | `specify = specify_cli:main`; wheel bundles core assets through Hatch force-include. Local wheel installation supports offline initialization. |
| Native delivery | `src/specify_cli/integrations/codex/__init__.py`, `claude/__init__.py` | Both use SKILL.md; Codex under `.agents/skills`, Claude under `.claude/skills`. |
| Plan source | `templates/commands/plan.md`, `templates/plan-template.md` | Frontmatter declares script variants and handoffs. Plan asks the assistant to derive model and contracts. |
| Context/script | `scripts/python/setup_plan.py`, `scripts/python/common.py` | Explicit feature directory selection; setup copies a plan template only when absent. It does not execute LLM modeling. |
| Template resolution | `scripts/python/common.py:resolve_template` | Local overrides, ordered presets, extensions, then core templates. Content composition has additional layer handling. |
| Lifecycle | `src/specify_cli/integrations/command_upgrade.py`, `command_uninstall.py`, `integration_state.py` | Managed hashes distinguish modified files; upgrade blocks edits without force; uninstall retains modified files by default. |
| Extensions | `src/specify_cli/extensions/`, `presets/`, `workflows/`, `bundles/` | Separate mechanisms for additional commands, template changes, orchestration and packaged setups. Not required by the chosen bridge. |
| Generated context | installed `.specify/memory/constitution.md`, `.specify/feature.json`, `extensions/agent-context/` | Constitution and explicit feature context matter. Agent-context is a bundled optional extension, not a reason to edit global configuration. |
| Distribution automation | `.github/workflows/publish-pypi.yml`, `.github/workflows/RELEASE-PROCESS.md` | Publication has its own upstream release process; DesignKit does not fork it. |

## Executed disposable fixtures

Commands were run in a dedicated workspace; quoted names intentionally contain spaces.
`SPECIFY_FEATURE_DIRECTORY` selects the feature independently of Git branches;
`SPECIFY_FEATURE_NO_PERSIST=1` avoids changing the shared current-feature pointer.

```sh
git clone https://github.com/github/spec-kit.git spec-kit-audit
git -C spec-kit-audit rev-parse HEAD
# Confirm the exact pin above before installing.
python3.12 -m venv audit-venv
audit-venv/bin/pip install ./spec-kit-audit
audit-venv/bin/specify init 'audit fresh' --integration codex --script py \
  --ignore-agent-tools --non-interactive --offline
# Inside an existing disposable project:
specify init --here --force --non-interactive --integration codex \
  --script py --ignore-agent-tools --offline
specify integration install claude
# In each selected feature (001-first, 002-second):
SPECIFY_FEATURE_DIRECTORY="$PWD/specs/001-first" SPECIFY_FEATURE_NO_PERSIST=1 \
  python .specify/scripts/python/setup_plan.py --json
specify integration upgrade codex
```

| Fixture | Observed result | Level |
|---|---|---|
| Fresh Codex initialization, path with spaces | Exit 0; `.specify` assets and native plan skill materialized | Executed CLI |
| Existing project adoption with Claude | Exit 0; authored AGENTS.md remained byte-identical | Executed CLI |
| Forced rerun after edits | AGENTS.md and constitution preserved; customized core plan template **overwritten** | Executed before/after content comparison |
| Add Claude alongside Codex | Exit 0; default remained Codex; existing shared infrastructure skipped | Executed CLI |
| Two explicit feature directories | Plan setup selected each correctly; no cross-write; existing plan, model and contract remained intact on rerun | Executed Python script |
| Upgrade after editing generated Codex skill | Exit 1; blocked modified skill; authored bytes preserved | Executed CLI |
| Downstream model/contract generation | Template instructions inspected; plan setup does not produce them | Source + fixture; no live agent |

## Complete plan delivery trace

1. `templates/commands/plan.md` is bundled as `specify_cli/core_pack/commands` by
   the wheel build; scripts and page templates are bundled separately.
2. `specify init ... --integration codex --script py` renders
   `.agents/skills/speckit-plan/SKILL.md`, with name, description and version
   metadata. The rendered file contains `python3 .specify/scripts/python/setup_plan.py --json`
   and the concrete `.specify/memory/constitution.md` path.
3. Native invocation is `$speckit-plan` in Codex, `/speckit-plan` in Claude,
   not a terminal command. Claude's generated skill was also inspected.
4. The helper resolves project and feature context and returns FEATURE_SPEC,
   IMPL_PLAN, FEATURE_DIR and BRANCH. Existing plan content is retained.
5. The authoring agent is instructed to read spec, constitution and plan, then
   produce research, `data-model.md`, contracts and quickstart. Those outputs are
   not automatically reconciled with an external transformation package.
6. DesignKit therefore supplies explicit input context and a separate conservative
   reconciliation check. A missing or changed downstream model/contract blocks
   conformance until the difference has a recorded review.

## Limits

No live Codex/Claude executable was available on PATH. No native agent invocation,
upstream LLM plan, extension/preset lifecycle, Windows PowerShell, or Linux upstream
setup was exercised. Hook text is not enforcement. Source-inspected uninstall
behavior is not an executed removal claim. Same-version rerun/upgrade was exercised;
a migration between upstream releases was not. Re-run this audit before widening
the compatibility pin. The checked-in DesignKit bridge tests exercise file
preservation and drift, not automatic semantic understanding.
