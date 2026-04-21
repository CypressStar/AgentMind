from pathlib import Path


def make_empty_root(tmpdir: Path) -> Path:
    root = tmpdir / ".explib"
    root.mkdir(parents=True, exist_ok=True)
    return root
