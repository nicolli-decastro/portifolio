import openai
import os

# Configure the OpenAI API key
OPENAI_API_KEY = os.environ['openai_key']
openai.api_key = OPENAI_API_KEY

# Specify the input (audio_dir) and output (transcript_dir) directories
audio_dir = "audio_files"
transcript_dir = "transcript_files"

def transcribe():
    # Create the transcription directory if it doesn't exist
    os.makedirs(transcript_dir, exist_ok=True)
    
    # Iterate over the audio files in the input directory
    for filename in os.listdir(audio_dir):
        
        # Get the filename without the extension
        name = os.path.splitext(filename)[0]
        
        # Define the input and output file paths
        audio_path = os.path.join(audio_dir, filename)
        transcript_path = os.path.join(transcript_dir, f"{name}_transcript.txt")
        
        # Transcribe the audio file using OpenAI's Whisper model
        with open(audio_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", file=audio_file)
            transcript = response["text"]
        
        # Save the transcription to the output file
        with open(transcript_path, "w") as transcript_file:
            transcript_file.write(transcript)
        
        print(f"Transcription saved for the file {name}")

    return None

# Call the transcribe() function to start the transcription process
transcribe()
