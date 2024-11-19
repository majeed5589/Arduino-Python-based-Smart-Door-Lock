import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import serial
import time
import pyttsx3

# Counters and flags
q = 1
unlocked_counter = 0
locked_counter = 0
door_open_flag = 0
face_not_found_counter = 0

# Training the model
while q <= 2:
    data_path = 'C:/Users/AbdulMajeed/Desktop/python/image/'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    Training_data, Labels = [], []
    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Resize images to ensure they are the same size
        images = cv2.resize(images, (200, 200))
        Training_data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_data), np.asarray(Labels))
    print("Training complete")
    q += 1

# Load the face classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Text-to-speech engine setup
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 140)
engine.setProperty("volume", 1.0)

# Face detection function
def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return img, []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))

    return img, roi

# Start video capture
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)
        if result[1] < 500:
            confidence = int((1 - (result[1]) / 300) * 100)
            display_string = f'{confidence}% Confidence'
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 0, 0), 2)

        if confidence >= 53:
            cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Face Recognition', image)
            unlocked_counter += 1
        else:
            cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Recognition', image)
            locked_counter += 1
    except:
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow('Face Recognition', image)
        face_not_found_counter += 1
        pass

    if cv2.waitKey(1) == 13 or unlocked_counter == 10 or locked_counter == 30 or face_not_found_counter == 20:
        break

cap.release()
cv2.destroyAllWindows()

# Communicate with Arduino based on recognition result
if unlocked_counter >= 5:
    door_open_flag = 1
    ard = serial.Serial('COM3', 9600)
    time.sleep(2)
    var = 'a'
    encoded_var = var.encode()
    speak("Face recognition complete. It is matching with database. Welcome sir. Door is opening for 5 seconds.")
    ard.write(encoded_var)
    time.sleep(5)
elif locked_counter == 30:
    speak("Face is not matching. Please try again.")
elif face_not_found_counter == 20:
    speak("Face not found. Please try again.")

if door_open_flag == 1:
    speak("Door is closing.")
