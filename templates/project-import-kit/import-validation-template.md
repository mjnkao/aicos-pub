# Import Validation Template

Status: shared reusable template

Purpose: decide whether an import is usable enough for real A1 work.

## A. Startup Sufficiency

- [ ] A1 can understand what the project is
- [ ] A1 can identify the first slice
- [ ] A1 can find the right packet without broad-loading
- [ ] independent executor can find the import-kit hub first

## B. Startup Efficiency

- [ ] startup remains light
- [ ] archive/history stays outside hot path
- [ ] packet-first behavior is preserved

## C. Rule Compatibility

- [ ] A1 knows which rule layers apply
- [ ] project / work_context / task are separate
- [ ] artifact-neutral language still fits the project

## D. Continuity Quality

- [ ] second A1 can continue cheaply
- [ ] `handoff/current.md` is sufficient
- [ ] task continuity metadata is sufficient

## E. Authority Integrity

- [ ] external repo remains code/runtime authority
- [ ] isolated checkout is the external work authority for the test
- [ ] AICOS remains context/control-plane authority
- [ ] imported truth is not confused with raw reference docs

## F. Full Active Context Discipline

- [ ] active context is complete enough for real work
- [ ] archive/history remains excluded unless justified
- [ ] generated output bulk remains excluded unless justified
- [ ] import did not pull too much into AICOS
- [ ] import did not mirror external structure too literally
- [ ] import did not pull broad internals too early

## G. Independent Execution Validation

- [ ] A2-Core Codex 2 can execute without old-thread memory
- [ ] current working folder was not mutated
- [ ] no MCP runtime was required for the import pass
- [ ] follow-up A1 test boundary is clear

## Rule

Do not mark the import complete until validation is recorded.
