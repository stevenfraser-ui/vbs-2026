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
        "filename": "vo_01_mission_starts.mp3",
        "text": "This is a message for new recruits. Your mission starts now."
    },
    {
        "filename": "vo_02_every_role.mp3",
        "text": "Every team needs problem-solvers, encouragers, and brave hearts."
    },
    {
        "filename": "vo_03_train_together.mp3",
        "text": "You will learn to trust your team, help others, and stay on mission."
    },
    {
        "filename": "vo_04_stand_together.mp3",
        "text": "The Null is trying to break the signal. Real agents stand together."
    },
    {
        "filename": "vo_05_do_you_accept.mp3",
        "text": "The Impossible Mission. Do you accept?"
    }
]

# Get the script's directory and construct absolute path to output
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
output_dir = os.path.join(project_root, "video", "teaser_trailer", "audio", "VO")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# We'll use the 'onyx' voice as it's deep and dramatic
voice = "onyx"

print(f"Generating voiceover using OpenAI TTS (Voice: {voice})...")
print(f"Output directory: {output_dir}")

for line in vo_lines:
    output_path = os.path.join(output_dir, line["filename"])
    print(f"Generating: {line['filename']}...")
    
    with client.audio.speech.with_streaming_response.create(
        model="tts-1-hd",  # Use the HD model for better audio quality
        voice=voice,
        input=line["text"]
    ) as response:
        response.stream_to_file(output_path)
    print(f"Saved to {output_path}")

print("\nAll voiceovers generated successfully!")
