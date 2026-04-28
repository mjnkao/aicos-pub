# Sample Research Digest Project Brief

Status: public sample

## Purpose

Sample Research Digest collects public notes, normalizes them into stable
records, validates source coverage, and packages a daily brief for an assistant
or human reviewer.

## Product Posture

- Output-first: define the digest consumers need before expanding inputs.
- Source-attributed: every useful claim should trace back to source material.
- Missingness-aware: the digest must say when coverage is incomplete.
- Reviewable: a human should be able to inspect the compact package.

## Non-Goals

- No private data ingestion.
- No raw mirror of all notes.
- No hidden scoring engine.
- No autonomous publishing without review.

## Success

A new agent can read AICOS context, inspect one selected task packet, open only
the relevant source artifacts, and improve the digest flow without bulk-loading
the whole project.
