import yt_dlp
from faster_whisper import WhisperModel
from ollama import Client

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'audio.wav'
    except Exception as e:
        raise Exception(f"Error downloading audio: {str(e)}")

def transcribe_audio(audio_file):
    # Explicitly specify CPU device and compute type
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_file)
    return " ".join([segment.text for segment in segments])

ollama_client = Client()

def generate_notes_and_summary_stream(transcript):
    prompt = f"""
    Based on the following transcript of a video, create:
    1. A set of concise, informative notes
    2. A brief summary of the main points

    Transcript:
    {transcript}

    Notes and Summary:
    """
    
    stream = ollama_client.generate(model='llama3.1:latest', prompt=prompt, stream=True)
    for chunk in stream:
        yield chunk['response']

def process_video(url):
    try:
        audio_file = download_audio(url)
        transcript = transcribe_audio(audio_file)
        return generate_notes_and_summary_stream(transcript)
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")