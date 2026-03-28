#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TRAILER_DIR="$ROOT_DIR/video/teaser_trailer"
VIDEO_DIR="$TRAILER_DIR/video"
VO_DIR="$TRAILER_DIR/audio/VO"
SFX_DIR="$TRAILER_DIR/audio/SFX"
MUSIC_DIR="$TRAILER_DIR/audio/Music"

required_video=(
  "01_recruitment_notice.mp4"
  "02_agent_roles.mp4"
  "03_training_together.mp4"
  "04_breach_and_regroup.mp4"
  "05_accept_the_mission.mp4"
)

required_vo=(
  "vo_01_mission_starts.mp3"
  "vo_02_every_role.mp3"
  "vo_03_train_together.mp3"
  "vo_04_stand_together.mp3"
  "vo_05_do_you_accept.mp3"
)

required_sfx=(
  "sfx_boot_hit.wav"
  "sfx_ui_beeps.wav"
  "sfx_glitch_breach.wav"
  "sfx_impact_hit.wav"
  "sfx_final_rise.wav"
)

required_music=(
  "music_spy_bed.wav"
)

missing=0

check_files() {
  local dir="$1"
  shift
  local files=("$@")

  for f in "${files[@]}"; do
    if [[ ! -f "$dir/$f" ]]; then
      echo "MISSING: $dir/$f"
      missing=1
    fi
  done
}

echo "Checking teaser trailer asset folders..."
check_files "$VIDEO_DIR" "${required_video[@]}"
check_files "$VO_DIR" "${required_vo[@]}"
check_files "$SFX_DIR" "${required_sfx[@]}"
check_files "$MUSIC_DIR" "${required_music[@]}"

if [[ "$missing" -eq 1 ]]; then
  echo
  echo "Asset check failed. Add the missing files and rerun."
  exit 1
fi

echo

echo "All required assets are present."
