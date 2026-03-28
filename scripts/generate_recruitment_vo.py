"""
generate_recruitment_vo.py — Generate recruitment video voiceover using ElevenLabs TTS

Requires:
    pip install elevenlabs
    export ELEVENLABS_API_KEY="your-api-key"

Usage:
    python3 scripts/generate_recruitment_vo.py
    python3 scripts/generate_recruitment_vo.py --voice "Antoni"
    python3 scripts/generate_recruitment_vo.py --list-voices
"""

import argparse
import os
import sys

try:
    from elevenlabs import ElevenLabs
except ImportError:
    print("Error: The 'elevenlabs' library is not installed.")
    print("Install it using: pip install elevenlabs")
    sys.exit(1)

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not API_KEY:
    print("Error: ELEVENLABS_API_KEY environment variable not set.")
    print("Please set it using: export ELEVENLABS_API_KEY='your-api-key'")
    sys.exit(1)

client = ElevenLabs(api_key=API_KEY)

# Recruitment video VO lines — IMF Director
# Beat 1: Mission Hook (0:00–0:09)
# Beat 2: Agent Badge Reveal (0:09–0:19)
# Beat 3: Final Call to Action (0:19–0:27)
vo_lines = [
    {
        "filename": "rec_vo_01_secure.mp3",
        "text": "This channel is secure.",
        "beat": 1
    },
    {
        "filename": "rec_vo_02_activating.mp3",
        "text": "The IMF is activating a new recruit.",
        "beat": 1
    },
    {
        "filename": "rec_vo_03_classified_mission.mp3",
        "text": "You have been selected for a classified mission.",
        "beat": 1
    },
    {
        "filename": "rec_vo_04_report_training.mp3",
        "text": "Prepare to report for training.",
        "beat": 1
    },
    {
        "filename": "rec_vo_05_assignment.mp3",
        "text": "Clearance confirmed. Further instructions will arrive in a separate transmission.",
        "beat": 2
    },
    {
        "filename": "rec_vo_06_cta.mp3",
        "text": "Await the signal. Answer the call. Join the IMF.",
        "beat": 3
    },
]

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
output_dir = os.path.join(project_root, "video", "recruitment", "audio", "VO")

os.makedirs(output_dir, exist_ok=True)


# ── Built-in voice name → ID map (ElevenLabs pre-made voices) ─────────────────
VOICE_MAP = {
    "adam":      "pNInz6obpgDQGcFmaJgB",
    "alice":     "Xb7hH8MSUJpSbSDYk0k2",
    "antoni":    "ErXwobaYiN019PkySvjV",
    "aria":      "9BWtsMINqrJLrRacOk9x",
    "arnold":    "VR6AewLTigWG4xSOukaG",
    "bella":     "hpp4J3VqNfWAUOO0d1Us",
    "bill":      "pqHfZKP75CvOlQylNhV4",
    "brian":     "nPczCjzI2devNBz1zQrb",
    "callum":    "N2lVS1w4EtoT3dr4eOWO",
    "charlie":   "IKne3meq5aSn9XLyUdCD",
    "charlotte": "XB0fDUnXU5powFXDhCwa",
    "chris":     "iP95p4xoKVk53GoZ742B",
    "cinematic trailer": "ZGgk7KqsgEdrlwJ93DA8",
    "clyde":     "2EiwWnXFnvU5JabPnv8n",
    "dallin":    "alFofuDn3cOwyoz1i44T",
    "daniel":    "onwK4e9ZLuTAKqWW03F9",
    "dave":      "CYw3kZ02Hs0563khs1Fj",
    "domi":      "AZnzlk1XvdvUeBnXmlld",
    "dorothy":   "ThT5KcBeYPX3keUQqHPh",
    "drew":      "29vD33N1CtxCmqQRPOHJ",
    "drew romantic": "65dhNaIr3Y4ovumVtdy0",
    "elli":      "MF3mGyEYCl7XYWbV9V6O",
    "emily":     "LcfcDJNUP1GQjkzn1xUU",
    "eric":      "cjVigY5qzO86Huf0OWal",
    "ethan":     "g5CIjZEefAph4nQFvHAz",
    "fin":       "D38z5RcWu1voky8WS1ja",
    "freya":     "jsCqWAovK2LkecY7zXl4",
    "george":    "JBFqnCBsd6RMkjVDRZzb",
    "gigi":      "jBpfuIE2acCO8z3wKNLl",
    "giovanni":  "zcAOhNBS3c14rBihAFp1",
    "glinda":    "z9fAnlkpzviPz146aGWa",
    "grace":     "oWAxZDx7w5VEj9dCyTzz",
    "harry":     "SOYHLrjzK2X1ezoPC6cr",
    "james":     "ZQe5CZNOzWyzPSCn5a3c",
    "jeremy":    "bVMeCyTHy58xNoL34h3p",
    "jessica":   "cgSgspJ2msm6clMCkdW9",
    "jessie":    "t0jbNlBVZ17f02VDIeMI",
    "john doe gentle": "iLzHtPh0bW6RGWRG0Xo5",
    "josh":      "TxGEqnHWrfWFTfGW9XjX",
    "kent":      "nGOINycDFt5Lv8UNXX65",
    "laura":     "FGY2WhTYpPnrIDTdsKH5",
    "liam":      "TX3LPaxmHKxFdv7VOQHJ",
    "lily":      "pFZP5JQG7iQjIQuC4Bku",
    "matilda":   "XrExE9yKIg1WjnnlVkGX",
    "michael":   "flq6f7yk4E4fJM5XTYuZ",
    "mimi":      "zrHiDhphv9ZnVXBqCLjz",
    "mr. noir":  "JftoyuzDFEXApFCWv9CQ",
    "nicole":    "piTKgcLEGmPE4e6mEKli",
    "patrick":   "ODq5zmih8GrVes37Dizd",
    "paul":      "5Q0t7uMcjvnagumLfvZi",
    "rachel":    "21m00Tcm4TlvDq8ikWAM",
    "river":     "SAz9YHcvj6GT2YYXdXww",
    "roger":     "CwhRBWXzGAHq8TQ4Fs17",
    "sam":       "yoZ06aMxZJJ28mfd3POQ",
    "sarah":     "EXAVITQu4vr4xnSDxMaL",
    "serena":    "pMsXgVXv3BLzUgSXRplE",
    "thomas":    "GBv7mTt0atIp3Br8iCZE",
    "true crime": "tZssYepgGaQmegsMEXjK",
    "will":      "bIHbv24MWmeRgasZH58o",
}


def list_voices():
    """Print built-in voices and any additional voices from the API."""
    print(f"{'Name':<25} {'Voice ID':<25} {'Source'}")
    print("-" * 70)
    for name, vid in sorted(VOICE_MAP.items()):
        print(f"{name:<25} {vid:<25} built-in")

    # Also fetch any custom/cloned voices from the API
    try:
        response = client.voices.get_all()
        for voice in response.voices:
            if voice.name.lower() not in VOICE_MAP:
                labels = ", ".join(f"{k}={v}" for k, v in (voice.labels or {}).items())
                print(f"{voice.name:<25} {voice.voice_id:<25} api ({labels})")
    except Exception:
        pass


def resolve_voice_id(voice_name: str) -> str:
    """Resolve a voice name to its ID using the built-in map or API fallback."""
    # If it looks like a raw voice ID (long alphanumeric), use directly
    if len(voice_name) > 15 and voice_name.isalnum():
        return voice_name

    # Check built-in map first
    key = voice_name.lower()
    if key in VOICE_MAP:
        return VOICE_MAP[key]

    # Fallback to API lookup for custom/cloned voices
    try:
        response = client.voices.get_all()
        for voice in response.voices:
            if voice.name.lower() == key:
                return voice.voice_id
    except Exception:
        pass

    print(f"Error: Voice '{voice_name}' not found. Use --list-voices to see available voices.")
    sys.exit(1)


def generate(voice_name: str, model: str):
    voice_id = resolve_voice_id(voice_name)
    safe_voice = voice_name.lower().replace(" ", "-")
    print(f"Generating recruitment voiceover using ElevenLabs TTS")
    print(f"  Voice: {voice_name} ({voice_id})")
    print(f"  Model: {model}")
    print(f"  Output: {output_dir}\n")

    for line in vo_lines:
        base, ext = os.path.splitext(line["filename"])
        out_filename = f"{base}_{safe_voice}{ext}"
        output_path = os.path.join(output_dir, out_filename)
        print(f"[Beat {line['beat']}] Generating: {out_filename}...")

        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=line["text"],
            model_id=model,
            output_format="mp3_44100_128",
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        size_kb = os.path.getsize(output_path) / 1024
        print(f"  Saved: {output_path} ({size_kb:.1f} KB)")

    print("\nAll recruitment voiceovers generated successfully!")
    print(f"Files written to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate recruitment VO using ElevenLabs TTS"
    )
    parser.add_argument("--voice", default="Antoni",
                        help='Voice name or ID (default: "Antoni"). Use --list-voices to browse.')
    parser.add_argument("--model", default="eleven_multilingual_v2",
                        help='Model ID (default: eleven_multilingual_v2)')
    parser.add_argument("--list-voices", action="store_true",
                        help="List available voices and exit")
    args = parser.parse_args()

    if args.list_voices:
        list_voices()
        return

    generate(args.voice, args.model)


if __name__ == "__main__":
    main()
