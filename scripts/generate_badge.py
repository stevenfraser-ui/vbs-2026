"""
generate_badge.py — IMF Agent badge generator

Produces a personalized PNG badge for each registered child.
The badge uses a rectangular rounded-corner design with a cinematic
cool blue / silver grade that matches the recruitment video palette.

Usage:
    python3 scripts/generate_badge.py --name "Jane Smith" --photo path/to/photo.jpg
    python3 scripts/generate_badge.py --name "Jane Smith"          # placeholder photo
    python3 scripts/generate_badge.py --name "Jane Smith" --photo path/to/photo.jpg --output custom/path/badge.png
"""

import argparse
import os
import random
import sys
from typing import Optional, Tuple

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFont
except ImportError:
    print("Error: Pillow is not installed. Please install it using 'pip install Pillow'.")
    sys.exit(1)

# ── Dimensions ────────────────────────────────────────────────────────────────
BADGE_W = 480
BADGE_H = 680
CORNER_R = 22

# ── Palette — cool blue / silver cinematic ────────────────────────────────────
BG_COLOR           = (10, 14, 26, 255)     # near-black blue
BORDER_COLOR       = (30, 80, 160)         # IMF blue
BORDER_INNER_COLOR = (30, 80, 160, 60)     # inner accent
ACCENT_COLOR       = (100, 160, 220)       # header text
LABEL_COLOR        = (130, 170, 205)       # secondary labels
NAME_COLOR         = (220, 235, 255)       # agent name
CLASSIFICATION_BG  = (50, 8, 8)           # classification bar background
CLASSIFICATION_FG  = (190, 55, 55)        # classification bar text/border
SCANLINE_COLOR     = (30, 80, 160, 18)    # subtle scanlines


# ── Font loader (tech-forward, bold-first) ───────────────────────────────────
_FONT_TECH_BOLD = [
    "/Library/Fonts/Orbitron-Bold.ttf",
    "/Library/Fonts/Exo2-Bold.ttf",
    "/Library/Fonts/EurostileLTStd-Bold.otf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

_FONT_TECH_REGULAR = [
    "/Library/Fonts/Orbitron-Regular.ttf",
    "/Library/Fonts/Exo2-Regular.ttf",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]

_FONT_UI_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def _load_font_from_candidates(size: int, candidates: list[str]) -> ImageFont.FreeTypeFont:
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size, index=0)
            except Exception:
                continue
    return ImageFont.load_default()


def _load_tech_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    if bold:
        return _load_font_from_candidates(size, _FONT_TECH_BOLD)
    return _load_font_from_candidates(size, _FONT_TECH_REGULAR)


def _load_ui_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    if bold:
        return _load_font_from_candidates(size, _FONT_UI_BOLD)
    return _load_font_from_candidates(size, _FONT_TECH_REGULAR)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _rounded_mask(size: Tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [(0, 0), (size[0] - 1, size[1] - 1)], radius=radius, fill=255
    )
    return mask


def _apply_cinematic_grade(photo: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
    """Center-crop, resize, and apply a cool blue / silver cinematic grade."""
    w, h = photo.size
    dim = min(w, h)
    photo = photo.crop(((w - dim) // 2, (h - dim) // 2,
                         (w + dim) // 2, (h + dim) // 2))
    photo = photo.resize(target_size, Image.LANCZOS)

    if photo.mode != "RGB":
        photo = photo.convert("RGB")

    # Slight desaturation
    photo = ImageEnhance.Color(photo).enhance(0.58)
    # Subtle contrast boost
    photo = ImageEnhance.Contrast(photo).enhance(1.2)
    # Slight darkening
    photo = ImageEnhance.Brightness(photo).enhance(0.82)

    # Cool-tone shift: lift blue, pull red
    r, g, b = photo.split()
    r = r.point(lambda x: int(x * 0.82))
    b = b.point(lambda x: min(255, int(x * 1.28)))
    return Image.merge("RGB", (r, g, b))


def _generate_agent_id() -> str:
    return f"IMF-{random.randint(1000, 9999)}-{random.randint(10, 99)}"


# ── Core badge builder ────────────────────────────────────────────────────────

def generate_badge(
    name: str,
    photo_path: Optional[str],
    output_path: str,
) -> None:
    badge = Image.new("RGBA", (BADGE_W, BADGE_H), (0, 0, 0, 0))

    # Background
    bg = Image.new("RGBA", (BADGE_W, BADGE_H), BG_COLOR)
    outer_mask = _rounded_mask((BADGE_W, BADGE_H), CORNER_R)
    badge.paste(bg, (0, 0), outer_mask)

    # Scanlines
    scan = Image.new("RGBA", (BADGE_W, BADGE_H), (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scan)
    for y in range(0, BADGE_H, 4):
        scan_draw.line([(0, y), (BADGE_W, y)], fill=SCANLINE_COLOR, width=1)
    badge = Image.alpha_composite(badge, scan)

    draw = ImageDraw.Draw(badge)

    # Outer border
    draw.rounded_rectangle(
        [(2, 2), (BADGE_W - 3, BADGE_H - 3)],
        radius=CORNER_R, outline=BORDER_COLOR, width=2
    )
    # Inner accent border
    draw.rounded_rectangle(
        [(6, 6), (BADGE_W - 7, BADGE_H - 7)],
        radius=CORNER_R - 2, outline=BORDER_INNER_COLOR, width=1
    )

    # Fonts (bold, technical visual language)
    f_header = _load_tech_font(15, bold=True)
    f_label  = _load_tech_font(15, bold=True)
    f_name   = _load_tech_font(32, bold=True)
    f_small  = _load_ui_font(12, bold=True)

    # ── IMF AGENCY header ──────────────────────────────────────────────────────
    header_y = 20
    draw.text((BADGE_W // 2, header_y), "IMPOSSIBLE MISSION FORCE",
              font=f_header, fill=ACCENT_COLOR, anchor="mt")

    sep1_y = header_y + 30
    draw.line([(24, sep1_y), (BADGE_W - 24, sep1_y)], fill=BORDER_COLOR, width=1)

    # ── Photo area ─────────────────────────────────────────────────────────────
    photo_margin = 32
    photo_size   = BADGE_W - (photo_margin * 2)   # 416 px square
    photo_y      = sep1_y + 16
    photo_rect   = [(photo_margin, photo_y),
                    (photo_margin + photo_size, photo_y + photo_size)]

    if photo_path and os.path.exists(photo_path):
        try:
            raw = Image.open(photo_path).convert("RGB")
            graded = _apply_cinematic_grade(raw, (photo_size, photo_size))
            photo_mask = _rounded_mask((photo_size, photo_size), 10)
            graded_rgba = graded.convert("RGBA")
            graded_rgba.putalpha(photo_mask)
            badge.paste(graded_rgba, (photo_margin, photo_y), graded_rgba)
        except Exception as e:
            print(f"Warning: could not load photo ({e}) — using placeholder.")
            _draw_photo_placeholder(draw, photo_rect, f_label)
    else:
        _draw_photo_placeholder(draw, photo_rect, f_label)

    # Re-acquire draw handle after paste operations
    draw = ImageDraw.Draw(badge)

    # Photo border overlay
    draw.rounded_rectangle(photo_rect, radius=10, outline=BORDER_COLOR, width=2)

    # ── AGENT label ────────────────────────────────────────────────────────────
    label_y = photo_y + photo_size + 16
    draw.text((BADGE_W // 2, label_y), "AGENT",
              font=f_label, fill=LABEL_COLOR, anchor="mt")

    # ── Agent name ─────────────────────────────────────────────────────────────
    name_y = label_y + 20
    draw.text((BADGE_W // 2, name_y), name.upper(),
              font=f_name, fill=NAME_COLOR, anchor="mt")

    sep2_y = name_y + 40
    draw.line([(24, sep2_y), (BADGE_W - 24, sep2_y)], fill=BORDER_COLOR, width=1)

    # ── Agent ID ───────────────────────────────────────────────────────────────
    id_y = sep2_y + 10
    draw.text((BADGE_W // 2, id_y), _generate_agent_id(),
              font=f_small, fill=LABEL_COLOR, anchor="mt")

    # ── Classification bar ─────────────────────────────────────────────────────
    bar_h = 30
    bar_y = BADGE_H - bar_h - 10
    draw.rectangle(
        [(photo_margin, bar_y), (BADGE_W - photo_margin, bar_y + bar_h)],
        fill=CLASSIFICATION_BG
    )
    draw.rectangle(
        [(photo_margin, bar_y), (BADGE_W - photo_margin, bar_y + bar_h)],
        outline=CLASSIFICATION_FG, width=1
    )
    draw.text((BADGE_W // 2, bar_y + bar_h // 2),
              "CLASSIFIED — IMF USE ONLY",
              font=f_small, fill=CLASSIFICATION_FG, anchor="mm")

    # ── Apply outer rounded mask to final composite ────────────────────────────
    badge.putalpha(_rounded_mask((BADGE_W, BADGE_H), CORNER_R))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    badge.save(output_path, "PNG")
    print(f"Badge saved: {output_path}")


def _draw_photo_placeholder(
    draw: ImageDraw.ImageDraw,
    rect: list,
    font: ImageFont.FreeTypeFont,
) -> None:
    draw.rounded_rectangle(rect, radius=10, fill=(18, 28, 45), outline=BORDER_COLOR, width=1)
    cx = (rect[0][0] + rect[1][0]) // 2
    cy = (rect[0][1] + rect[1][1]) // 2
    draw.text((cx, cy), "[PHOTO PLACEHOLDER]",
              font=font, fill=LABEL_COLOR, anchor="mm")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a personalized IMF agent badge PNG."
    )
    parser.add_argument("--name",   required=True,
                        help='Agent full name, e.g. "Jane Smith"')
    parser.add_argument("--photo",  default=None,
                        help="Path to the agent portrait photo (optional)")
    parser.add_argument("--output", default=None,
                        help="Output PNG path (default: video/recruitment/badges/badge-<name>.png)")
    args = parser.parse_args()

    if args.output:
        output_path = args.output
    else:
        script_dir   = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        safe_name    = args.name.lower().replace(" ", "-")
        output_path  = os.path.join(
            project_root, "video", "recruitment", "badges",
            f"badge-{safe_name}.png"
        )

    generate_badge(args.name, args.photo, output_path)


if __name__ == "__main__":
    main()
