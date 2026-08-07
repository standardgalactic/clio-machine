#!/usr/bin/env bash
set -euo pipefail

cmd="${1:-}"
shift || true

case "${cmd}" in
  spherepop) exec "$(dirname "$0")/bin/spherepop" "$@" ;;
  forth) exec "$(dirname "$0")/bin/forth" "$@" ;;
  *)
    echo "usage: $0 {spherepop|forth} ..." >&2
    exit 1
    ;;
esac
