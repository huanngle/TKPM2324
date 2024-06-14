import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Text to convert to speech
text = "Hello, how is the weather today?"

# Save the speech to an audio file
audio_path = "/mnt/data/hello_how_are_you.mp3"
engine.save_to_file(text, audio_path)

# Run the event loop to process all commands
engine.runAndWait()

audio_path


