import argparse
from typing import Optional, Sequence


def parse_bool(raw_value: str) -> bool:
    normalized = raw_value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("Expected boolean value: true/false, yes/no, 1/0")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate annual tax based on profile"
    )
    parser.add_argument("--income", type=float, required=True, help="Annual income")
    parser.add_argument(
        "--category",
        type=str,
        required=True,
        choices=[
            "salary",
            "business",
            "investment",
            "freelance",
            "crypto",
            "real_estate",
        ],
        help="Income category",
    )
    parser.add_argument("--age", type=int, required=True, help="Person age")
    parser.add_argument(
        "--resident", type=parse_bool, required=True, help="Resident status"
    )
    parser.add_argument(
        "--dependents",
        type=parse_bool,
        default=False,
        help="Whether person has dependents",
    )
    parser.add_argument(
        "--married",
        type=parse_bool,
        default=False,
        help="Whether person is married",
    )
    return parser


def parse_cli_arguments(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    return build_parser().parse_args(args)
