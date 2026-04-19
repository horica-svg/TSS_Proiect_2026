#!/usr/bin/env python3
"""Recompute and update expected values in structural coverage tests.

Supported schema in @pytest.mark.parametrize:
    income, category, age, is_resident, has_dependents, is_married, expected
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from App.Tax_Calculator import TaxEngine

STRUCTURAL_DIR = ROOT / "tests" / "structural_coverage"
TARGET_TO_FILE = {
    "statement": STRUCTURAL_DIR / "test_statement_coverage.py",
    "branch": STRUCTURAL_DIR / "test_branch_coverage.py",
    "condition": STRUCTURAL_DIR / "test_condition_coverage.py",
    "paths": STRUCTURAL_DIR / "test_independent_paths_coverage.py",
}
REQUIRED_FIELDS = {
    "income",
    "category",
    "age",
    "is_resident",
    "has_dependents",
    "is_married",
    "expected",
}


@dataclass
class Replacement:
    start: int
    end: int
    new_text: str


@dataclass
class FileStats:
    file_path: Path
    cases: int = 0
    updated: int = 0
    unchanged: int = 0
    drift_found: int = 0


def _line_offsets(text: str) -> List[int]:
    offsets = [0]
    total = 0
    for line in text.splitlines(keepends=True):
        total += len(line)
        offsets.append(total)
    return offsets


def _abs_offset(line_offsets: Sequence[int], lineno: int, col: int) -> int:
    return line_offsets[lineno - 1] + col


def _literal(node: ast.AST, source: str):
    segment = ast.get_source_segment(source, node)
    if segment is None:
        raise ValueError("Could not read literal source segment")
    return ast.literal_eval(segment)


def _is_parametrize_call(node: ast.Call) -> bool:
    func = node.func
    if not isinstance(func, ast.Attribute) or func.attr != "parametrize":
        return False
    mark = func.value
    if not isinstance(mark, ast.Attribute) or mark.attr != "mark":
        return False
    root = mark.value
    return isinstance(root, ast.Name) and root.id == "pytest"


def _parse_fields(node: ast.Call) -> List[str]:
    if not node.args:
        raise ValueError("parametrize missing field list")
    fields_expr = node.args[0]
    if not isinstance(fields_expr, ast.Constant) or not isinstance(
        fields_expr.value, str
    ):
        raise ValueError("parametrize field list must be a string literal")
    fields = [part.strip() for part in fields_expr.value.split(",") if part.strip()]
    if set(fields) != REQUIRED_FIELDS:
        raise ValueError(
            f"Unexpected fields {fields}. Expected exactly {sorted(REQUIRED_FIELDS)}"
        )
    return fields


def _find_case_list(node: ast.Call) -> ast.AST:
    if len(node.args) < 2:
        raise ValueError("parametrize missing case list")
    container = node.args[1]
    if not isinstance(container, (ast.List, ast.Tuple)):
        raise ValueError("parametrize case collection must be list/tuple")
    return container


def process_file(
    file_path: Path, engine: TaxEngine, dry_run: bool, check_only: bool
) -> Tuple[FileStats, bool]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    offsets = _line_offsets(source)
    replacements: List[Replacement] = []
    stats = FileStats(file_path=file_path)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not _is_parametrize_call(node):
            continue

        fields = _parse_fields(node)
        case_list = _find_case_list(node)

        for case in case_list.elts:
            if not isinstance(case, ast.Tuple):
                raise ValueError(f"Only tuple cases supported in {file_path}")
            if len(case.elts) != len(fields):
                raise ValueError(
                    f"Tuple length {len(case.elts)} does not match fields {len(fields)} in {file_path}"
                )

            row = {
                name: _literal(elem, source) for name, elem in zip(fields, case.elts)
            }
            stats.cases += 1

            computed = engine.calculate_annual_tax(
                income=row["income"],
                category=row["category"],
                age=row["age"],
                is_resident=row["is_resident"],
                has_dependents=row["has_dependents"],
                is_married=row["is_married"],
            )
            current = row["expected"]
            if computed == current:
                stats.unchanged += 1
                continue

            stats.updated += 1
            stats.drift_found += 1
            expected_idx = fields.index("expected")
            expected_node = case.elts[expected_idx]
            start = _abs_offset(offsets, expected_node.lineno, expected_node.col_offset)
            end = _abs_offset(
                offsets, expected_node.end_lineno, expected_node.end_col_offset
            )
            replacements.append(
                Replacement(start=start, end=end, new_text=repr(computed))
            )

    changed = bool(replacements)
    if changed and not (dry_run or check_only):
        updated_text = source
        for rep in sorted(replacements, key=lambda r: r.start, reverse=True):
            updated_text = (
                updated_text[: rep.start] + rep.new_text + updated_text[rep.end :]
            )
        file_path.write_text(updated_text, encoding="utf-8")

    return stats, changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update expected values in structural tests"
    )
    parser.add_argument(
        "--target",
        default="all",
        choices=["all", "statement", "branch", "condition", "paths"],
        help="Choose which structural test file(s) to process",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show drift without writing changes"
    )
    parser.add_argument(
        "--check", action="store_true", help="Exit non-zero if drift exists"
    )
    args = parser.parse_args()

    targets = list(TARGET_TO_FILE.keys()) if args.target == "all" else [args.target]
    files = [TARGET_TO_FILE[t] for t in targets]

    engine = TaxEngine()
    total_cases = 0
    total_updated = 0
    total_unchanged = 0
    files_with_drift = 0

    for file_path in files:
        stats, changed = process_file(file_path, engine, args.dry_run, args.check)
        total_cases += stats.cases
        total_updated += stats.updated
        total_unchanged += stats.unchanged
        if changed:
            files_with_drift += 1

        status = "DRIFT" if changed else "OK"
        print(
            f"[{status}] {file_path.relative_to(ROOT)}: "
            f"cases={stats.cases} unchanged={stats.unchanged} updated={stats.updated}"
        )

    print(
        f"Summary: files={len(files)} drift_files={files_with_drift} "
        f"cases={total_cases} unchanged={total_unchanged} updated={total_updated}"
    )

    if args.check and total_updated > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
