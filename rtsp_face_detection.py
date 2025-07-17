import cv2
import os
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Create output folder
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Use a simulated RTSP source (for now, just your webcam)
# Replace this with your RTSP stream URL if needed
rtsp_url = 'sample.mp4'  # 0 = default webcam. Replace with 'rtsp://...' to use RTSP.

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open video stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    logging.error("Failed to connec to stream")
    exit()

logging.info("Connected to stream")

frame_count = 0
saved_frames = 0

while saved_frames < 5:  # Save 5 annotated frames
    ret, frame = cap.read()
    if not ret:
        logging.warning("Dropped frame")
        continue

    start_time = time.time()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Run face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    inference_time = time.time() - start_time
    logging.info(f"Inference time: {inference_time:.2f} seconds, Faces detected::: {len(faces)}")

    # Save annotated frame
    filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
    saved = cv2.imwrite(filename, frame)
    if saved:
        logging.info(f" Saved frame to i {filename}")
    else:
        logging.error(f" Failed to save frame to {filename}")

    saved_frames += 1
    frame_count += 1

cap.release()
cv2.destroyAllWindows()
logging.info("Completed saving annotated frames.")
