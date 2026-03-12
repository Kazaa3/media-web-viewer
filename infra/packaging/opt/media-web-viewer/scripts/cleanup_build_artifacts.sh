#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEEP_DEB="${KEEP_DEB:-5}"
KEEP_DIST="${KEEP_DIST:-2}"
EXECUTE="false"

if [[ "${1:-}" == "--execute" ]]; then
  EXECUTE="true"
fi

echo "==> Cleanup build artifacts in: ${ROOT_DIR}"
echo "    keep deb:  ${KEEP_DEB}"
echo "    keep dist: ${KEEP_DIST}"
echo "    mode:      $([[ "$EXECUTE" == "true" ]] && echo EXECUTE || echo DRY-RUN)"

mapfile -t deb_files < <(find "$ROOT_DIR" -maxdepth 1 -type f -name "media-web-viewer_*_amd64.deb" -printf "%T@ %p\n" | sort -nr | awk '{print $2}')
mapfile -t dist_files < <(find "$ROOT_DIR/dist" -maxdepth 1 -type f -name "MediaWebViewer*" -printf "%T@ %p\n" 2>/dev/null | sort -nr | awk '{print $2}')

delete_deb=()
if (( ${#deb_files[@]} > KEEP_DEB )); then
  delete_deb=("${deb_files[@]:KEEP_DEB}")
fi

delete_dist=()
if (( ${#dist_files[@]} > KEEP_DIST )); then
  delete_dist=("${dist_files[@]:KEEP_DIST}")
fi

if (( ${#delete_deb[@]} == 0 && ${#delete_dist[@]} == 0 )); then
  echo "==> Nothing to clean."
  exit 0
fi

echo "==> Candidate files to remove:"
for f in "${delete_deb[@]}"; do
  echo "  [deb]  $f"
done
for f in "${delete_dist[@]}"; do
  echo "  [dist] $f"
done

if [[ "$EXECUTE" == "true" ]]; then
  rm -f "${delete_deb[@]}" "${delete_dist[@]}"
  echo "==> Cleanup finished."
else
  echo "==> Dry-run only. Re-run with --execute to delete these files."
fi
