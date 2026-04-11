/**
 * collections.js
 * Forensic Collection & Folder Orchestration (v1.45.130)
 * Handles advanced grouping, folder name parsing, and metadata association.
 */

window.CollectionManager = (function() {
    
    /**
     * Parses a folder name to extract Title and Year.
     * Supports: "Movie Name (2024)", "Artist - Album (2023)", "Series S01"
     */
    function parseFolderName(name) {
        if (!name) return { title: 'Unknown', year: '', category_prefix: '' };
        
        // Remove [FOLDER] prefix if present
        let cleanName = name.replace(/^\[FOLDER\]\s+/, '');
        
        const result = {
            title: cleanName,
            year: '',
            artist: '',
            category_prefix: ''
        };

        // 0. Detect Specialized Category Prefixes (v1.45.130-EXT)
        const prefixMatch = cleanName.match(/^\[(MIX|PODCAST|AUDIOBOOK)\]\s*/i);
        if (prefixMatch) {
            result.category_prefix = prefixMatch[1].toUpperCase();
            cleanName = cleanName.replace(/^\[.*?\]\s*/i, '');
            result.title = cleanName;
        }
        
        // 1. Regex for (Year) pattern: "Title (2024)"
        const yearMatch = cleanName.match(/\((\d{4})\)$/);
        if (yearMatch) {
            result.year = yearMatch[1];
            result.title = cleanName.replace(/\s*\(\d{4}\)$/, '').trim();
        }
        
        // 2. Regex for Artist - Title pattern: "Artist - Album"
        if (result.title.includes(' - ')) {
            const parts = result.title.split(' - ');
            result.artist = parts[0].trim();
            result.title = parts.slice(1).join(' - ').trim();
        }
        
        return result;
    }

    /**
     * Groups individual library items by their parent folder.
     * Used for "Collection View" to consolidate multi-part media.
     */
    function groupItemsByFolder(items) {
        if (!items || items.length === 0) return [];
        
        const folders = {};
        const standalone = [];
        
        items.forEach(item => {
            const pathParts = (item.path || '').split('/');
            if (pathParts.length > 1) {
                const parentDir = pathParts.slice(0, -1).join('/');
                if (!folders[parentDir]) {
                    folders[parentDir] = {
                        id: `coll-${parentDir}`,
                        name: pathParts[pathParts.length - 2],
                        path: parentDir,
                        items: [],
                        category: item.category, // Initial guess
                        type: 'collection'
                    };
                }
                folders[parentDir].items.push(item);
            } else {
                standalone.push(item);
            }
        });
        
        // Consolidate folders into Collection items
        const collections = Object.values(folders).map(folder => {
            if (folder.items.length === 1) return folder.items[0]; // Not really a collection
            
            // Logic for a real collection
            const meta = parseFolderName(folder.name);
            return {
                ...folder,
                displayTitle: meta.title,
                year: meta.year,
                artist: meta.artist,
                count: folder.items.length,
                is_collection: true
            };
        });
        
        return [...standalone, ...collections].sort((a, b) => (a.name || '').localeCompare(b.name || ''));
    }

    return {
        parseFolderName,
        groupItemsByFolder
    };

})();

// Created with MWV v1.45.130-EVO-REBUILD
