#!/usr/bin/env bash
# Append a row to results/discovery_log.tsv with a live UTC timestamp.
# usage: log.sh <kind> <ref> <outcome> [note]
set -euo pipefail
LOG="$(cd "$(dirname "$0")/.." && pwd)/results/discovery_log.tsv"
n=$(( $(wc -l < "$LOG") ))   # header counts as line 1 -> next step = lines
ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
kind="$1"; ref="$2"; outcome="$3"; note="${4:-}"
clean() { printf '%s' "$1" | tr '\t\n' '  '; }
printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$ts" "$(clean "$kind")" "$(clean "$ref")" "$(clean "$outcome")" "$(clean "$note")" >> "$LOG"
