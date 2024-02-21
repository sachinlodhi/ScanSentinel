import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import cv2

model_path = os.path.join(os.path.dirname(__file__), 'models', 'trained_model.hdf5')
model = load_model(model_path)

def predict(img_path):
    class_names = ["benign", "malicious"]
    img_height, img_width = 296, 296

    img = tf.keras.utils.load_img(img_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    predicted_class = class_names[np.argmax(score)]
    confidence = 100 * np.max(score)

    qr_image = cv2.imread(img_path)
    decoded_text = None

    gray = cv2.cvtColor(qr_image, cv2.COLOR_BGR2GRAY)
    qr_decoder = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qr_decoder.detectAndDecodeMulti(gray)

    if retval:
        decoded_text = decoded_info[0]

    return predicted_class, confidence, decoded_text