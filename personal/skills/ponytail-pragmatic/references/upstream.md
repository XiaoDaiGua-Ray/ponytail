# Upstream provenance and adaptation notes

Derived from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), version 5.3.2, at commit `09c434ab73ca43761c5d8b0c5d341926c2fba710`.

The primary source is [skills/ponytail/SKILL.md](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md). The adaptation also draws on the compact rules in [AGENTS.md](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/AGENTS.md) and the loading design in [ponytail-instructions.js](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-instructions.js), which reads the core skill and filters it for the selected mode.

| Upstream rule | Adaptation |
| --- | --- |
| Read the code and identify callers and affected scope before writing | Retained, with explicit attention to agreed scope and applicable project contracts |
| Six-step preference order for the smallest complete change | Retained: necessity, project reuse, platform capabilities, installed dependencies, direct expression, then minimal implementation |
| Avoid unrequested abstractions, wrappers, and speculative features | Retained; avoiding additions does not authorize deleting existing behavior |
| Preserve existing structure and inspect callers when fixing bugs | Retained, including legitimate differences between caller contracts |
| Preserve validation, data-loss prevention, security, accessibility, and hardware calibration | Retained, alongside required compatibility, performance, and behavior |
| Leave a small test for nontrivial logic | Adapted to risk and existing coverage, within editing and command authorization; project-required checks still apply |
| Use one-line comments and a fixed shortcut marker | Replaced with the applicable project's comment and limitation-recording conventions |
| End every reply with skipped checks and risks | Replaced with relevant verification boundaries and material limitations, subject to the requested output format |
| Coding persona, intensity levels, and a session-wide mode | Replaced with task-sensitive communication and implementation preferences |
| Inject the rules through host hooks | Replaced by native skill discovery and invocation for this standalone adaptation |

## Installation and coexistence

The maintained adaptation lives at `personal/skills/ponytail-pragmatic/`. Installing that directory includes the entrypoint, UI metadata, this reference, and the upstream MIT license. It has a distinct skill name and does not install hooks.

Upstream `skills/ponytail/`, the root `AGENTS.md`, and the original adapters remain available for comparison and future merges. The original plugin entry points still load the upstream rules, not this adaptation; cloning the fork is not the same as installing the standalone skill. An agent working inside the clone may also receive its upstream project instructions.

If original Ponytail rules, plugins, or hooks are enabled separately, they can coexist with this skill and introduce conflicting preferences. This skill neither detects nor disables them. Inspect the host's active configuration when diagnosing such a conflict; do not assume that installing this skill replaces the original plugin.

`allow_implicit_invocation: true` permits automatic selection of the standalone skill. It does not guarantee selection on every request, activation in every host, or injection into subagents. This fork also provides an optional conversation-start integration outside the standalone skill directory: it synchronizes the complete canonical body into one managed global Codex instruction block. That path supplies the body without relying on catalog selection; it does not install a per-message hook. See `personal/TRIGGERING.md` in the fork for installation and validation boundaries.

## Maintenance boundaries

Compare upstream core-rule changes before adopting them. Incorporate only changes consistent with this skill's purpose and instruction boundaries. Preserve the original copyright and MIT license. Do not automatically overwrite the adaptation or present upstream benchmark percentages as measurements of this version.

Compatibility relies on following the current task's authoritative project and role requirements under the host's instruction hierarchy. It is not tied to a framework name and does not provide runtime adapters or certify compatibility with every harness. Keep behavioral evaluations separate from claims about actual host discovery, automatic invocation, or runtime integration.
