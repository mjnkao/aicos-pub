# GBrain Adapter

Status: initial MVP scaffold

The adapter reuses the existing local GBrain wrapper:

```text
scripts/gbrain_local.sh
```

The MVP keeps PGLite as the local-first engine through the existing GBrain tool
under `tools/gbrain`. AICOS does not reimplement the brain engine.

