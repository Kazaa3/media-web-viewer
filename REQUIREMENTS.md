# Media Web Viewer - Requirement Mapping

This document maps the project requirements to the corresponding automated tests.

## 1. Core Logic & FFmpeg Integration
| Requirement | Test Path |
|-------------|-----------|
| FFmpeg metadata extraction accuracy | `tests/integration/category/tech/ffmpeg/` |
| 24-bit PCM detection | `tests/integration/category/tech/ffmpeg/test_ffmpeg_pcm_detection.py` |
| Video format diversity support | `tests/integration/category/video/test_video_format_diversity.py` |

## 2. Environment & Stability
| Requirement | Test Path |
|-------------|-----------|
| Python environment validation | `tests/integration/basic/env/test_python_environments.py` |
| UI Session Stability (Long-running) | `tests/integration/category/ui/test_ui_session_stability.py` |
| Environment dependency hygiene | `tests/integration/basic/env/test_environment_packages_fallback.py` |

## 3. CI/CD & Security
| Requirement | Test Path |
|-------------|-----------|
| Git history binary protection | `tests/integration/category/git/test_git_guard.py` |
| Version synchronization | `tests/integration/test_version_sync.py` |
| Clean Install/Reinstall via DEB | `tests/e2e/install/test_reinstall_deb.py` |

## 4. Performance & Scale
| Requirement | Test Path |
|-------------|-----------|
| Media scan performance | `tests/integration/performance/benchmark_scanner.py` |
| Database write overhead | `tests/integration/performance/benchmark_debug_db_write_speed.py` |
| System responsiveness under load | `tests/integration/performance/test_performance_probes.py` |

## 5. UI & Interaction
| Requirement | Test Path |
|-------------|-----------|
| Library media visibility | `tests/integration/category/ui/test_ui_media_visibility.py` |
| Playlist interaction (Selenium) | `tests/e2e/selenium/` |
