<!-- Category: Parser -->
<!-- Title_DE: Natural Sorting -->
<!-- Title_EN: Natural Sorting -->
<!-- Summary_DE: Korrekte numerische Kapitelsortierung (1, 2, 10...) basierend auf Titeln & Timestamps. -->
<!-- Summary_EN: Correct numerical chapter sorting (1, 2, 10...) based on titles & timestamps. -->
<!-- Status: COMPLETED -->

# Natural Sorting

## Problem
Standard-Sortierung (lexikographisch) führt zu Reihenfolgen wie:
- Kapitel 1
- Kapitel 10
- Kapitel 11
- Kapitel 2

Das ist für Menschen kontraintuitiv, die eine numerische Reihenfolge erwarten.

## Lösung
Wir haben einen `natural_sort_key` in `parsers/format_utils.py` implementiert, der:
1. Strings in numerische und nicht-numerische Teile zerlegt.
2. Numerische Teile für den Vergleich in Integer umwandelt.
3. Gemischte Typen sicher verarbeitet.

## Integration
In `parsers/media_parser.py` wenden wir diese Sortierung auf alle extrahierten Kapitel an.
- **Primäre Sortierung**: Titel (Natural)
- **Sekundäre Sortierung**: Startzeit (Chronologisch)

Dies stellt sicher, dass Kapitel auch bei inkonsistenten Timestamps in der richtigen numerischen Reihenfolge (1, 2, 3... 10... 21, 22) erscheinen.

<!-- lang-split -->

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
