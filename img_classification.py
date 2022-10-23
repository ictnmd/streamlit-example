import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageOps
import numpy as np


def fruit_classification(img, weights_file):
    # Load the model
    model = keras.models.load_model(weights_file)

    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = img
    #image sizing
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 255.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference

    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    return index, confidence_score