#!/bin/bash
#
# Generate a run case from templates/ (CLAUDE.md 1.3, 8.3).
# Supports:
#   --chamber microgreen (default)
#   --chamber veggie
#   --chamber aph
#
# Cases in runs/ are DISPOSABLE. Any result must be reproducible from this
# script plus a parameter set -- so never hand-edit a generated case, change
# the parameters or the template and regenerate.
#
# Usage:
#   scripts/generate_case.sh --name p1_baseline_m2 [options]
#
# Options:
#   --chamber NAME    microgreen|veggie|aph         default microgreen
#   --name    NAME    run directory under runs/     (required)
#   --phase   1|2     1 = simpleFoam (isothermal)   default 1
#                     2 = buoyantSimpleFoam
#   --mesh    m0|m1|m2|m3                           default m2
#                     m0/m1/m2 is the independence ladder; m3 is NOT buildable
#   --Q       M3H     fan volumetric flow, m3/h     default: chamber-specific
#   --portD   MM      port diameter (microgreen)    default 40
#   --diffuser DEG    inlet vane angle (microgreen) default none (control)
#   --diffuserType cascade|radial                   default cascade
#   --vanes   N       vanes in the diffuser         default 5
#   --bellowsH MM     bellows height (veggie)       default 350
#   --fanSpeed low|high fan setting (veggie)        default high
#   --airVel  M_S     inlet velocity (aph)          default 0.6
#   --g       VALUE   gravity magnitude, m/s2       default 9.81
#   --led     WATTS   LED panel power (phase 2)     default 38.4
#   --model   kOmegaSST|laminar                     default kOmegaSST
#
#   --transient       time-accurate run: phase 1 -> pimpleFoam,
#                     phase 2 -> buoyantPimpleFoam.
#   --endTime   S     transient end time, seconds   default 6.6 * tau
#   --avgStart  S     start time averaging, seconds default 2.75 * tau
#   --frames    N     write times over the run     default 60
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CHAMBER=microgreen
NAME="" ; PHASE=1 ; MESH=m2 ; Q_M3H="" ; GVAL=9.81 ; LED=38.4 ; MODEL=kOmegaSST
TRANSIENT=0 ; END_TIME="" ; AVG_START="" ; JETREFINE=0
PORT_D_MM=40 ; DIFF_TILT="" ; DIFF_VANES="" ; DIFF_TYPE=cascade
BELLOWS_H_MM=350 ; FAN_SPEED=high ; AIR_VEL=0.6
FRAMES=60

FAN_QFREE=18.69 ; FAN_DPMAX=27.4 ; KSYS=2.5 ; RHO_AIR=1.2
N_TAU_END=6.6 ; N_TAU_AVG=2.75

# Portable in-place regex replacement
py_replace() {
    python3 -c "
import sys, re
fpath, pat, repl = sys.argv[1], sys.argv[2], sys.argv[3]
with open(fpath, 'r') as f: content = f.read()
new_content = re.sub(pat, repl, content, flags=re.MULTILINE)
with open(fpath, 'w') as f: f.write(new_content)
" "$1" "$2" "$3"
}

while [ $# -gt 0 ]; do
    case "$1" in
        --chamber)   CHAMBER=$2 ; shift 2 ;;
        --name)      NAME=$2  ; shift 2 ;;
        --phase)     PHASE=$2 ; shift 2 ;;
        --mesh)      MESH=$2  ; shift 2 ;;
        --Q)         Q_M3H=$2 ; shift 2 ;;
        --g)         GVAL=$2  ; shift 2 ;;
        --led)       LED=$2   ; shift 2 ;;
        --model)     MODEL=$2 ; shift 2 ;;
        --transient) TRANSIENT=1 ; shift 1 ;;
        --jetRefine) JETREFINE=1 ; shift 1 ;;
        --portD)     PORT_D_MM=$2 ; shift 2 ;;
        --diffuser)  DIFF_TILT=$2 ; shift 2 ;;
        --vanes)     DIFF_VANES=$2 ; shift 2 ;;
        --diffuserType) DIFF_TYPE=$2 ; shift 2 ;;
        --bellowsH)  BELLOWS_H_MM=$2 ; shift 2 ;;
        --fanSpeed)  FAN_SPEED=$2 ; shift 2 ;;
        --airVel)    AIR_VEL=$2 ; shift 2 ;;
        --frames)    FRAMES=$2 ; shift 2 ;;
        --endTime)   END_TIME=$2  ; shift 2 ;;
        --avgStart)  AVG_START=$2 ; shift 2 ;;
        *) echo "unknown option: $1" >&2 ; exit 1 ;;
    esac
done

if [ "$TRANSIENT" = 0 ] && [ -n "$AVG_START" ]; then
    echo "--avgStart is transient-only; add --transient" >&2 ; exit 1
fi
[ -n "$NAME" ] || { echo "--name is required" >&2 ; exit 1 ; }

CASE="$ROOT/runs/$NAME"
[ -e "$CASE" ] && { echo "runs/$NAME already exists -- remove it first" >&2 ; exit 1 ; }

set +eu
. /usr/lib/openfoam/openfoam2606/etc/bashrc 2>/dev/null || true
set -eu

case "$CHAMBER" in
    microgreen)  TEMPL_DIR="$ROOT/templates" ;;
    veggie)      TEMPL_DIR="$ROOT/templates_veggie" ;;
    aph)         TEMPL_DIR="$ROOT/templates_aph" ;;
    chromex)     TEMPL_DIR="$ROOT/templates_chromex" ;;
    chromex_pgc) TEMPL_DIR="$ROOT/templates_chromex_pgc" ;;
    *) echo "--chamber must be microgreen, veggie, aph, chromex, or chromex_pgc" >&2 ; exit 1 ;;
esac

mkdir -p "$ROOT/runs"
cp -r "$TEMPL_DIR" "$CASE"
rm -rf "$CASE/0.orig.phase2" "$CASE/transient"
chmod +x "$CASE/Allrun" "$CASE/Allclean"
cd "$CASE"

# --- Mesh Resolution Ladder ---
if [ "$CHAMBER" = "microgreen" ]; then
    case "$MESH" in
        m0) NX=19  ; NY=29  ; NZ=23  ;;
        m1) NX=38  ; NY=58  ; NZ=45  ;;
        m2) NX=76  ; NY=116 ; NZ=90  ;;
        m3) NX=152 ; NY=232 ; NZ=180 ;;
        *)  echo "--mesh must be m0, m1, m2 or m3" >&2 ; exit 1 ;;
    esac
elif [ "$CHAMBER" = "veggie" ]; then
    case "$MESH" in
        m0) NX=45  ; NY=57  ; NZ=57  ;;
        m1) NX=90  ; NY=114 ; NZ=114 ;;
        m2) NX=180 ; NY=228 ; NZ=228 ;;
        *)  echo "--mesh must be m0, m1, or m2" >&2 ; exit 1 ;;
    esac
elif [ "$CHAMBER" = "aph" ]; then
    case "$MESH" in
        m0) NX=69  ; NY=63  ; NZ=78  ;;
        m1) NX=138 ; NY=126 ; NZ=156 ;;
        m2) NX=276 ; NY=252 ; NZ=312 ;;
        *)  echo "--mesh must be m0, m1, or m2" >&2 ; exit 1 ;;
    esac
elif [ "$CHAMBER" = "chromex" ]; then
    case "$MESH" in
        m0) NX=76  ; NY=54  ; NZ=40  ;;
        m1) NX=153 ; NY=108 ; NZ=81  ;;
        m2) NX=306 ; NY=216 ; NZ=162 ;;
        *)  echo "--mesh must be m0, m1, or m2" >&2 ; exit 1 ;;
    esac
elif [ "$CHAMBER" = "chromex_pgc" ]; then
    case "$MESH" in
        m0) NX=28  ; NY=14  ; NZ=57  ;;
        m1) NX=57  ; NY=28  ; NZ=114 ;;
        m2) NX=114 ; NY=57  ; NZ=228 ;;
        *)  echo "--mesh must be m0, m1, or m2" >&2 ; exit 1 ;;
    esac
fi

py_replace "system/blockMeshDict" "^nx\s+[0-9]+;" "nx  $NX;"
py_replace "system/blockMeshDict" "^ny\s+[0-9]+;" "ny  $NY;"
py_replace "system/blockMeshDict" "^nz\s+[0-9]+;" "nz  $NZ;"

# --- Geometry Generation ---
if [ "$CHAMBER" = "microgreen" ]; then
    PORT_R_M=$(awk -v d="$PORT_D_MM" 'BEGIN{printf "%.6f", d/2000.0}')
    GEOM_ARGS="--port-r $PORT_R_M"
    if [ -n "$DIFF_TILT" ]; then
        GEOM_ARGS="$GEOM_ARGS --diffuser-type $DIFF_TYPE --diffuser-tilt $DIFF_TILT"
        [ -n "$DIFF_VANES" ] && GEOM_ARGS="$GEOM_ARGS --diffuser-vanes $DIFF_VANES"
    fi
    printf '%s\n' "$GEOM_ARGS" > system/geometryArgs
    python3 "$ROOT/scripts/make_geometry.py" --case . $GEOM_ARGS --verify > log.makeGeometry 2>&1 \
      || { echo "geometry generation FAILED:" >&2; cat log.makeGeometry >&2; exit 1; }

elif [ "$CHAMBER" = "veggie" ]; then
    GEOM_ARGS="--bellows-h $BELLOWS_H_MM"
    printf '%s\n' "$GEOM_ARGS" > system/geometryArgs
    python3 "$ROOT/scripts/make_veggie_geometry.py" --case . $GEOM_ARGS --verify > log.makeGeometry 2>&1 \
      || { echo "geometry generation FAILED:" >&2; cat log.makeGeometry >&2; exit 1; }

elif [ "$CHAMBER" = "aph" ]; then
    GEOM_ARGS="--air-vel $AIR_VEL"
    printf '%s\n' "$GEOM_ARGS" > system/geometryArgs
    python3 "$ROOT/scripts/make_aph_geometry.py" --case . $GEOM_ARGS --verify > log.makeGeometry 2>&1 \
      || { echo "geometry generation FAILED:" >&2; cat log.makeGeometry >&2; exit 1; }
fi

_geom() { awk -v k="$1" '$1==k{print $2}' constant/triSurface/geometry.info; }

# --- Flow Rates and BCs ---
if [ "$CHAMBER" = "microgreen" ]; then
    A_PORT=$(_geom PORT_AREA)
    V_AIR=$(_geom V_AIR)
    
    if [ -n "$DIFF_TILT" ]; then
        KSYS=$(awk -v k="$KSYS" 'BEGIN{printf "%.3f", k + 0.2}')
    fi
    if [ -z "$Q_M3H" ]; then
        Q_M3H=$(awk -v qf="$FAN_QFREE" -v dp="$FAN_DPMAX" -v k="$KSYS" \
                    -v rho="$RHO_AIR" -v a="$A_PORT" 'BEGIN{
            lo=0; hi=qf;
            for(i=0;i<60;i++){
                q=(lo+hi)/2;
                f=dp*(1-q/qf) - k*0.5*rho*(q/3600.0/a)^2;
                if(f>0) lo=q; else hi=q;
            }
            printf "%.3f", (lo+hi)/2;
        }')
    fi
    Q_M3S=$(awk -v q="$Q_M3H" 'BEGIN{printf "%.6e", q/3600.0}')
    U_IN=$(awk  -v q="$Q_M3S" -v a="$A_PORT" 'BEGIN{printf "%.4f", q/a}')
    RE=$(awk    -v u="$U_IN" -v d="$PORT_D_MM" 'BEGIN{printf "%.0f", u*d/1000.0/1.516e-5}')
    foamDictionary -entry "boundaryField/inlet/volumetricFlowRate" -set "$Q_M3S" 0.orig/U > /dev/null 2>&1 || true

elif [ "$CHAMBER" = "veggie" ]; then
    V_AIR=$(_geom V_AIR)
    [ -n "$V_AIR" ] || V_AIR=0.0376
    if [ -z "$Q_M3H" ]; then
        # High fan = ~50 CFM = 85 m3/h, Low fan = ~25 CFM = 42.5 m3/h
        [ "$FAN_SPEED" = "low" ] && Q_M3H=42.5 || Q_M3H=85.0
    fi
    Q_M3S=$(awk -v q="$Q_M3H" 'BEGIN{printf "%.6e", q/3600.0}')
    U_IN=$(awk -v q="$Q_M3S" 'BEGIN{printf "%.4f", q/(3.14159265*0.025*0.025)}')
    RE=$(awk -v u="$U_IN" 'BEGIN{printf "%.0f", u*0.050/1.516e-5}')
    # For VEGGIE top fan suction: negative flow rate
    Q_NEG=$(awk -v q="$Q_M3S" 'BEGIN{printf "%.6e", -q}')
    foamDictionary -entry "boundaryField/fan_exhaust/volumetricFlowRate" -set "$Q_NEG" 0.orig/U > /dev/null 2>&1 || true

elif [ "$CHAMBER" = "aph" ]; then
    V_AIR=$(_geom V_AIR)
    [ -n "$V_AIR" ] || V_AIR=0.0834
    A_INLET=$(_geom INLET_AREA)
    [ -n "$A_INLET" ] || A_INLET=0.00612
    if [ -z "$Q_M3H" ]; then
        Q_SINGLE=$(awk -v v="$AIR_VEL" -v a="$A_INLET" 'BEGIN{printf "%.6e", v*a}')
        Q_M3S=$(awk -v q="$Q_SINGLE" 'BEGIN{printf "%.6e", 2.0*q}')
        Q_M3H=$(awk -v q="$Q_M3S" 'BEGIN{printf "%.3f", q*3600.0}')
    else
        Q_M3S=$(awk -v q="$Q_M3H" 'BEGIN{printf "%.6e", q/3600.0}')
        Q_SINGLE=$(awk -v q="$Q_M3S" 'BEGIN{printf "%.6e", q/2.0}')
    fi
    U_IN=$AIR_VEL
    RE=$(awk -v u="$AIR_VEL" 'BEGIN{printf "%.0f", u*0.015/1.516e-5}')
    foamDictionary -entry "boundaryField/left_inlet/volumetricFlowRate" -set "$Q_SINGLE" 0.orig/U > /dev/null 2>&1 || true
    foamDictionary -entry "boundaryField/right_inlet/volumetricFlowRate" -set "$Q_SINGLE" 0.orig/U > /dev/null 2>&1 || true
fi

ACH=$(awk -v q="$Q_M3H" -v v="$V_AIR" 'BEGIN{printf "%.0f", q/v}')
TAU=$(awk -v q="$Q_M3S" -v v="$V_AIR" 'BEGIN{printf "%.2f", v/q}')

# Gravity and Turbulence
foamDictionary -entry value -set "(0 0 -$GVAL)" constant/g > /dev/null 2>&1 || true
if [ "$MODEL" = laminar ]; then
    foamDictionary -entry simulationType -set laminar constant/turbulenceProperties > /dev/null 2>&1 || true
else
    foamDictionary -entry RAS/RASModel -set "$MODEL" constant/turbulenceProperties > /dev/null 2>&1 || true
fi

# Transient vs Steady
if [ "$TRANSIENT" = 1 ]; then
    [ -n "$END_TIME" ]  || END_TIME=$(awk  -v t="$TAU" -v n="$N_TAU_END" 'BEGIN{printf "%.2f", t*n}')
    [ -n "$AVG_START" ] || AVG_START=$(awk -v t="$TAU" -v n="$N_TAU_AVG" 'BEGIN{printf "%.2f", t*n}')
    WRITE_INT=$(awk -v e="$END_TIME" -v n="$FRAMES" 'BEGIN{printf "%.6g", e/n}')
    py_replace "system/controlDict" "^endTime\s+.*" "endTime         $END_TIME;"
    py_replace "system/controlDict" "^writeInterval\s+.*" "writeInterval   $WRITE_INT;"
elif [ -n "$END_TIME" ]; then
    py_replace "system/controlDict" "^endTime\s+.*" "endTime         $END_TIME;"
fi

# Solver selection
if [ "$PHASE" = 2 ]; then
    SOLVER=$( [ "$TRANSIENT" = 1 ] && echo buoyantPimpleFoam || echo buoyantSimpleFoam )
else
    SOLVER=$( [ "$TRANSIENT" = 1 ] && echo pimpleFoam || echo simpleFoam )
fi
py_replace "system/controlDict" "^application\s+.*" "application     $SOLVER;"

cat > NOTES.md <<EOF
# $NAME

Generated $(date -Iseconds) by scripts/generate_case.sh -- do not hand-edit this case.

## Parameters

| | |
|---|---|
| Chamber | $CHAMBER |
| Phase / solver | $PHASE / \`$SOLVER\` |
| Time treatment | $( [ "$TRANSIENT" = 1 ] && echo "transient" || echo "steady" ) |
| Mesh level | $MESH ($NX x $NY x $NZ background) |
| Turbulence | $MODEL |
| Q | $Q_M3H m3/h = $Q_M3S m3/s |
| ACH | $ACH h^-1 |
| tau (residence) | $TAU s |
| g | $GVAL m/s2 |
EOF

echo "created runs/$NAME ($CHAMBER)"
echo "  solver     $SOLVER   mesh $MESH ($NX x $NY x $NZ)   model $MODEL"
echo "  Q          $Q_M3H m3/h  ->  ACH $ACH   tau ${TAU}s"
echo "  cd runs/$NAME && ./Allrun"
