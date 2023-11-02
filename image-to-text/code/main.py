import numpy as np
import logging
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageOps 
from tensorflow.keras import models  # Use the TensorFlow version
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Define the CORS settings
origins = [
    # TODO Remove it after debug
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


model = models.load_model("trained-models/trained_model_v2.h5")


@app.get("/predict_simple")
async def predict_simple():
  im = Image.open(r"sample_images/five.jpg")
  label = predict_number(im)

  return {"number": str(label[0])}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        logging.info(f'File received: {file.filename}')
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)

        im = Image.open(file.filename)
        logging.info(im.size)
        label = predict_number(im)
        logging.info(f'Number received: {str(label[0])}')
        response_data = {"number": str(label[0])}

        return JSONResponse(content=response_data)
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return JSONResponse(content={"message": "There was an error uploading or processing the file"}, status_code=500)
    finally:
        file.file.close()


def predict_number(image):
    im = image.convert('L').resize((28, 28))
    im = ImageOps.invert(im)

    img = np.array(im)
    img = np.array(img) / 255.0
    img = img.reshape(1, 28, 28, 1)

    predictions = model.predict(img)
    label = np.argmax(predictions, axis=1)
    # log to console what is prediction we have for all numbers. Useful for debug
    for index, element in enumerate(predictions[0]):
        formatted_num = '{:.6f}'.format(element)  # Adjust the number of decimal places as needed
        print(f"Digit {index}: {formatted_num}")

    return label
