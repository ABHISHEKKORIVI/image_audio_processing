import logging
import os
import speech_recognition as sr
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Speech Recognition
r = sr.Recognizer()

# Create the directory if it doesn't exist
if not os.path.exists('extracted_data'):
    os.makedirs('extracted_data')


# Function to extract text from audio using PocketSphinx
def extract_text_from_audio(audio_path):
    try:
        logging.info('Extracting text from audio: %s', audio_path)

        # Convert the audio file to WAV format (required by PocketSphinx)
        print("Convert the audio file to WAV format (required by PocketSphinx)")
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000)  # PocketSphinx requires 16kHz audio
        audio.export(audio_path + '.wav', format='wav')

        # Use PocketSphinx to transcribe the audio file to text
        with sr.AudioFile(audio_path + '.wav') as source:
            audio = r.record(source)
            text = r.recognize_sphinx(audio)

            # Print and save the extracted text
            print("Text:", text)
            out_path = os.path.join('extracted_data', f"extracted_{os.path.basename(audio_path)}_text.txt")
            with open(out_path, "w") as f_out:
                f_out.write(f"Text: {text}")

        # Delete the temporary WAV file
        os.remove(audio_path + '.wav')

    except Exception as e:
        logging.error('Error extracting text from audio: %s', e)


# Main function
if __name__ == '__main__':
    directory_path = input("Enter directory path: ")
    file_type = input("Enter file type (audio): ")

    if file_type.lower() == 'audio':
        logger.info('Extracting text from audio...')
        for filename in os.listdir(directory_path):
            if filename.endswith(".wav") or filename.endswith(".m4a"):
                audio_path = os.path.join(directory_path, filename)
                extract_text_from_audio(audio_path)
    else:
        logger.error('Invalid file type specified.')
        exit(1)
