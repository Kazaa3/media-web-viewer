## UI Tab Switch Loop & WebSocket Keepalive Behaviour (2026-03-12)

### Observed Log Sequence
- Alternating tab switches between `player` and `playlist` (normal navigation).
- Repeated `player → player` switches, indicating redundant tab switch events.
- WebSocket keepalive warning: `keepalive recovered from base error: SystemExit:`.

### Analysis
- The UI triggers multiple redundant tab switches to the same tab (`player → player`), possibly due to a bug or unintended event loop.
- Backend WebSocket keepalive handler recovers from a `SystemExit` error, suggesting a session shutdown or restart.
- This behaviour may indicate instability in session management or frontend event handling.

### Recommendations
- Review frontend tab switch logic to prevent unnecessary switch events.
- Investigate backend session and WebSocket keepalive handling for unexpected exits.
