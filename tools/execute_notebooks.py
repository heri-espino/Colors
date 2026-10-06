"""Execute every documentation notebook and write outputs in place."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def stable_cell_id(index: int, source: str) -> str:
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:10]
    return f"cell-{index:02d}-{digest}"


def execute_notebook(path: Path, *, cwd: Path, timeout: int) -> None:
    notebook = nbformat.read(path, as_version=4)

    for index, cell in enumerate(notebook.cells):
        if not cell.get("id"):
            cell["id"] = stable_cell_id(index, cell.get("source", ""))

    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        allow_errors=False,
        record_timing=False,
        resources={"metadata": {"path": str(cwd)}},
    )
    client.execute()
    nbformat.write(notebook, path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute all Sphinx example notebooks and save outputs."
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path("docs/source/notebooks"),
        help="Directory containing .ipynb files.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Per-cell execution timeout in seconds.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    directory = (root / args.directory).resolve()
    notebooks = sorted(directory.glob("*.ipynb"))

    if not notebooks:
        raise SystemExit(f"No notebooks found in {directory}")

    print(f"Executing {len(notebooks)} notebooks")
    for index, path in enumerate(notebooks, start=1):
        print(f"[{index:02d}/{len(notebooks):02d}] {path.relative_to(root)}")
        execute_notebook(path, cwd=root, timeout=args.timeout)

    print("All notebooks executed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
