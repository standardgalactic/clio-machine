#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <scene-script> [output-dir] [blender-bin]" >&2
  exit 1
fi

SCENE_SCRIPT="$1"
OUTPUT_DIR="${2:-renders}"
BLENDER_BIN="${3:-blender}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCENE_PATH="${REPO_ROOT}/scenes/${SCENE_SCRIPT}"

if [[ ! -f "${SCENE_PATH}" ]]; then
  echo "Scene script not found: ${SCENE_PATH}" >&2
  exit 1
fi

mkdir -p "${REPO_ROOT}/${OUTPUT_DIR}"
SCENE_NAME="${SCENE_SCRIPT%.py}"

"${BLENDER_BIN}" \
  --background \
  --python "${SCENE_PATH}" \
  --render-output "${REPO_ROOT}/${OUTPUT_DIR}/${SCENE_NAME}_####" \
  --render-format PNG \
  --render-anim
