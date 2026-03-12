# Compatibility and Version Mapping

## Current pairing
| Klipper Component | DWIN Component | Status |
|-------------------|----------------|--------|
| 1.4.4             | 0.5.2          | Current |
| 1.4.3             | 0.5.2          | Supported |
| 1.4.2             | 0.5.1          | Deprecated |

## Rules
- A MAJOR increment in either component requires a new row in this table.
- A MINOR increment in either component requires a compatibility note.
- A PATCH increment in either component does not change pairings.
- Release notes must always state the required paired version.

## Compatibility rule
- Klipper MAJOR change → DWIN MAJOR must also increment (forced pairing break).
- Klipper MINOR change → existing DWIN version may still be compatible (verify and document).
- DWIN MINOR change → existing Klipper version may still be compatible (verify and document).