from pathlib import Path
import subprocess


def get_project_root(project_root_arg: str | None) -> Path:
    if project_root_arg:
        return Path(project_root_arg)

    cwd = Path.cwd()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return cwd


def get_explib_root(project_root: Path) -> Path:
    return project_root / ".explib"


def to_project_relative(path: Path, project_root: Path) -> str:
    return path.relative_to(project_root).as_posix()


def get_domain_dir(project_root: Path, domain: str) -> Path:
    return get_explib_root(project_root) / "domains" / domain


def get_domain_index_path(project_root: Path, domain: str) -> Path:
    return get_domain_dir(project_root, domain) / "toc.index.json"


def get_domain_toc_path(project_root: Path, domain: str) -> Path:
    return get_domain_dir(project_root, domain) / "TOC.md"


def get_entry_path(project_root: Path, kind: str, domain: str, entry_id: str) -> Path:
    base = "resolved" if kind == "resolved" else "dead-ends"
    return get_explib_root(project_root) / base / domain / f"{entry_id}.json"


def get_pending_events_dir(project_root: Path) -> Path:
    return get_explib_root(project_root) / "pending" / "events"


def get_pending_event_dir(project_root: Path, event_id: str) -> Path:
    return get_pending_events_dir(project_root) / event_id
