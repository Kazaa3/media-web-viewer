#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from typing import Iterable, Optional

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page, sync_playwright


DEFAULT_APP_URL = "http://localhost:8345"

QUEUE_SELECTORS = [
    '[data-testid="queue-item"]',
    '[data-track-id]',
    '#player-queue .queue-item',
    '#sidebar-queue .queue-item',
    '.queue-item',
    '.player-queue-item',
    '#queue-list li',
    '.queue-list li',
    'aside .track-item',
]

TITLE_SELECTOR = "#big-player-title"
PROGRESS_SELECTORS = [
    '[data-state="playing"]',
    '.is-playing',
    '.playing',
    '.player--playing',
    '#player-progress.playing',
    '.progress-bar.playing',
]


@dataclass
class Checkpoint:
    name: str
    passed: bool
    detail: str


def log(msg: str) -> None:
    print(f"[playback_verify] {msg}", flush=True)


def fail(reason: str, checkpoints: list[Checkpoint], exit_code: int = 1) -> None:
    print("\nFAILURE", flush=True)
    print(f"Reason: {reason}", flush=True)
    print("\nCheckpoints:", flush=True)
    for cp in checkpoints:
        status = "PASS" if cp.passed else "FAIL"
        print(f"- {status}: {cp.name} -> {cp.detail}", flush=True)
    sys.exit(exit_code)


def success(checkpoints: list[Checkpoint]) -> None:
    print("\nSUCCESS", flush=True)
    print("Playback verification passed.", flush=True)
    print("\nCheckpoints:", flush=True)
    for cp in checkpoints:
        print(f"- PASS: {cp.name} -> {cp.detail}", flush=True)


def first_visible_selector(page: Page, selectors: Iterable[str], timeout_ms: int = 1000) -> Optional[str]:
    for selector in selectors:
        locator = page.locator(selector)
        try:
            if locator.first.is_visible(timeout=timeout_ms):
                return selector
        except Exception:
            continue
    return None


def get_media_state(page: Page) -> tuple[bool, float]:
    data = page.evaluate(
        """
        () => {
            const media = document.querySelector('audio, video');
            if (!media) return { exists: false, paused: true, currentTime: 0 };
            return {
                exists: true,
                paused: !!media.paused,
                currentTime: Number(media.currentTime || 0)
            };
        }
        """
    )
    if not data.get("exists"):
        return False, 0.0
    return (not data.get("paused", True)), float(data.get("currentTime", 0.0))


def has_progress_playing_indicator(page: Page) -> bool:
    selector = first_visible_selector(page, PROGRESS_SELECTORS, timeout_ms=200)
    return selector is not None


def wait_for_tracks(page: Page, timeout_ms: int = 20000) -> str:
    start = time.time()
    while (time.time() - start) * 1000 < timeout_ms:
        selector = first_visible_selector(page, QUEUE_SELECTORS, timeout_ms=250)
        if selector:
            count = page.locator(selector).count()
            if count > 0:
                return selector
        time.sleep(0.25)
    raise PlaywrightTimeoutError("No playable Titel found in queue/sidebar within timeout")


def wait_for_playback_transition(page: Page, timeout_s: float = 12.0) -> tuple[bool, str]:
    _, before_t = get_media_state(page)
    start = time.time()

    while time.time() - start < timeout_s:
        is_playing, now_t = get_media_state(page)
        progress_flag = has_progress_playing_indicator(page)
        if is_playing and now_t > before_t + 0.15:
            return True, f"Media active (currentTime {before_t:.2f} -> {now_t:.2f})"
        if progress_flag and now_t > before_t + 0.05:
            return True, "Progress state indicates playing and media time advances"
        time.sleep(0.4)

    return False, "Playback transition not observed (media time/class did not move to playing)"


def main() -> None:
    app_url = os.getenv("APP_URL", DEFAULT_APP_URL)
    headless = os.getenv("PLAYBACK_VERIFY_HEADLESS", "0").strip() in {"1", "true", "True"}
    keep_open_ms = int(os.getenv("PLAYBACK_VERIFY_KEEP_OPEN_MS", "3500"))

    checkpoints: list[Checkpoint] = []
    log(f"Connecting to: {app_url}")
    log(f"Headless: {headless}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(app_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
            checkpoints.append(Checkpoint("Application connection", True, f"Loaded {app_url}"))
        except Exception as exc:
            checkpoints.append(Checkpoint("Application connection", False, str(exc)))
            fail("Could not load application URL", checkpoints)

        # Probe title baseline
        initial_title = ""
        try:
            page.wait_for_selector(TITLE_SELECTOR, timeout=7000)
            initial_title = (page.locator(TITLE_SELECTOR).first.inner_text() or "").strip()
            checkpoints.append(Checkpoint("Player title probe", True, f"Initial title: '{initial_title}'"))
        except Exception as exc:
            checkpoints.append(Checkpoint("Player title probe", False, str(exc)))
            fail("Missing #big-player-title", checkpoints)

        # Find first Titel in queue/sidebar and trigger playback
        try:
            queue_selector = wait_for_tracks(page, timeout_ms=25000)
            first_track = page.locator(queue_selector).first
            label = (first_track.inner_text() or "").strip().replace("\n", " ")
            first_track.click(timeout=5000)
            checkpoints.append(Checkpoint("Trigger playback", True, f"Clicked first Titel via {queue_selector}: '{label[:100]}'"))
        except Exception as exc:
            checkpoints.append(Checkpoint("Trigger playback", False, str(exc)))
            fail("Unable to find/click first Titel", checkpoints)

        # Verify title updates and playing state/progress transitions
        title_updated = False
        try:
            start = time.time()
            while time.time() - start < 10:
                current_title = (page.locator(TITLE_SELECTOR).first.inner_text() or "").strip()
                if current_title and current_title != initial_title:
                    title_updated = True
                    break
                time.sleep(0.3)

            if title_updated:
                checkpoints.append(Checkpoint("DOM assertion: title update", True, "#big-player-title updated after playback trigger"))
            else:
                checkpoints.append(Checkpoint("DOM assertion: title update", False, "Title did not change within timeout"))
                fail("Playback title update not detected", checkpoints)
        except Exception as exc:
            checkpoints.append(Checkpoint("DOM assertion: title update", False, str(exc)))
            fail("Error while verifying title update", checkpoints)

        playing_ok, detail = wait_for_playback_transition(page, timeout_s=12.0)
        if not playing_ok:
            checkpoints.append(Checkpoint("DOM assertion: progress/playing state", False, detail))
            fail("Playback state did not transition to active", checkpoints)

        checkpoints.append(Checkpoint("DOM assertion: progress/playing state", True, detail))

        success(checkpoints)
        log(f"Keeping browser open for {keep_open_ms} ms for visual confirmation...")
        page.wait_for_timeout(keep_open_ms)

        context.close()
        browser.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFAILURE", flush=True)
        print("Reason: Interrupted by user", flush=True)
        sys.exit(130)
