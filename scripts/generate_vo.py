import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("Error: The 'openai' library is not installed. Please install it using 'pip install openai'.")
    sys.exit(1)

# Ensure the API key is set
if not os.environ.get("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it using: export OPENAI_API_KEY='your-api-key'")
    sys.exit(1)

client = OpenAI()

# Define the Voiceover lines from the script
vo_lines = [
    {
        "filename": "vo_01_code_red.mp3",
        "text": "IMF Command to all available recruits. We have a Code Red."
    },
    {
        "filename": "vo_02_the_light.mp3",
        "text": "A device of unimaginable power, The Light, is in danger. And our top agents can't do this alone."
    },
    {
        "filename": "vo_03_the_null.mp3",
        "text": "An unknown enemy has hacked the system. The Null is watching."
    },
    {
        "filename": "vo_04_accept.mp3",
        "text": "We need you. Are you ready to accept the mission?"
    },
    {
        "filename": "vo_05_briefing.mp3",
        "text": "Mission Briefing arriving soon."
    }
]

output_dir = "Teaser_Trailer/Audio/VO"

# We'll use the 'onyx' voice as it's deep and dramatic
voice = "onyx"

print(f"Generating voiceover using OpenAI TTS (Voice: {voice})...")

for line in vo_lines:
    output_path = os.path.join(output_dir, line["filename"])
    print(f"Generating: {line['filename']}...")
    
    response = client.audio.speech.create(
        model="tts-1-hd",  # Use the HD model for better audio quality
        voice=voice,
        input=line["text"]
    )
    
    response.stream_to_file(output_path)
    print(f"Saved to {output_path}")

print("\nAll voiceovers generated successfully!")
