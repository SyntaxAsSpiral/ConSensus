#!/usr/bin/env bash
# Select arbitrary JSONL records with jq, then render one review document with Knap.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

selector='true'
title='Esocortex record review'
output='selection.md'

usage() {
  echo 'usage: knap/review.sh [--select JQ] [--title TEXT] [--output REVIEW.md] JSONL...' >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --select)
      selector="$2"
      shift 2
      ;;
    --title)
      title="$2"
      shift 2
      ;;
    --output)
      output="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      usage
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -eq 0 ]]; then
  usage
  exit 2
fi

case "$output" in
  */*|.|..)
    echo '--output must be a filename, not a path' >&2
    exit 2
    ;;
esac

while :; do
  chronohex="$(python3 -c 'import time; print(hex(time.time_ns())[-6:])')"
  review_path="docs/review/${chronohex}-${output}"
  [[ ! -e "$review_path" ]] && break
done

data="$(mktemp --suffix=.json)"
trap 'rm -f "$data"' EXIT
mkdir -p docs/review

jq -Rn \
  --arg title "$title" \
  --arg selector "$selector" \
  --arg chronohex "$chronohex" \
  '{
    title: $title,
    selector: $selector,
    chronohex: $chronohex,
    entries: [
      inputs
      | fromjson?
      | select('"$selector"')
      | . + {
          review_file: input_filename,
          review_line: input_line_number,
          display_heading: ([.heading, .title, .id] | map(select(type == "string" and length > 0)) | first),
          key_names: [(.keys // [])[] | if type == "object" then .name else . end]
        }
    ]
  }' "$@" > "$data"

npx -y knap@0.6.0 render knap/review-template.md --data "$data" --output "$review_path"
echo "wrote $(jq '.entries | length' "$data") entries → $review_path"
