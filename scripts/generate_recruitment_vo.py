import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("Error: The 'openai' library is not installed. Please install it using 'pip install openai'.")
    sys.exit(1)

if not os.environ.get("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it using: export OPENAI_API_KEY='your-api-key'")
    sys.exit(1)

client = OpenAI()

# Recruitment video VO lines — IMF Director (voice: onyx)
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

voice = "onyx"

print(f"Generating recruitment voiceover using OpenAI TTS (Voice: {voice})...")
print(f"Output directory: {output_dir}\n")

for line in vo_lines:
    output_path = os.path.join(output_dir, line["filename"])
    print(f"[Beat {line['beat']}] Generating: {line['filename']}...")
    with client.audio.speech.with_streaming_response.create(
        model="tts-1-hd",
        voice=voice,
        input=line["text"]
    ) as response:
        response.stream_to_file(output_path)
    print(f"  Saved: {output_path}")

print("\nAll recruitment voiceovers generated successfully!")
print(f"Files written to: {output_dir}")
