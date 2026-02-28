#!/usr/bin/env python3
"""
Scan a root directory (recursively). For each directory that contains .pt files,
keep only the latest one and optionally delete the rest.

Selection rule:
- If filenames contain numeric tokens, the largest numeric token (last found) is
  used to determine the "latest" (e.g. model_20000.pt > model_10000.pt).
- Otherwise fallback to file modification time.

Usage:
  python3 keep_latest_pt.py /path/to/root        # dry-run, don't delete
  python3 keep_latest_pt.py /path/to/root --yes  # actually remove older .pt files
"""
import argparse
import os
import re
from pathlib import Path
from typing import List, Optional


NUM_RE = re.compile(r"(\d+)")


def list_pt_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        pts = [Path(dirpath) / f for f in filenames if f.endswith('.pt')]
        if pts:
            yield Path(dirpath), pts


def extract_trailing_number(p: Path) -> Optional[int]:
    # find all numbers in filename and use the last one as the representative
    ms = NUM_RE.findall(p.name)
    if not ms:
        return None
    return int(ms[-1])


def choose_latest(paths: List[Path]) -> Path:
    # prefer numeric suffix if present
    nums = {p: extract_trailing_number(p) for p in paths}
    numeric = {p: n for p, n in nums.items() if n is not None}
    if numeric:
        # choose the path with the largest numeric token
        latest = max(numeric.items(), key=lambda kv: kv[1])[0]
        return latest
    # fallback: choose by modification time
    latest = max(paths, key=lambda p: p.stat().st_mtime)
    return latest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=str, help='root folder to scan')
    parser.add_argument('--yes', action='store_true', help='actually delete older files')
    parser.add_argument('--pattern', type=str, default='*.pt', help='file pattern to consider')
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f'root {root} does not exist')
        return

    total_deleted = 0
    total_kept = 0
    to_delete = []

    for d, pts in list_pt_files(root):
        if len(pts) <= 1:
            total_kept += len(pts)
            continue
        latest = choose_latest(pts)
        kept_name = latest.name
        total_kept += 1
        for p in pts:
            if p == latest:
                continue
            to_delete.append((d, p, kept_name))

    if not to_delete:
        print('No redundant .pt files found; nothing to do.')
        return

    print('Planned deletions (older .pt files). The latest file in each directory will be kept:')
    for d, p, kept in to_delete:
        print(f'  DIR: {d}  ->  DELETE: {p.name}    (keep {kept})')

    if args.yes:
        for d, p, kept in to_delete:
            try:
                p.unlink()
                total_deleted += 1
            except Exception as e:
                print(f'Failed to delete {p}: {e}')
        print(f'Deleted {total_deleted} files. Kept {total_kept} files.')
    else:
        print('\nDry-run mode: no files were deleted. Rerun with --yes to actually remove them.')
        print(f'Would delete {len(to_delete)} files and keep {total_kept} files.')


if __name__ == '__main__':
    main()
