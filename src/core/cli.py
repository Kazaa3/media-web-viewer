#!/usr/bin/env python3
"""Minimal `mwv-cli` implementation (lightweight, lazy imports).

Designed for headless/CI usage. Keep imports lazy to avoid heavy side-effects
when the module is imported by tests.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from typing import Any


def _get_callable_from_module(name: str, module_name: str):
    # prefer local override (for tests monkeypatching)
    local = globals().get(name)
    if callable(local):
        return local
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, name)
    except Exception:
        return None


def _write_output(data: Any, path: str | None):
    out = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
    else:
        print(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='mwv-cli')
    sub = parser.add_subparsers(dest='cmd')

    p = sub.add_parser('parse')
    p.add_argument('path')
    p.add_argument('--output')

    sub.add_parser('health')

    l = sub.add_parser('logs')
    l.add_argument('--limit', type=int, default=200)

    f = sub.add_parser('ffprobe')
    f.add_argument('file')
    f.add_argument('--output')

    args = parser.parse_args(argv)

    if args.cmd == 'parse':
        extract = _get_callable_from_module('extract_metadata', 'main')
        if not extract:
            from src.core.logger import get_logger
            log = get_logger("cli")
            log.error('Error: extract_metadata not available')
            return 2
        try:
            meta = extract(args.path)
            _write_output(meta, getattr(args, 'output', None))
            return 0
        except Exception as e:
            from src.core.logger import get_logger
            log = get_logger("cli")
            log.error(f'Error during parse: {e}')
            return 2

    if args.cmd == 'health':
        info = _get_callable_from_module('get_environment_info', 'main')
        if not info:
            from src.core.logger import get_logger
            log = get_logger("cli")
            log.error('Error: get_environment_info not available')
            return 2
        try:
            _write_output(info(), None)
            return 0
        except Exception as e:
            from src.core.logger import get_logger
            log = get_logger("cli")
            log.error(f'Error during health: {e}')
            return 2

    if args.cmd == 'logs':
        # Use logger.get_ui_logs lazily
        try:
            logger = importlib.import_module('logger')
            get_ui_logs = getattr(logger, 'get_ui_logs')
        except Exception:
            from src.core.logger import get_logger
            log = get_logger("cli")
            log.error('Error: logger.get_ui_logs not available')
            return 2
        logs = get_ui_logs()[: args.limit]
        print('\n'.join(logs))
        return 0

    if args.cmd == 'ffprobe':
        try:
            ffw = importlib.import_module('tools.ffprobe_wrapper')
            res = ffw.run_ffprobe(args.file)
            _write_output(res, getattr(args, 'output', None))
            return 0
        except Exception as e:
            from src.core.logger import get_logger
            log = get_logger("cli")
            log.error(f'Error running ffprobe: {e}')
            return 2

    parser.print_help()
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
