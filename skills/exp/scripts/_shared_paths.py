from pathlib import Path


def get_root(root_arg: str | None) -> Path:
    return Path(root_arg or ".explib")
