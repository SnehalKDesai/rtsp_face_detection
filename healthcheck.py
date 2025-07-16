import cv2
import sys

# Try opening a dummy video source
cap = cv2.VideoCapture('sample.mp4')

if not cap.isOpened():
    print("Healthcheck failed: Cannot access video stream")
    sys.exit(1)

ret, frame = cap.read()
if not ret or frame is None:
    print("Healthcheck failed: Cannot read frame")
    sys.exit(1)

# Fake inference simulation
try:
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print("Healthcheck passed")
    sys.exit(0)
except:
    print("Healthcheck failed: Model dummy inference failed")
    sys.exit(1)
