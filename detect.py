import cv2
from ultralytics import YOLO

# Load YOLOv8 face model
model = YOLO("yolov8n-face-lindevs.pt")

# Load Haar cascade untuk mata
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

def detect_faces_and_eyes(image):
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = model(image_bgr)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face_roi = image_bgr[y1:y2, x1:x2]
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

        eyes = eye_cascade.detectMultiScale(gray_face, scaleFactor=1.1, minNeighbors=5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face_roi, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

        cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
