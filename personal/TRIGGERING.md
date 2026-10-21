# Conversation-start guidance

## Diagnosis

The real-project observation showed the skill in discovery metadata, but no body read in the main conversation or its four identified subagents. Project workflow skills were read. This establishes a selection miss, not an installation failure or a demonstrated framework conflict.

The earlier description emphasized general communication and did not explicitly name code review. This could weaken matching, but the records do not establish the model's exact selection rationale. The fundamental limitation is that `allow_implicit_invocation: true` permits selection; it does not require the body to load.

## Required behavior

Load the complete guidance at the start of each conversation, independently of its topic, wording, directory, or project phase. Reuse that context through subsequent messages and work stages. Do not add a new copy on every user prompt, require repeated file reads, or print a recurring activation notice. Context recovery after compaction or resumption may restore needed instructions; that is distinct from per-message injection.

## Canonical skill and startup integration

`personal/skills/ponytail-pragmatic/SKILL.md` is the canonical rule source. The standalone skill remains available for ordinary native discovery or explicit invocation.

For persistent personal defaults in Codex, [the startup installer](scripts/install-codex-startup.py) copies the complete body, without its discovery frontmatter, into a marked section of the user's global `AGENTS.md`. It records the source path and SHA-256. Codex loads global instructions through its normal startup instruction chain, so the body is already in context even when the model does not select a skill from its catalog.

This is one startup instruction section, not a `UserPromptSubmit` hook. The header carries the once-loaded context across planning, analysis, implementation, review, and handoff. The skill's coding-specific guidance applies only when relevant; communication preferences remain subject to the user's requested depth, language, and format.

## Installation and updates

First install the standalone skill from the same fork revision. From that revision's checkout, run:

```sh
python3 personal/scripts/install-codex-startup.py
python3 personal/scripts/install-codex-startup.py --check
```

The default Codex home is `$CODEX_HOME` when set, otherwise `~/.codex`. Use `--codex-home /path/to/profile` for another profile. Existing guidance outside the managed markers is preserved. Previous contents are backed up locally under the profile's `backups/ponytail-pragmatic/` directory. Repeated installation is idempotent. `--check` does not write files.

The installer refuses a missing or different installed skill revision, malformed or duplicate markers, a symlinked target, and a nonempty global `AGENTS.override.md` that would take precedence. Resolve these conditions rather than silently writing an inactive or unrelated file.

After updating the skill, synchronize startup guidance again. Start a fresh conversation to verify its initial context. Existing conversations may retain their original instructions until the host refreshes or restores context. Do not treat editing an instruction file as proof that all already-running conversations changed.

## Project and harness boundaries

The startup block remains subject to the host's instruction hierarchy, the user's current requirements, and more specific applicable project or role instructions. It preserves project phases, delegation, records, comments, output formats, verification requirements, and execution permissions. It does not create a competing workflow, change a model setting, or enable a lifecycle hook.

When authorized delegation is used, pass the companion context to recipients that do not inherit it, or have them read the advertised skill file. Do not assume every host forwards the parent context. The guidance does not itself authorize delegation.

This setup applies to supported local Codex sessions using the configured Codex home. It is not a claim that arbitrary cloud accounts, other profiles, or unrelated AI products load this local file. Keep global guidance within the host's instruction-size limits; inspect the actual incoming context when diagnosing discovery or truncation.

## Verification

For startup integration, inspect incoming global instruction messages for the full marked body and the recorded source hash. Compare the embedded body with the installed canonical body. A separate `cat SKILL.md` command is unnecessary when those complete instructions are already present.

For skill-only installation, confirm successful reads of `SKILL.md` after normal requests that do not name it. A catalog entry, a self-reported claim, or a concise final answer alone is insufficient loading evidence.

Test a normal opening with no coding or review keywords, then a follow-up in the same conversation. Check reuse rather than a second appended block. Also test real-project development and review requests, with their actual project guidance, output format, and permission boundaries. Record loading evidence separately from the correctness of generated reviews or patches.

The original project's conversation is a historical observation. Use separate controlled verification chats rather than sending unrequested messages to an active project conversation.

## Observed validation on 2026-10-21

- Nine offline installer tests passed: complete-body generation, preservation of unrelated guidance and CRLF bytes, idempotence, read-only stale checks, malformed markers, active overrides, installed-revision mismatch, backups, and symlink refusal.
- A fresh native Codex Desktop chat in a real project began with a normal work-planning request containing no skill, implementation, or review keywords. Its initial instruction message contained one complete canonical body, the matching source hash, and the complete project-root instructions.
- A second turn in that same chat reused the initial context. The complete body still appeared in only one instruction message, neither turn executed a command or reread the skill, and the requested JSON-only follow-up was returned exactly.
- Two earlier real-project development and review probes used the intermediate explicit companion-routing rule. Both read the same canonical body successfully and retained project workflows; the development proposal kept the project's multiline JSDoc. Those probes were not fresh-start tests of the later full-body mechanism and are recorded separately.
- The ten project instruction and harness files included in the before/after comparison were unchanged. The probes did not edit files or run the forbidden verification commands.

These are observed startup, reuse, and coexistence results, not statistical reliability measurements or proof of every model, profile, subagent, compaction, or recovery path. Private conversation records and project-specific evidence are retained locally rather than published in this fork.

References: [global instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [skill selection](https://learn.chatgpt.com/docs/build-skills), and [requiring skills through instruction files](https://developers.openai.com/blog/skills-agents-sdk).
