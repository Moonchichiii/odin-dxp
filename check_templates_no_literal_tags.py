from __future__ import annotations

import re
from pathlib import Path

TEMPLATE_DIRS = ["templates"]  # Directories to scan.
TEMPLATE_EXTS = {".html", ".djhtml", ".jinja", ".j2"}  # Template-like file extensions.


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]  # Repo root (one level above this file's folder).
    files: list[Path] = []

    for tdir in TEMPLATE_DIRS:
        base = repo_root / tdir
        if not base.exists():
            continue
        files.extend(p for p in base.rglob("*") if p.is_file() and p.suffix in TEMPLATE_EXTS)  # Collect templates.

    bad_context = re.compile(r">[^<]*{%\s*image\s+[^<]*<")  # `{% image ... %}` printed in text between tags.

    failures: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")  # Read file safely.
        for line_no, line in enumerate(text.splitlines(), start=1):
            if bad_context.search(line):
                failures.append(
                    f"{f}:{line_no} literal wagtail {{% image %}} found inside HTML text context"
                )  # Escape `{` in f-strings.

    if failures:
        print("\n".join(failures))
        print("\nFix: restore proper Django/Wagtail template syntax (no `{% image %}` printed as text).")
        return 1  # Fail the check.

    return 0  # Pass the check.


if __name__ == "__main__":
    raise SystemExit(main())
