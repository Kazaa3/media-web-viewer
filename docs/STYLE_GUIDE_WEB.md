# Style Guide - Web Frontend

## I18n Usage
- Use `data-i18n="tag_name"` for static text in HTML.
- Use `t('tag_name')` for dynamic text in JavaScript.
- All new tags MUST be added to both `de` and `en` sections in `web/i18n.json`.

## UI Feedback
- Use `appendUiTrace(message)` to log events that appear in the Debug tab.
- Button IDs should follow kebab-case: `my-button-id`.
- Tab content IDs MUST follow `tab_name-tab` pattern.

## Persistence
- Use `saveParserChainUI()` to trigger a backend save of the parser configuration.
- Local temporary UI state can be stored in `localStorage` with `mwv_` prefix.
