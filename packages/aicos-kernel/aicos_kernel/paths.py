from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
BRAIN_ROOT_ENV = "AICOS_BRAIN_ROOT"


def brain_root() -> Path:
    """Return the active AICOS brain root.

    Defaults to <repo>/brain. AICOS_BRAIN_ROOT is an experimental deployment
    boundary for mounted/private brain packs; callers should still render
    source refs as virtual brain/... paths.
    """
    configured = os.environ.get(BRAIN_ROOT_ENV, "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    return REPO_ROOT / "brain"


def brain_path(*parts: str) -> Path:
    return brain_root().joinpath(*parts)


def repo_rel(path: Path) -> str:
    resolved = path.resolve() if path.exists() else path
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def virtual_repo_path(path: Path) -> Path:
    """Map files under AICOS_BRAIN_ROOT back to virtual brain/... refs."""
    resolved = path.resolve() if path.exists() else path
    root = brain_root().resolve()
    try:
        return Path("brain") / resolved.relative_to(root)
    except ValueError:
        try:
            return resolved.relative_to(REPO_ROOT)
        except ValueError:
            return path


def virtual_repo_ref(path: Path) -> str:
    return str(virtual_repo_path(path))
