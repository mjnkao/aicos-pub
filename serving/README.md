# AICOS Serving

Status: generated review/context surfaces

`serving/` holds generated or derived packets that help humans and agents
inspect AICOS state without making backend state authoritative.

Examples include:

- generated capsules;
- branch and option packets;
- promotion review packets;
- query helpers;
- truth and feedback review surfaces.

Generated serving material must not silently override `brain/` or
`agent-repo/`. If a generated view reveals a meaningful change, normalize it
back into the appropriate authority lane through review/writeback.
