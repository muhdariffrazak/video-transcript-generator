#!/usr/bin/env bash
set -euo pipefail

# Run from project root even if called from elsewhere.
cd "$(dirname "$0")"

VIDEO_DIR="${1:-videos}"

if [[ ! -d "$VIDEO_DIR" ]]; then
  mkdir -p "$VIDEO_DIR"
  echo "Created missing video directory: $VIDEO_DIR"
fi

mkdir -p output

echo "Processing videos from: $VIDEO_DIR"

processed=0
failed=0

while IFS= read -r -d '' f; do
  base_name="$(basename "${f%.*}")"
  container_video="/videos/$(basename "$f")"

  echo "---"
  echo "Input:  $f"
  echo "SRT:    /output/${base_name}.srt"
  echo "Output: /output/${base_name}_with_subs.mp4"

  if docker compose run --rm -T transcript-generator \
    transcribe "$container_video" \
    --srt "/output/${base_name}.srt" \
    --output "/output/${base_name}_with_subs.mp4" < /dev/null; then
    processed=$((processed + 1))
  else
    failed=$((failed + 1))
    echo "Failed: $f" >&2
  fi
done < <(find "$VIDEO_DIR" -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.mkv" -o -iname "*.avi" \) -print0)

echo "Done. Success: ${processed}, Failed: ${failed}. Check output/ for generated files."

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi
