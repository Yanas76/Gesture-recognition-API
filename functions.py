import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def get_recognizer(url, file_name):

    if not os.path.exists(file_name):
        urllib.request.urlretrieve(url, file_name)
        print('Downloaded gesture recognizer model')
    else:
        print('Gesture recognizer already exists')

    base_options = python.BaseOptions(model_asset_path=file_name)
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)

    return recognizer


def get_classification_result_from_path(image_path, recognizer):

    image = mp.Image.create_from_file(image_path)
    result = recognizer.recognize(image)
    gesture = result.gestures[0][0]
    gesture_name = gesture.category_name

    return gesture_name
