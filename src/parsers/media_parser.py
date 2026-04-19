import time
import copy
import subprocess
from typing import Any
from pathlib import Path
import multiprocessing
import importlib
from src.core.config_master import GLOBAL_CONFIG
from src.core.logger import get_logger

log = get_logger("media_parser")

# Parser Categories (Centralized v1.41.00)
AUDIO_PARSER_IDS = set(GLOBAL_CONFIG["parser_registry"]["categories"]["audio"])
VIDEO_PARSER_IDS = set(GLOBAL_CONFIG["parser_registry"]["categories"]["video"])
UNIVERSAL_PARSER_IDS = set(GLOBAL_CONFIG["parser_registry"]["categories"]["universal"])

def sanitize_metadata(tags: dict[str, Any]) -> dict[str, Any]:
    """
    @brief Sanitizes metadata to prevent memory bloat or UI lag (v1.46.102).
    """
    limits = GLOBAL_CONFIG.get("parser_limits", {})
    max_len = limits.get("max_tag_length", 1024)
    max_chaps = limits.get("max_chapters", 500)
    
    # Use centralized feature flag (v1.46.132)
    feat_cfg = GLOBAL_CONFIG.get("parser_registry", {}).get("feature_flags", {})
    enable_log = feat_cfg.get("log_truncation_warnings", True)

    for key, value in tags.items():
        if isinstance(value, str) and len(value) > max_len:
            if enable_log:
                log.warning(f"[Parser-Sanitize] Truncating long tag '{key}' ({len(value)} chars)")
            tags[key] = value[:max_len] + "..."
    
    if "chapters" in tags and isinstance(tags["chapters"], list):
        if len(tags["chapters"]) > max_chaps:
            if enable_log:
                log.warning(f"[Parser-Sanitize] Truncating excessive chapters ({len(tags['chapters'])} -> {max_chaps})")
            tags["chapters"] = tags["chapters"][:max_chaps]
            
    return tags

# Magic byte signatures (Centralized v1.41.00)
_sig_map = GLOBAL_CONFIG["parser_registry"]["magic_signatures"]
REQUIRED_MAGIC = {k: bytes.fromhex(v) for k, v in _sig_map.items()}

def get_file_magic(path: Path, length: int = 16, offset: int = 0) -> bytes:
    """
    @brief Reads bytes from a file at a specific offset.
    """
    try:
        with path.open("rb") as f:
            if offset > 0:
                f.seek(offset)
            return f.read(length)
    except Exception as e:
        log.debug(f"[Parser-Magic] Failed to read magic for {path.name}: {e}")
        return b""

def validate_semantic_consistency(tags: dict[str, Any], filename: str):
    """
    @brief Compares metadata from different sources for sanity.
    """
    # 1. Duration Cross-Check
    durations = []
    for k in tags:
        if 'duration' in k.lower() and tags[k]:
            try:
                durations.append(float(tags[k]))
            except (ValueError, TypeError):
                continue
    
    if len(set(durations)) > 1:
        avg_dur = sum(durations) / len(durations)
        discrepancy = max(durations) - min(durations)
        if discrepancy > 5: # More than 5 seconds difference
            log.warning(f"⚖️ [Semantic-Validation] Duration discrepancy for '{filename}': {min(durations)}s to {max(durations)}s")

def _sandboxed_worker(func, queue, *args, **kwargs):
    """
    Internal worker for multiprocessing.
    """
    try:
        result = func(*args, **kwargs)
        queue.put((True, result))
    except Exception as e:
        queue.put((False, str(e)))

def run_sandboxed(func, timeout, *args, **kwargs):
    """
    @brief Runs a function in a separate process to isolate crashes/hangs.
    """
    result_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_sandboxed_worker, args=(func, result_queue) + args, kwargs=kwargs)
    p.start()
    
    try:
        success, result = result_queue.get(timeout=timeout)
        p.join(timeout=1.0)
        if success:
            return result
        else:
            raise Exception(f"Sandboxed process error: {result}")
    except (multiprocessing.TimeoutError, queue.Empty):
        p.terminate()
        p.join()
        raise TimeoutError(f"Sandboxed process timed out after {timeout}s")
    except Exception as e:
        p.terminate()
        p.join()
        raise e


# Mapping which parsers are responsible for which file types (Centralized v1.41.00)
PARSER_MAPPING = GLOBAL_CONFIG["parser_registry"]["extension_map"]


def get_parser_info() -> dict[str, Any]:
    """
    @brief Aggregates info about all available parsers, their capabilities and settings schemas.
    """
    registry = GLOBAL_CONFIG.get("parser_registry", {})
    module_reg = registry.get("module_registry", {})
    
    parsers = {}
    for p_id, mod_path in module_reg.items():
        try:
            # Dynamic Import (Phase 12 Centralization)
            mod = importlib.import_module(mod_path)
            parsers[p_id] = mod
        except Exception as e:
            log.warning(f"[Parser-Registry] Failed to import {p_id} ({mod_path}): {e}")
    
    info = {}
    for p_id, p_mod in parsers.items():
        p_info = {}
        if hasattr(p_mod, 'get_capabilities'):
            p_info['capabilities'] = p_mod.get_capabilities()
        if hasattr(p_mod, 'get_settings_schema'):
            p_info['settings_schema'] = p_mod.get_settings_schema()
        
        if p_info:
            info[p_id] = p_info
            
    return info


def extract_metadata(path, filename, mode=None, file_type=None, **kwargs):
    """
    @brief Orchestrates the metadata extraction process using a sequential parser chain (Centralized v1.46.131).
    """
    if mode is None:
        mode = GLOBAL_CONFIG.get("parser_modes", {}).get("default", "lightweight")
        
    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from src.core.config_master import ALL_AUDIO_EXTENSIONS
    
    if file_type in ALL_AUDIO_EXTENSIONS:
        return extract_metadata_audio(path, filename, mode, **kwargs)
    else:
        return extract_metadata_multimedia(path, filename, mode, **kwargs)

def extract_metadata_audio(path, filename, mode='lightweight', **kwargs):
    """
    @brief Specialized branch for audio-only extraction.
    """
    log.debug(f"🎵 [Audio-Branch] Starting extraction for '{filename}'")
    return _extract_metadata_internal(path, filename, mode, category='audio', **kwargs)

def extract_metadata_multimedia(path, filename, mode='lightweight', **kwargs):
    """
    @brief Specialized branch for multimedia (video/ISO) extraction.
    """
    log.debug(f"🎬 [Multimedia-Branch] Starting extraction for '{filename}'")
    return _extract_metadata_internal(path, filename, mode, category='multimedia', **kwargs)

def _extract_metadata_internal(path, filename, mode='lightweight', category=None, **kwargs):
    """
    @brief Core extraction logic shared by branches.
    """
    log.info(f"[Parser-Trace] Starte Parsing für '{filename}' (Mode: {mode}, Category: {category})")
    if mode in ('full', 'ultimate'):
        log.info(f"[Parser-Trace] 🚀 {mode.capitalize()} Mode aktiviert für '{filename}' – sammle ALLE Tags!")

    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from src.parsers.format_utils import PARSER_CONFIG, format_bitdepth, format_codec, format_container, format_tagtype

    # 2. Initialize Tags from Centralized Registry (Phase 9)
    registry = GLOBAL_CONFIG.get("parser_registry", {})
    default_tags = registry.get("default_tags", {})
    
    tags: dict[str, Any] = copy.deepcopy(default_tags)
    tags.update({
        'name': filename,
        'type': 'directory' if path_obj.is_dir() else 'file' if path_obj.is_file() else 'missing'
    })

    # Initialize full_tags for high-fidelity modes (Centralized v1.46.131)
    parser_cfg = GLOBAL_CONFIG.get("parser_modes", {})
    if (mode in ('full', 'ultimate') or parser_cfg.get("enable_full_tags", False)) and 'full_tags' not in tags:
        tags['full_tags'] = {}

    duration = 0
    parser_times = {}

    registry = GLOBAL_CONFIG.get("parser_registry", {})
    module_reg = registry.get("module_registry", {})

    def vlc_dispatch(profile):
        def _vlc_wrapper(path, file_type, tags, filename=None, mode='lightweight', settings=None):
            if settings is None: settings = {}
            settings['profile'] = profile
            # Resolve vlc_parser dynamically
            try:
                vlc_mod = importlib.import_module(module_reg.get('parser_vlc_bridge', 'src.parsers.vlc_parser'))
                return vlc_mod.parse(path, file_type, tags, filename, mode, settings)
            except Exception as e:
                log.error(f"[VLC-Dispatch] Failed: {e}")
                return tags
        return _vlc_wrapper

    # 3. Mode-based Chain Selection (Phase 10 Ultimate Expansion)
    is_audio = category == 'audio'
    if mode == 'ultimate':
        parser_chain = registry.get("ultimate_chain", [])
        log.info(f"🚀 [Ultimate-Mode] Overriding chain: {parser_chain}")
    else:
        parser_chain = cast(list[str], PARSER_CONFIG.get(
            "parser_chain", registry.get("default_chain", ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "isoparser"])))

    # 4. Resolve Active Steps Dynamically (Centralized v1.46.132)
    active_steps = []
    for p_id in parser_chain:
        if p_id.startswith('vlc_'):
            # Virtual VLC profile steps
            profile = p_id.replace('vlc_', '')
            if profile == 'exhaustive': profile = 'exhaustive' 
            active_steps.append((p_id, vlc_dispatch(profile)))
            continue

        mod_path = module_reg.get(p_id)
        if mod_path:
            try:
                mod = importlib.import_module(mod_path)
                if hasattr(mod, 'parse'):
                    active_steps.append((p_id, mod.parse))
                else:
                    log.warning(f"[Parser-Chain] Module {p_id} missing parse() function")
            except Exception as e:
                log.error(f"[Parser-Chain] Failed to load {p_id} from {mod_path}: {e}")
        else:
            log.warning(f"[Parser-Chain] No module registered for ID: {p_id}")

    from src.core.models import SLOW_PARSERS
    error_shortcircuit = False
    
    # Calibration Settings (Phase 11)
    cal_cfg = registry.get("calibration_registry", {})
    
    for step_name, step_func in active_steps:
        # Ultimate Mode bypasses branch isolation (Phase 10)
        if mode != 'ultimate':
            if is_audio and step_name in VIDEO_PARSER_IDS:
                log.debug(f"🔇 [Audio-Branch] Skipping multimedia parser '{step_name}'")
                continue
            if not is_audio and step_name in AUDIO_PARSER_IDS:
                log.debug(f"🔇 [Multimedia-Branch] Skipping audio parser '{step_name}'")
                continue
        
        # Inject Calibration into Parser Settings
        p_settings = copy.deepcopy(settings)
        p_settings.update(cal_cfg)
        
        is_slow = step_name in SLOW_PARSERS
        if error_shortcircuit:
            log.debug(f"Shortcircuit: Skipping remaining parsers for '{filename}' due to prior error.")
            break
            
        # Category Isolation
        if is_audio and step_name in VIDEO_PARSER_IDS:
             log.debug(f"🔇 [Audio-Branch] Skipping multimedia parser '{step_name}' for '{filename}'")
             continue
        
        if not is_audio and step_name in AUDIO_PARSER_IDS:
             log.debug(f"🔇 [Multimedia-Branch] Skipping audio parser '{step_name}' for '{filename}'")
             continue
        is_slow = step_name in SLOW_PARSERS
        fast_scan = PARSER_CONFIG.get("fast_scan_enabled", True)
        
        # [Fast-Audit] Round 5: Enforce strict timeouts for lightweight mode
        step_timeout = 0.2 if mode == 'lightweight' else 2.0 
        
        if is_slow and mode != 'full' and fast_scan:
            log.debug(f"⏩ [Fast-Scan] Skipping slow parser '{step_name}' for '{filename}'")
            continue
            
        # Magic Byte Verification
        required_magic = REQUIRED_MAGIC.get(step_name)
        if required_magic:
            offset = 32769 if step_name in ["pycdlib", "isoparser"] else 0
            file_magic = get_file_magic(path_obj, len(required_magic), offset=offset)
            if not file_magic.startswith(required_magic):
                log.debug(f"🔍 [Magic-Check] Skipping '{step_name}' for '{filename}': magic {file_magic.hex()} mismatch at {offset}")
                continue
        if mode != 'full':
            has_essential = (
                tags.get('samplerate')
                and tags.get('bitrate')
                and tags.get('bitdepth')
                and tags.get('codec')
                and tags.get('codec') != file_type[1:].lower()
                and tags.get('container')
                and duration
            )
            needs_chapters = file_type in ['.m4b', '.mkv', '.m4a', '.mp4'] and not tags.get('chapters')
            if has_essential and not needs_chapters:
                continue
        current_tags = tags
        attempt = 0
        success = False
        while attempt <= MAX_RETRIES and not success:
            t0 = time.time()
            tags_backup = copy.deepcopy(current_tags)
            try:
                # In ultimate mode, we want a copy of the tags before this parser
                tags_before = current_tags.copy() if mode == 'ultimate' else None
                
                
                # Get parser specific settings from PARSER_CONFIG
                p_settings = PARSER_CONFIG.get('parser_settings', {}).get(step_name, {})
                
                if step_name in ["pymediainfo", "pycdlib", "isoparser"]:
                    # Optimization: Skip heavy parsers for very large ISO files
                    # They tend to cause extreme memory spikes during full/deep scans (Centralized v1.46.102)
                    limits = GLOBAL_CONFIG.get("parser_limits", {})
                    heavy_skip_mb = limits.get("heavy_parser_skip_size_mb", 500)
                    
                    if file_type == ".iso" and path_obj.stat().st_size > heavy_skip_mb * 1024 * 1024:
                        log.info(f"[Parser-Audit] Skipping heavy parser '{step_name}' for large ISO: {filename} (> {heavy_skip_mb}MB)")
                        parser_times[step_name] = time.time() - t0
                        success = True
                        continue

                if step_func:
                    new_tags = cast(dict[str, Any], step_func(
                        path_obj, file_type, current_tags.copy(), filename, 
                        mode=('full' if mode == 'ultimate' else mode),
                        settings=p_settings))
                    
                    # 5. Intelligent Metadata Merging (v1.46.132)
                    # We only overwrite Artist/Album/Title if the new value is meaningful.
                    for core_field in ['artist', 'album', 'title']:
                        new_val = new_tags.get(core_field)
                        if new_val and str(new_val).lower() not in ('', 'unknown', 'unbekannt', 'none'):
                            current_tags[core_field] = new_val
                    
                    # Update other tags as usual but preserve full_tags
                    for k, v in new_tags.items():
                        if k not in ['artist', 'album', 'title']:
                            current_tags[k] = v

                    current_tags = sanitize_metadata(current_tags)
                    parser_times[step_name] = time.time() - t0
                    success = True
            except (subprocess.TimeoutExpired, TimeoutError) as e:
                attempt += 1
                current_tags = tags_backup # Restore state
                log.error(f"⏱️ Parser {step_name} timed out for '{filename}' (Attempt {attempt}/{MAX_RETRIES+1}): {e}")
                if attempt > MAX_RETRIES:
                    parser_times[step_name] = time.time() - t0
            except (ImportError, ModuleNotFoundError) as e:
                # Missing dependencies shouldn't be retried
                current_tags = tags_backup # Restore state
                log.error(f"📦 Parser {step_name} failed due to missing dependency for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
                success = True # Skip this parser
            except Exception as e:
                attempt += 1
                current_tags = tags_backup # Restore state
                # Error shortcircuit: skip remaining parsers for typical file errors
                error_str = str(e).lower()
                if any(msg in error_str for msg in ["is a directory", "not a file", "no tag reader found", "mutagen type <class 'nonetype'> not implemented", "failed to read entire volume descriptor", "can't sync to mpeg frame"]):
                    log.error(f"Shortcircuit: {step_name} parser error for '{filename}': {e}")
                    parser_times[step_name] = time.time() - t0
                    error_shortcircuit = True
                    break
                if attempt <= MAX_RETRIES:
                    log.warning(f"⚠️ Parser {step_name} failed (Attempt {attempt}/{MAX_RETRIES+1}) for '{filename}': {e}. Retrying...")
                    time.sleep(0.05 * attempt)
                else:
                    log.error(f"❌ {step_name} parser error after {MAX_RETRIES} retries for '{filename}': {e}")
                    parser_times[step_name] = time.time() - t0
        tags = current_tags
        if 'duration' in tags and tags['duration'] and not duration:
            try:
                duration = int(float(tags['duration']))
            except (ValueError, TypeError):
                duration = 0

    # Final Fallback for Lossy / Missing Bitdepth
    # The user specifically requested formats like MP3 to default to "16 Bit (lossy)"
    # We now use centralized formatting logic.
    if not tags.get('bitdepth'):
        tags['bitdepth'] = format_bitdepth(None, codec=tags.get('codec'), file_type=file_type)

    # Enforce standard formatting for consistency across all parsers
    if tags.get('codec'):
        tags['codec'] = format_codec(tags['codec'])
    if tags.get('container'):
        tags['container'] = format_container(tags['container'], file_type)
    tags['tagtype'] = format_tagtype(tags.get('tagtype'))
    
    # 🧪 Forensic Integrity Auditor (Phase 10 Validation)
    if feature_flags.get("integrity_auditor", True):
        discrepancies = perform_forensic_validation(tags, parser_times)
        if discrepancies:
            tags['validation_flags'] = discrepancies
            log.warning(f"⚖️ [Forensic-Audit] Metadata discrepancies found for '{filename}': {discrepancies}")

    # 🛡️ Final sanitization pass (Centralized Limits)
    tags = sanitize_metadata(tags)

    # 💾 Forensic Export (Phase 10 Separate Storage)
    if mode == 'ultimate' or feature_flags.get("enable_forensic_export", False):
        store_forensic_export(path_obj, tags)

    # 📑 Final Chapter Sort (Centralized v1.46.132)
    if feature_flags.get("extract_chapters", True) and tags.get('chapters') and isinstance(tags['chapters'], list):
        from .format_utils import natural_sort_key
        # Detect chapter variants
        nero_variant = any('chapter' in c and 'start_time' in c for c in tags['chapters'])
        apple_variant = any('title' in c and 'start' in c for c in tags['chapters'])
        both_variants = nero_variant and apple_variant
        variant_str = (
            'Beide Varianten (Nero & Apple)' if both_variants else
            'Nero-Variante' if nero_variant else
            'Apple-Variante' if apple_variant else
            'Unbekannte Variante'
        )
        log.info(f"[Parser-Chapters] Variant detected: {variant_str} for '{filename}'")
        
        # Priority: 1. Natural Title, 2. Start Time
        tags['chapters'] = sorted(tags['chapters'], key=lambda x: (
            natural_sort_key(x.get('title', '')), x.get('start', 0.0)))
            
        if log.isEnabledFor(10): # DEBUG level
            first_chaps = [c.get('title') for c in tags['chapters'][:5]]
            log.debug(f"[Parser-Chapters] Sorted {len(tags['chapters'])} chapters. First 5: {first_chaps}")

    total_time = sum(parser_times.values())
    timing_report = ", ".join([f"{p}: {t:.3f}s" for p, t in parser_times.items() if t > 0.001])
    log.info(f"[Parser-Trace] Metadata extraction complete for {filename} in {total_time:.3f}s.")
    if timing_report:
        log.info(f"[Parser-Trace] ⏱️ Detailed Timings: {timing_report}")
        
    return cast(dict[str, Any], tags), parser_times

def perform_forensic_validation(tags: dict[str, Any], parser_results: dict[str, float]) -> list[str]:
    """
    @brief Compares results from different parsers to identify discrepancies (Phase 10).
    """
    # 1. Audit Simulation (Phase 11)
    cal_cfg = GLOBAL_CONFIG.get("calibration_registry", {})
    flags: list[str] = []
    if cal_cfg.get("error_simulation_active", False):
        flags.append("Audit-Simulation: Discrepancy Injected for Validation Testing")
        # Mutate a random value to trigger discrepancies if needed
        if 'duration' in tags:
            tags['full_tags']['simulated_error_duration'] = float(tags['duration']) + 60.0

    # 1. Duration Validation (Critical)
    durations = {}
    for k, v in tags.get('full_tags', {}).items():
        if 'duration' in k.lower() or 'ebml_duration' in k.lower():
            try:
                durations[k] = float(v)
            except (ValueError, TypeError):
                continue
    
    if len(durations) > 1:
        vals = durations.values()
        if max(vals) - min(vals) > 5.0:
            flags.append(f"Duration Discrepancy: {min(vals)}s to {max(vals)}s across {len(durations)} engines")
            
    # 2. Codec Validation
    # (Future: compare vlc_codec vs ffprobe_codec)
    
    return flags

def store_forensic_export(path_obj: Path, tags: dict[str, Any]):
    """
    @brief Serializes full_tags to a timestamped JSON file (Phase 10).
    """
    try:
        import json
        from datetime import datetime
        
        export_root = Path(GLOBAL_CONFIG.get("project_root", ".")) / "data" / "forensic_exports"
        export_root.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = f"{path_obj.name}.{ts}.forensic.json"
        export_path = export_root / export_name
        
        # Deep copy to avoid mutating original tags during serialization
        export_data = {
            "source_file": str(path_obj),
            "timestamp": ts,
            "metadata": tags
        }
        
        with export_path.open('w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=4, default=str)
            
        log.info(f"💾 [Forensic-Export] Full tags archived to {export_path.name}")
    except Exception as e:
        log.error(f"❌ [Forensic-Export] Failed to save archive for {path_obj.name}: {e}")

