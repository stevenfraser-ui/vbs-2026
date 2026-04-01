"""Sound effects utility — plays audio via HTML/JS injection in Streamlit."""

import base64
import logging
from pathlib import Path

import streamlit.components.v1 as components

from src.config.settings import ASSETS_PATH

SOUNDS_DIR = ASSETS_PATH / "sounds"

logger = logging.getLogger(__name__)


def _play_audio_html(file_path: Path, volume: float = 0.5) -> str:
    """Generate HTML that auto-plays an audio file."""
    if not file_path.exists() or file_path.stat().st_size == 0:
        logger.warning("Audio file missing or empty: %s", file_path.name)
        return ""  # Skip empty placeholder files

    audio_bytes = file_path.read_bytes()
    b64 = base64.b64encode(audio_bytes).decode()
    mime = "audio/mpeg" if file_path.suffix == ".mp3" else "audio/wav"

    return f"""
    <audio autoplay>
        <source src="data:{mime};base64,{b64}" type="{mime}">
    </audio>
    <script>
        var audio = document.querySelector('audio');
        if (audio) {{ audio.volume = {volume}; }}
    </script>
    """


def play_sound(sound_name: str, volume: float = 0.5):
    """
    Play a sound effect by name.

    Available sounds: message_beep, unlock_chime, scan_sweep,
                      phase_complete, typing_click
    """
    file_path = SOUNDS_DIR / f"{sound_name}.mp3"
    logger.debug("Playing sound: %s", sound_name)
    html = _play_audio_html(file_path, volume)
    if html:
        components.html(html, height=0, width=0)


def play_message_beep():
    play_sound("message_beep", 0.3)


def play_unlock_chime():
    play_sound("unlock_chime", 0.5)


def play_scan_sweep():
    play_sound("scan_sweep", 0.3)


def play_phase_complete():
    play_sound("phase_complete", 0.6)
