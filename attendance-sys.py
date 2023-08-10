#!/usr/bin/env python3

import cv2
import face_recognition
import os
import numpy as np

# Load dataset and encode known faces


def load_known_faces(dataset_path):
    known_faces = []
    known_names = []

    for person_name in os.listdir(dataset_path):
        person_dir = os.path.join(dataset_path, person_name)
        if os.path.isdir(person_dir):
            for image_filename in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                known_faces.append(encoding)
                known_names.append(person_name)

    return known_faces, known_names


# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Load known faces
dataset_path = 'datasets'
known_faces, known_names = load_known_faces(dataset_path)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find faces in the frame
    # face_locations = face_recognition.face_locations(frame)
    # face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_encodings = face_recognition.face_encodings(frame)
    if len(face_encodings) > 0:
        face_locations = face_recognition.face_locations(frame)
    else:
        face_locations = []

    face_locations = face_recognition.face_locations(frame, model='cnn')

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Match the face with known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        if True in matches:
            matched_indices = [i for i, match in enumerate(matches) if match]
            name = known_names[matched_indices[0]]

            # Print name in terminal
            print("Recognized:", name)

            # Write to attendance file
            with open("attendance.txt", "a") as f:
                f.write(name + "\n")

            # Ask if person wants to try again
            try_again = input("Do you want to try again? (y/n): ")
            if try_again.lower() != "y":
                break

        # Draw rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()
