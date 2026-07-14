# Onboarding revamp — proposal

<!-- EVAL FIXTURE for qualifying-outputs. Free-form proposal, no owning template or checklist,
and no originating decision record, on purpose, so the decision-fidelity anchor has no ground
truth to check against and must be declared unverifiable. Planted internal-consistency and
conventions drift is intentional. Do not "clean up" this file. -->

## Summary

We propose to revamp the new-hire onboarding flow so a new engineer ships a change on day one.

## Approach

The new flow has three stages: environment setup, a guided first task, and a review. Setup is fully
automated and takes under 10 minutes. The guided first task is picked by the mentor from a curated
backlog. The review happens on day two.

## Timeline

The whole flow completes within a single day, environment through review.

## Tooling

We will use the existing CLI. Setup is automated (e.g. the DB seed and the env file are generated).
This is a **robust** approach that harnesses the current toolchain to ensure a smooth first day.

## Open questions

- Who owns the curated backlog long-term?
