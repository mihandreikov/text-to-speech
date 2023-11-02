from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from gtts import gTTS
from fastapi.middleware.cors import CORSMiddleware

import io

app = FastAPI()

# Define the CORS settings
origins = [
    "*",
    "http://localhost", 
    "http://localhost:3000",
]

# Add the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)


@app.get("/ping")
async def root():
  return {"pong"}


@app.get("/generate_audio/")
async def generate_audio(number: int, language: str = "en"):
    # Convert the integer to a spoken text
    spoken_text = str(number)

    # Use gTTS to generate speech from the spoken text
    tts = gTTS(spoken_text, lang=language)

    # Save the generated speech as an audio file in memory
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)

    # Seek to the beginning of the file
    audio_bytes.seek(0)

    # Create a streaming response for the audio
    return StreamingResponse(audio_bytes, media_type="audio/mpeg")
