# FRAMING: requirements-chain test suite

## Why
The chain skills get reworked, and each rework is redeployed into a real project, a new one or an existing one. Before any redeploy we need confidence the chain will still work where it lands. This suite is that confidence: a pre-deploy regression gate. When a chain skill (bootstrapping-project, framing-project, brainstorming-requirements, writing-requirements) is reworked, the gate proves three things still hold. The skill's own behaviour has not regressed. The seams to its neighbours still hold. And it still behaves in a deployed target context, not only inside skills-lab, where a whole class of bug stays hidden until the skill runs somewhere else. What gets tested follows what gets deployed, and setting that mapping is a QA Lead decision, not a fixed rule.

## For whom
The skill engineer at the moment of release, the author acting as releaser. This is not a design-time reference. That moment sets two bars. The gate has to be fast enough to run before every redeploy. And a failure has to point at one mechanism, so the engineer sees what broke without re-deriving it.

## Success
The gate returns a go/no-go verdict you can trust on every redeploy. Green means the reworked skill is safe to ship. Red means a real regression. Two failure modes shape the design, and they do not cost the same.

- An escaped defect is a green that should have been red. This is the main enemy of a deploy gate. Run 1 did exactly this, a clean 0/0/0 report hid both the Summary-tally defect and the Phase 0.5 repo-root escape.
- A false alarm is a red from flake rather than a real break. Under a non-deterministic chain this is the trust-killer, because a gate that cries wolf gets switched off, and a gate nobody runs is worth nothing.

Indicators. Escaped regressions at zero, checked by seeding a known defect and confirming the gate turns red. We have one such point already, the injected tally defect went red while the rest stayed green. False alarms rare enough that a red is always believed. And a cost cheap enough to run on every redeploy. That is what efficient has to mean here, the condition for the gate to be run at all, not a virtue on its own.

## Delivered
- The chain scenario specs, one per behaviour and seam.
- Executable assertion checks that read a run's outputs from disk and return a verdict, deterministic and needing no model call.
- The run records, the retrospectives, and the design map of what each scenario proves.
- A one-run invariant gate as the deploy default. Variance testing across repeated runs is kept separate, a predictability audit, not part of the gate.

## Constraints
- The chain is LLM-driven, so nothing is byte-repeatable. Checks assert invariants, structure, contracts, diff-confinement, not exact output.
- Deploy is a copy of a skill's directory, so the gate tests the skill as it lands, and only what sits in the skill directory ever ships.
- The gate runs once per redeploy by default. Multi-run variance stays outside it.
- If the gate is too slow or costly to run each time, it fails by not being run.
