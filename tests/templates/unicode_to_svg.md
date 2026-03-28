# Unicode-to-SVG Migration Template

## Problem Statement
The project requires 100% SVG-based iconography for the UI layer to ensure rendering consistency, performance, and modern aesthetics (glassmorphism). Unicode symbols are permitted **ONLY** in `console.log`, `console.info`, and standard text logging where SVG rendering is not supported by the environment.

## Migration Workflow

### 1. Identify Target Symbols
Find all raw Unicode symbols (emojis, technical symbols) in `.html` and `.js` files.
*   **Audit Tool**: `python3 tests/run_all.py --basis` (Optimization Suite L1)

### 2. Update Centralized Library
Ensure the symbol exists in the `<svg>` block at the top of `web/app.html`.
```html
<symbol id="icon-new" viewBox="...">
  <!-- Path data -->
</symbol>
```

### 3. Replace in HTML/JS
Replace the Unicode character with the appropriate SVG calling convention.

#### HTML Template:
```html
<svg width="12" height="12"><use href="#icon-new"></use></svg>
```

#### CSS / JS Template (Dynamic Injection):
```javascript
const svgHtml = `<svg width="12" height="12"><use href="#icon-new"></use></svg>`;
element.innerHTML = `${svgHtml} Label Text`;
```

### 4. Verify Exception Policy
Ensure Unicode remains in logging functions ONLY:
```javascript
// ✅ ALLOWED
console.info("🚀 System initialized"); 

// ❌ FORBIDDEN
button.innerHTML = "🚀 Start"; 
// ✅ CORRECTED
button.innerHTML = `${svgSparkles} Start`;
```

## Maintenance
The `OptimizationSuiteEngine` (Level 1) will automatically flag any UI-layer Unicode violations during the master diagnostic run.
