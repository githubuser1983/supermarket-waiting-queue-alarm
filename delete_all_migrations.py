#!/usr/bin/env python3
# coding: utf-8


""" deletes all migration files """


from pathlib import Path

cwd = Path(".")
apps = cwd / "apps"
sub_dirs = [
    sub_dir
    for sub_dir in apps.iterdir()
    if sub_dir.is_dir() and sub_dir.name != "__pycache__"
]

for d in sub_dirs:
    migrations = Path(d) / "migrations"
    if migrations.exists():
        for f in [m for m in migrations.iterdir() if not m.is_dir()]:
            if f.name != "__init__.py":
                print(f"deleting {f.parent}/{f.name}")
                f.unlink()
