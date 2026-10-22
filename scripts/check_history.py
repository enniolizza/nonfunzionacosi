#!/usr/bin/env python3
"""Prevent reintroducing the removed PDF, including through an old branch merge."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REMOVED_PATH = 'Apri_Trading_in_the_Zone.pdf'
REMOVED_BLOB = 'f1297c62a800a2bb74b2c15130f1f3f0668a0d32'


def check_history(refs=('--all',)):
    shallow = subprocess.run(['git', 'rev-parse', '--is-shallow-repository'], cwd=ROOT,
                             text=True, capture_output=True, check=True)
    if shallow.stdout.strip() == 'true':
        raise ValueError('A complete clone is required to inspect history.')
    result = subprocess.run(['git', 'rev-list', '--objects', *refs], cwd=ROOT,
                            text=True, capture_output=True, check=True)
    for line in result.stdout.splitlines():
        oid, _, path = line.partition(' ')
        if oid == REMOVED_BLOB or Path(path).name == REMOVED_PATH:
            return False
    return True


if __name__ == '__main__':
    try:
        clean = check_history()
    except (subprocess.CalledProcessError, ValueError):
        print('ERROR: Git history unavailable; use a complete clone.', file=sys.stderr)
        sys.exit(1)
    if not clean:
        print('ERROR: removed PDF reachable in Git history. Do not merge an old clone or branch.', file=sys.stderr)
        sys.exit(1)
    print('OK: removed PDF absent from all locally available Git refs (path and blob).')
