# AICOS Backend

Status: serving/index substrate, not authority

`backend/` may hold engine config, indexes, sync state, embeddings, health
checks, migrations, and other runtime support.

It is not a truth layer. Current project truth remains in `brain/`, and actor
operations remain in `agent-repo/`.

The MVP uses GBrain/PGLite as local serving substrate. Retrieval freshness is a
known architectural risk until sync/embedding status is explicit and observable.
