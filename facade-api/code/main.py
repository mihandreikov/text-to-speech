from fastapi import FastAPI
from fastapi import File, UploadFile, Form, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum

import io
import httpx

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


image_to_text_microservice_url = "http://image-to-text-service"  # Replace with the actual URL

# URL of the text-to-audio microservice
translate_api_microservice_url = "http://translate-api-service"  # Replace with the actual URL


class SupportedLanguages(str, Enum):
    en = "en"
    es = "es"
    fr = "fr"


class ProcessImageRequest(BaseModel):
    image: UploadFile
    language: SupportedLanguages


@app.post("/image-to-audio/")
async def generate_audio(image: UploadFile = File(...),
                        language: SupportedLanguages = Form(...)):
    print(f'Got image and language {language}')
    async with httpx.AsyncClient() as client:
        image_data = await image.read()
        response = await client.post(f"{image_to_text_microservice_url}/predict",
                                     files={"image": (image.filename, image_data, image.content_type)})
        response_json = response.json()
        number = response_json.get("number")

    async with httpx.AsyncClient() as client:
        audio_response = await client.get(f"{translate_api_microservice_url}/generate_audio/?number={number}&language={language}")

        # Read the audio data
        audio_data = audio_response.content

    return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")

