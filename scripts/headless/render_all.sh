#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="${1:-renders}"
BLENDER_BIN="${2:-blender}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SCENES=(
  01_pop_field.py
  02_bind_lattice.py
  03_refuse_frontier.py
  04_collapse_representation.py
  05_history_frontier.py
  06_nested_continuations.py
  07_repair_cycle.py
  08_observer_dependent_collapse.py
  09_recursive_city.py
  10_spherepop_cosmology.py
)

for scene in "${SCENES[@]}"; do
  "${SCRIPT_DIR}/render_scene.sh" "${scene}" "${OUTPUT_DIR}" "${BLENDER_BIN}"
done
