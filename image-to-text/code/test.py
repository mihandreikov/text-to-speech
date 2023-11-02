from PIL import Image
from tensorflow import keras
from typing import Union
from fastapi import FastAPI
import numpy as np

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Load the image
image = Image.open('five.jpg')
# Convert the image to grayscale
image = image.convert('L')  # 'L' mode is for grayscale
# Resize the image to match your model's input size (e.g., 28x28)
image = image.resize((28, 28))
# Convert to a numerical array and normalize pixel values
image_data = np.array(image) / 255.0
# Reshape the image data to match the model's input shape
image_data = image_data.reshape(1, 28, 28, 1)
# Load the model
loaded_model = keras.models.load_model("my_model.h5")
# Make predictions
predictions = loaded_model.predict(image_data)

print(predictions)