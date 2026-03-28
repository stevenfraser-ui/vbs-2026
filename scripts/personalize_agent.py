"""
personalize_agent.py — On-demand per-child recruitment video generator

Takes a child's name and photo, generates their personalized IMF agent badge,
and composites it onto the master recruitment video to produce a unique MP4.

Requires:
    pip install Pillow
    ffmpeg installed (brew install ffmpeg)

Usage:
    # Full pipeline (badge + video):
    python3 scripts/personalize_agent.py \\
        --name "Jane Smith" \\
        --photo video/recruitment/photos/agent-jane-smith.jpg \\
        --master video/recruitment/master.mp4 \\
        --output video/recruitment/final-videos/Agent-Jane-Smith.mp4

    # Badge only (no master video yet):
    python3 scripts/personalize_agent.py \\
        --name "Jane Smith" \\
        --photo video/recruitment/photos/agent-jane-smith.jpg \\
        --badge-only

Personalization slots (v1):
    - Photo: child portrait, color-graded to cinematic blue/silver
    - Name: AGENT FIRSTNAME LASTNAME rendered into badge
    - Agent ID: auto-generated unique code per child
    - VO: generic (no per-child spoken name in v1)
"""

import argparse
import os
import subprocess
import sys
from typing import Optional

# Badge generator lives in the same scripts/ directory
_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)

sys.path.insert(0, _SCRIPT_DIR)
try:
    from generate_badge import generate_badge
except ImportError:
    print("Error: could not import generate_badge. "
          "Ensure generate_badge.py is in the same scripts/ directory.")
    sys.exit(1)


# ── Badge positioning (portrait-first defaults) ──────────────────────────────
# Badge is 480×680 px (from generate_badge.py)
# Defaults are for a 1080×1920 smartphone vertical frame and are recalculated
# dynamically from the master video unless manually overridden.
BADGE_W = 480
BADGE_H = 680
DEFAULT_VIDEO_W = 1080
DEFAULT_VIDEO_H = 1920
BADGE_TARGET_WIDTH_RATIO = 0.44
BADGE_MAX_HEIGHT_RATIO = 0.62

BADGE_X = (DEFAULT_VIDEO_W - BADGE_W) // 2   # = 300
BADGE_Y = (DEFAULT_VIDEO_H - BADGE_H) // 2 + 90  # = 710 — lower-middle in portrait


def _check_ffmpeg() -> bool:
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def _get_video_dimensions(video_path: str) -> Optional[tuple[int, int]]:
    """Return (width, height) using ffprobe, or None if unavailable."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=s=x:p=0",
        video_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dims = result.stdout.strip()
        if "x" not in dims:
            return None
        w, h = dims.split("x", 1)
        return int(w), int(h)
    except Exception:
        return None


def _default_badge_layout(video_w: int, video_h: int) -> tuple[int, int, int, int]:
    """Return (x, y, render_w, render_h) tuned for smartphone-first framing."""
    render_w = max(200, int(video_w * BADGE_TARGET_WIDTH_RATIO))
    render_h = int(render_w * BADGE_H / BADGE_W)

    max_h = int(video_h * BADGE_MAX_HEIGHT_RATIO)
    if render_h > max_h:
        render_h = max_h
        render_w = int(render_h * BADGE_W / BADGE_H)

    x = max(0, (video_w - render_w) // 2)
    y = max(0, int(video_h * 0.56) - (render_h // 2))
    return x, y, render_w, render_h


def _composite_badge(
    master_path: str,
    badge_path:  str,
    output_path: str,
    badge_start: float,
    badge_end:   float,
    badge_x:     int,
    badge_y:     int,
    badge_render_w: int,
    badge_render_h: int,
    fade_in:     float = 0.5,
) -> None:
    """
    Overlay the badge PNG onto the master video between badge_start and badge_end
    with a fade-in transition.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # FFmpeg filter:
    # 0. Scale badge for phone-friendly composition
    # 1. Fade badge in over `fade_in` seconds from `badge_start`
    # 2. Display until `badge_end`
    filter_graph = (
        f"[1:v]scale={badge_render_w}:{badge_render_h},"
        f"fade=in:st={badge_start}:d={fade_in}:alpha=1,"
        f"fade=out:st={badge_end - fade_in}:d={fade_in}:alpha=1"
        f"[badge];"
        f"[0:v][badge]overlay={badge_x}:{badge_y}"
        f":enable='between(t,{badge_start},{badge_end})'"
    )

    # -loop 1 turns the single PNG into a continuous video stream so the
    # fade filters get real timestamps.  -t limits the loop so ffmpeg
    # terminates when the badge window is done.
    loop_duration = str(badge_end + 1)

    cmd = [
        "ffmpeg", "-y",
        "-i", master_path,
        "-loop", "1", "-t", loop_duration, "-i", badge_path,
        "-filter_complex", filter_graph,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "copy",
        output_path
    ]

    print(f"Running FFmpeg composite...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:")
        print(result.stderr)
        sys.exit(1)
    print(f"Video saved: {output_path}")


def personalize_agent(
    name:         str,
    photo_path:   Optional[str],
    master_path:  Optional[str],
    output_path:  Optional[str],
    badge_only:   bool,
    badge_start:  float,
    badge_end:    float,
    badge_x:      Optional[int],
    badge_y:      Optional[int],
    badge_width:  Optional[int],
) -> None:
    safe_name  = name.lower().replace(" ", "-")
    badge_path = os.path.join(
        _PROJECT_ROOT, "video", "recruitment", "badges",
        f"badge-{safe_name}.png"
    )

    # ── Step 1: Generate badge ─────────────────────────────────────────────────
    print(f"\n[1/2] Generating badge for: {name}")
    generate_badge(name, photo_path, badge_path)

    if badge_only:
        print("\nBadge-only mode. Skipping video composite.")
        return

    # ── Step 2: Composite onto master video ────────────────────────────────────
    if not master_path:
        print("\nNo --master video provided. Badge generated but video skipped.")
        print(f"Badge is ready at: {badge_path}")
        print("Re-run with --master once the master video is complete.")
        return

    if not os.path.exists(master_path):
        print(f"Error: master video not found at: {master_path}")
        sys.exit(1)

    if not _check_ffmpeg():
        print("Error: ffmpeg is not installed or not in PATH.")
        print("Install it with: brew install ffmpeg")
        sys.exit(1)

    dims = _get_video_dimensions(master_path)
    if dims is None:
        print("Warning: Could not read video dimensions via ffprobe.")
        print(f"Falling back to portrait defaults: {DEFAULT_VIDEO_W}x{DEFAULT_VIDEO_H}")
        video_w, video_h = DEFAULT_VIDEO_W, DEFAULT_VIDEO_H
    else:
        video_w, video_h = dims

    # Auto-calculate badge placement from master video dimensions unless
    # explicitly overridden via --badge-x / --badge-y.
    auto_x, auto_y, auto_w, auto_h = _default_badge_layout(video_w, video_h)
    badge_x = auto_x if badge_x is None else badge_x
    badge_y = auto_y if badge_y is None else badge_y

    if badge_width is None:
        badge_render_w = auto_w
    else:
        badge_render_w = max(120, badge_width)
    badge_render_h = int(badge_render_w * BADGE_H / BADGE_W)

    if badge_render_h > int(video_h * BADGE_MAX_HEIGHT_RATIO):
        badge_render_h = int(video_h * BADGE_MAX_HEIGHT_RATIO)
        badge_render_w = int(badge_render_h * BADGE_W / BADGE_H)

    print(
        f"Using badge layout: x={badge_x}, y={badge_y}, "
        f"w={badge_render_w}, h={badge_render_h}"
    )

    if not output_path:
        first, last = (name.split(" ", 1) + [""])[:2]
        filename     = f"Agent-{first.capitalize()}-{last.capitalize()}.mp4"
        output_path  = os.path.join(
            _PROJECT_ROOT, "video", "recruitment", "final-videos", filename
        )

    print(f"\n[2/2] Compositing badge onto master video...")
    _composite_badge(
        master_path  = master_path,
        badge_path   = badge_path,
        output_path  = output_path,
        badge_start  = badge_start,
        badge_end    = badge_end,
        badge_x      = badge_x,
        badge_y      = badge_y,
        badge_render_w = badge_render_w,
        badge_render_h = badge_render_h,
    )

    print(f"\nDone. Personalized video ready: {output_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a personalized IMF recruitment video for one child."
    )
    parser.add_argument("--name",    required=True,
                        help='Child full name, e.g. "Jane Smith"')
    parser.add_argument("--photo",   default=None,
                        help="Path to the child portrait photo (optional)")
    parser.add_argument("--master",  default=None,
                        help="Path to the assembled master recruitment video MP4")
    parser.add_argument("--output",  default=None,
                        help="Output MP4 path (default: auto-named in final-videos/)")
    parser.add_argument("--badge-only", action="store_true",
                        help="Generate badge PNG only, skip video composite")
    parser.add_argument("--badge-start", type=float, default=9.0,
                        help="Video timestamp (seconds) when badge appears (default: 9.0)")
    parser.add_argument("--badge-end",   type=float, default=19.0,
                        help="Video timestamp (seconds) when badge disappears (default: 19.0)")
    parser.add_argument("--badge-x", type=int, default=None,
                        help="Badge X position in pixels (default: auto-center based on master video)")
    parser.add_argument("--badge-y", type=int, default=None,
                        help="Badge Y position in pixels (default: auto lower-middle based on master video)")
    parser.add_argument("--badge-width", type=int, default=None,
                        help="Badge render width in pixels (default: auto ~44% of video width)")
    args = parser.parse_args()

    personalize_agent(
        name        = args.name,
        photo_path  = args.photo,
        master_path = args.master,
        output_path = args.output,
        badge_only  = args.badge_only,
        badge_start = args.badge_start,
        badge_end   = args.badge_end,
        badge_x     = args.badge_x,
        badge_y     = args.badge_y,
        badge_width = args.badge_width,
    )


if __name__ == "__main__":
    main()
