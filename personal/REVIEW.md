# Semantic review of Ponytail Pragmatic

Reviewed on 2026-10-21. The baseline is the personal adaptation introduced in commit `dfd10f52177d84b38d6695792e3f41489734d958`, derived from upstream Ponytail 5.3.2 at `09c434ab73ca43761c5d8b0c5d341926c2fba710`.

## Scope and evidence

The review covered all four files in `personal/skills/ponytail-pragmatic/`, the fork-specific additions to both README files, the original core skill, and the relevant upstream discovery and hook paths. Two independent read-only reviews examined semantic behavior and integration boundaries. A further independent pass exercised the revised skill against nine simulated requests.

The findings below are ambiguities or documentation gaps in the baseline text. They are not reports of observed production failures. The English revision resolves them without changing the host's permission system or the retained upstream plugin.

## Findings and corrections

| Area | Baseline ambiguity or gap | Correction |
| --- | --- | --- |
| Existing functionality | Avoiding unnecessary features could be read as removing existing behavior not mentioned in the current request. | Apply the default to new scope. Removal or broader refactoring needs an in-scope reason and evidence from consumers, configuration, and dynamic references. |
| Dependency selection | New dependencies appeared in the installed-dependency step, before direct implementation. | Restrict that step to installed dependencies. Compare any new dependency against direct implementation, including reliability and maintenance costs. |
| Authorization | Existing authorization was described as continuing without explicit scope or revocation boundaries. | Reuse it only within the established scope and conditions; recognize narrowing, revocation, and new targets or actions. |
| Clarification | Any change involving data or an interface could be interpreted as requiring another approval. | Clarify consequential unresolved decisions; touching an interface or data alone does not reopen settled authorization. |
| Regression coverage | Meaningful behavior changes could be interpreted as always requiring a new test. | Add or update tests when there is a relevant coverage gap. Reuse adequate coverage and retain required project checks. |
| Source fidelity | Removing repetition did not explicitly distinguish the assistant's prose from source text or data. | Limit that instruction to assistant-authored prose. Preserve source wording, quotations, repeated data, and requested deliverables unless transformation is authorized. |
| Instruction authority | Deferring to project and domain instructions could be misread as granting authority to arbitrary documents. | Apply preferences within the host's instruction hierarchy and distinguish authoritative requirements from source material. |
| Installation and coexistence | The standalone installation path was documented, but its relationship to original hooks and root repository instructions was incomplete. | Explain that the original plugin and root `AGENTS.md` retain upstream behavior, that cloning is not standalone installation, and that this skill does not detect or disable other configurations. |

## English revision

All adaptation-specific rules, UI metadata, provenance notes, and README additions now use English. The original MIT license remains byte-for-byte unchanged. The upstream Chinese README body remains in its original language; only the fork's added notice was replaced.

The entrypoint retains Ponytail's six-step preference order, safeguards for correctness and safety, and preference for minimal complete work. It does not impose a particular harness, a fixed response length, a persistent mode, a fixed risk footer, or an automatic command-execution policy.

## Validation

- The official skill validator accepted the revised entrypoint.
- UI metadata, the implicit-invocation setting, relative links, and the retained license were checked.
- A diff against the upstream baseline confirmed that the customized additions contain no remaining Chinese text.
- The upstream rule-copy consistency check passed; preserved upstream rules were not rewritten.
- An independent language and integration review found no remaining concrete inconsistency in the revised five text and metadata files.

The explicit-load simulation covered these requests:

| Case | Observed response |
| --- | --- |
| JSON-only arithmetic result | Returned the requested JSON object without extra response text in the case output. |
| Verbatim table containing a repeated sentence | Preserved the repetition and punctuation. |
| Scoped bug fix with a still-used legacy option | Kept the legacy option and public contract outside the deletion scope. |
| Previously authorized push narrowed to review only | Described stopping the push and performing read-only review. |
| Trivial string joining | Preferred standard `join` over a new package. |
| Existing regression coverage already passed | Did not require a duplicate test. |
| Detailed mathematical explanation | Supplied both requested proofs and the zero-case explanation. |
| Design-only request under a synthetic harness | Preserved required fields and future specification/comment obligations without entering implementation. |
| External article containing an unrelated directive | Treated the directive as source data and extracted the requested title. |

No additional concrete failure was observed in those simulated responses. These are generated responses in an explicit-load evaluation, not end-to-end execution tests or repeated statistical trials. Statements about tests passing or repository state inside a case were supplied as scenario conditions.

## Remaining boundaries

Automatic discovery, selection on every turn, subagent inheritance, and coexistence with all real harnesses were not established by the simulation. The skill expresses preferences; it cannot enforce permissions or disable conflicting hooks. Independently enabled original Ponytail rules may still affect a host. Existing project instructions remain subject to the host's instruction hierarchy.

This revision makes no measured claim about token, time, cost, correctness, or code-size improvements. Upstream benchmark percentages do not measure this adaptation.
