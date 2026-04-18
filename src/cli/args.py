# src/cli/args.py

"""
Reusable CLI argument helpers for template repositories.

Each helper adds one argument to an existing argparse parser.
This keeps scripts modular, readable, and easy to mix and match.

Why not build one giant parser?
- Most scripts do not need every argument.
- Giant parsers become bloated, harder to read, and harder to maintain.
- Composing parsers from small helpers makes intent obvious in each script.

Why compose instead?
- Reuse: common arguments live in one place.
- Clarity: each script only includes what it actually needs.
- Consistency: same names, defaults, and help text across projects.
"""

from __future__ import annotations
import argparse


# .========================================================================
# BLOCK 1 — Constants
# .========================================================================

DEFAULT_OUTPUT_DIR = "outputs"
DEFAULT_ENCODING = "utf-8"

# .========================================================================
# BLOCK 2 — Shared internal helpers
# .========================================================================


def _add_path_argument(
    parser: argparse.ArgumentParser,
    *,
    flag: str,
    help_text: str,
    required: bool = False,
    default: str | None = None,
) -> None:
    parser.add_argument(
        flag,
        type=str,
        required=required,
        default=default,
        help=help_text,
    )


def _add_int_argument(
    parser: argparse.ArgumentParser,
    *,
    flag: str,
    help_text: str,
    default: int | None,
) -> None:
    parser.add_argument(
        flag,
        type=int,
        default=default,
        help=help_text,
    )


# .========================================================================
# BLOCK 3 — Public argument helpers
# .========================================================================


def add_input_arg(parser: argparse.ArgumentParser) -> None:

    # Use an optional flag instead of a positional argument so scripts stay clear as they grow
    _add_path_argument(
        parser,
        flag="--input",
        required=True,
        help_text=(
            "Path to the input file or folder "
            "(for example CSV, Excel, or a directory)"
        ),
    )


def add_output_arg(parser: argparse.ArgumentParser) -> None:

    _add_path_argument(
        parser,
        flag="--output",
        default=DEFAULT_OUTPUT_DIR,
        help_text='Path to the output file or folder Default: "outputs"',
    )


def add_sheet_arg(parser: argparse.ArgumentParser) -> None:

    parser.add_argument(
        "--sheet",
        type=str,
        default=None,
        help="Excel sheet name to read If omitted, default sheet handling is used",
    )


def add_drop_empty_arg(parser: argparse.ArgumentParser) -> None:

    parser.add_argument(
        "--drop-empty",
        action="store_true",
        help="Drop fully empty rows before processing",
    )


def add_encoding_arg(parser: argparse.ArgumentParser) -> None:

    parser.add_argument(
        "--encoding",
        type=str,
        default=DEFAULT_ENCODING,
        help='Text encoding to use when reading files Default: "utf-8"',
    )


def add_rows_arg(
    parser: argparse.ArgumentParser,
    default: int | None = None,
) -> None:

    if default is None:
        help_text = "Number of rows to process or preview Default: all rows"
    else:
        help_text = f"Number of rows to process or preview Default: {default}"

    _add_int_argument(
        parser,
        flag="--rows",
        default=default,
        help_text=help_text,
    )


def add_max_cols_arg(
    parser: argparse.ArgumentParser,
    default: int | None = None,
) -> None:

    if default is None:
        help_text = "Maximum number of columns to process or preview Default: no limit"
    else:
        help_text = (
            f"Maximum number of columns to process or preview Default: {default}"
        )

    _add_int_argument(
        parser,
        flag="--max-cols",
        default=default,
        help_text=help_text,
    )


# END OF FILE
