# Hinweis: Tab-IDs und tabMap – Video/VLC

**Datum:** 15.03.2026

## Aktueller Stand
- Die tabMap im Frontend enthält sowohl `'vlc': 'vlc'` als auch `'video': 'video-tab'`.
- Dies kann zu Inkonsistenzen führen, wenn die Tab-IDs und die zugehörigen Container nicht eindeutig und konsistent verwendet werden.

## Empfehlung
- Einheitliche Benennung: Für den Video-Tab sollte nur eine ID verwendet werden (z. B. `'video': 'video-tab'` oder `'vlc': 'vlc'`), nicht beide parallel.
- Die Tab-Map und die HTML-IDs müssen exakt übereinstimmen, damit die Navigation und das Anzeigen/Verstecken der Tabs zuverlässig funktioniert.
- Nach Umstrukturierungen (z. B. Umbenennung von VLC zu Video) die tabMap und alle zugehörigen IDs/Referenzen im Code anpassen.

## ToDo
- Überprüfen, ob im HTML und in der tabMap noch alte IDs (z. B. 'vlc') verwendet werden.
- Konsolidieren auf eine eindeutige Tab-ID für den Video-Tab.

## Ergebnis
- Vermeidung von UI-Bugs und Navigationsproblemen durch konsistente Tab-IDs.


        const tabMap = {
            'player': 'media-list',
            'library': 'library-tab',
            'browser': 'browser-tab',
            'edit': 'edit-tab',
            'options': 'options-tab',
            'parser': 'parser-tab',
            'debug': 'debug-tab',
            'tests': 'tests',
            'logbuch': 'logbuch-tab',
            'playlist': 'playlist-tab',
            'vlc': 'vlc',
            'video': 'video-tab'
        };