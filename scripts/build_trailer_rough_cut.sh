#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TRAILER_DIR="$ROOT_DIR/video/teaser_trailer"
VIDEO_DIR="$TRAILER_DIR/video"
VO_DIR="$TRAILER_DIR/audio/VO"
SFX_DIR="$TRAILER_DIR/audio/SFX"
MUSIC_DIR="$TRAILER_DIR/audio/Music"
OUT_DIR="$TRAILER_DIR/video"
TMP_DIR="$TRAILER_DIR/.tmp"

mkdir -p "$TMP_DIR"

"$ROOT_DIR/scripts/validate_trailer_assets.sh"

FFMPEG_BIN="${FFMPEG_BIN:-}"
if [[ -z "$FFMPEG_BIN" ]]; then
  if command -v ffmpeg >/dev/null 2>&1 && ffmpeg -version >/dev/null 2>&1; then
    FFMPEG_BIN="$(command -v ffmpeg)"
  else
    if command -v python3 >/dev/null 2>&1; then
      FFMPEG_BIN="$(python3 - <<'PY'
try:
    import imageio_ffmpeg
    print(imageio_ffmpeg.get_ffmpeg_exe())
except Exception:
    print("")
PY
)"
    fi
  fi
fi

if [[ -z "$FFMPEG_BIN" || ! -x "$FFMPEG_BIN" ]]; then
  echo "ffmpeg is required but no compatible binary was found."
  echo "Install an Apple Silicon compatible ffmpeg or run: python3 -m pip install --user imageio-ffmpeg"
  exit 1
fi

echo "Using ffmpeg: $FFMPEG_BIN"

# Build a concat list in timeline order.
CONCAT_LIST="$TMP_DIR/concat_list.txt"
cat > "$CONCAT_LIST" <<EOF
file '$VIDEO_DIR/01_recruitment_notice.mp4'
file '$VIDEO_DIR/02_agent_roles.mp4'
file '$VIDEO_DIR/03_training_together.mp4'
file '$VIDEO_DIR/04_breach_and_regroup.mp4'
file '$VIDEO_DIR/05_accept_the_mission.mp4'
EOF

VIDEO_STITCHED="$TMP_DIR/video_stitched.mp4"
VO_MIX="$TMP_DIR/vo_mix.wav"
SFX_MIX="$TMP_DIR/sfx_mix.wav"
MUSIC_MIX="$TMP_DIR/music_mix.wav"
FINAL_OUT="$OUT_DIR/teaser_trailer_rough_cut.mp4"

# Concatenate video clips without re-encoding where possible.
"$FFMPEG_BIN" -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$VIDEO_STITCHED"

# Mix VO lines in sequence with short spacing to keep pace.
"$FFMPEG_BIN" -y \
  -i "$VO_DIR/vo_01_mission_starts.mp3" \
  -i "$VO_DIR/vo_02_every_role.mp3" \
  -i "$VO_DIR/vo_03_train_together.mp3" \
  -i "$VO_DIR/vo_04_stand_together.mp3" \
  -i "$VO_DIR/vo_05_do_you_accept.mp3" \
  -filter_complex "[0:a]adelay=0|0[a0];[1:a]adelay=5000|5000[a1];[2:a]adelay=11000|11000[a2];[3:a]adelay=18000|18000[a3];[4:a]adelay=24000|24000[a4];[a0][a1][a2][a3][a4]amix=inputs=5:normalize=0,volume=1.5" \
  "$VO_MIX"

# Place SFX at key trailer beats.
"$FFMPEG_BIN" -y \
  -i "$SFX_DIR/sfx_boot_hit.wav" \
  -i "$SFX_DIR/sfx_ui_beeps.wav" \
  -i "$SFX_DIR/sfx_glitch_breach.wav" \
  -i "$SFX_DIR/sfx_impact_hit.wav" \
  -i "$SFX_DIR/sfx_final_rise.wav" \
  -filter_complex "[0:a]adelay=0|0[s0];[1:a]adelay=600|600[s1];[2:a]adelay=12000|12000[s2];[3:a]adelay=22000|22000[s3];[4:a]adelay=26800|26800[s4];[s0][s1][s2][s3][s4]amix=inputs=5:normalize=0,volume=1.0" \
  "$SFX_MIX"

# Prepare music bed.
"$FFMPEG_BIN" -y -i "$MUSIC_DIR/music_spy_bed.wav" -af "volume=0.22" "$MUSIC_MIX"

# Final mix and output.
"$FFMPEG_BIN" -y \
  -i "$VIDEO_STITCHED" \
  -i "$VO_MIX" \
  -i "$SFX_MIX" \
  -i "$MUSIC_MIX" \
  -filter_complex "[1:a][2:a][3:a]amix=inputs=3:normalize=0:duration=first[a]" \
  -map 0:v:0 -map "[a]" \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest \
  "$FINAL_OUT"

echo "Rough cut created: $FINAL_OUT"
