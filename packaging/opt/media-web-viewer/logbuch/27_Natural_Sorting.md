<!-- Category: Parser -->

# Natural Sorting

## Problem
Standard sorting (lexicographical) leads to orders like:
- Kapitel 1
- Kapitel 10
- Kapitel 11
- Kapitel 2

This is counter-intuitive for humans who expect numerical order.

## Solution
We implemented a `natural_sort_key` in `parsers/format_utils.py` that:
1. Splits strings into numeric and non-numeric parts.
2. Converts numeric parts into integers for proper comparison.
3. Handles mixed types safely.

## Integration
In `parsers/media_parser.py`, we apply this sorting to all extracted chapters.
- **Primary Sort**: Title (Natural)
- **Secondary Sort**: Start Time (Chronological)

This ensures that even if file metadata has inconsistent timestamps, the chapters appear in the correct numerical order (1, 2, 3... 10... 21, 22).
