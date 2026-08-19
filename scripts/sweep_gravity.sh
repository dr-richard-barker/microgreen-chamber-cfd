#!/bin/bash
#
# Phase 3 gravity sweep for Microgreen, VEGGIE, or APH chambers.
#
# The knob is ONE FILE: constant/g. Mesh, turbulence model and BCs stay frozen
# across the sweep or the result is not interpretable.
#
# Usage:
#   scripts/sweep_gravity.sh [--chamber microgreen|veggie|aph]
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CHAMBER=${CHAMBER:-microgreen}

while [ $# -gt 0 ]; do
    case "$1" in
        --chamber) CHAMBER=$2 ; shift 2 ;;
        *) break ;;
    esac
done

MESH=${MESH:-m0}
MODEL=${MODEL:-kOmegaSST}
CPUSET=${FOAM_CPUSET:-0-7}
GVALS=${GVALS:-"0 1.62 3.72 9.81"}

if [ "$CHAMBER" = "microgreen" ]; then
    Q=${Q:-11.8}
    LED=${LED:-38.4}
elif [ "$CHAMBER" = "veggie" ]; then
    Q=${Q:-85.0}
    LED=${LED:-50.0}
elif [ "$CHAMBER" = "aph" ]; then
    Q=${Q:-26.4}
    LED=${LED:-100.0}
fi

N=$(echo "$GVALS" | wc -w)
cat <<EOF
=== Phase 3 gravity sweep ($CHAMBER)
    mesh $MESH   Q $Q m3/h   model $MODEL   LED $LED W
    g values: $GVALS  ($N cases)
EOF

for G in $GVALS; do
    TAG=$(printf "%.3f" "$G" | tr '.' 'p')
    NAME="${CHAMBER}_g_${TAG}_${MESH}"

    echo
    echo "=== $NAME  (g = $G m/s2)"
    [ -e "$ROOT/runs/$NAME" ] && { echo "    exists, skipping"; continue; }

    "$ROOT/scripts/generate_case.sh" --chamber "$CHAMBER" --name "$NAME" --phase 2 \
        --mesh "$MESH" --Q "$Q" --led "$LED" --model "$MODEL" --g "$G"

    ( cd "$ROOT/runs/$NAME" && FOAM_CPUSET="$CPUSET" ./Allrun ) || {
        echo "!! $NAME did not complete or requires OpenFOAM environment."
    }
done

echo
echo "=== sweep generation complete for $CHAMBER ==="
