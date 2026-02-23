import cv2
import time
import numpy as np
import pygame
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

VIDEO_PATH = resource_path("raahh_fixed.mp4")
AUDIO_PATH = resource_path("raahh_audio.mp3")
XML_PATH = resource_path("haarcascade_frontalface_default.xml")

SECOND_LIMIT = 1.5

pygame.mixer.init()
cap_webcam = cv2.VideoCapture(0)
cap_alarm = cv2.VideoCapture(VIDEO_PATH)

fps = cap_alarm.get(cv2.CAP_PROP_FPS)
frames = cap_alarm.get(cv2.CAP_PROP_FRAME_COUNT)
duration_ms = (frames / fps) * 1000 if fps > 0 else 5000

face_cascade = cv2.CascadeClassifier(XML_PATH)

start_time = None
is_alarm_active = False

def play_sync_alarm():
    if os.path.exists(AUDIO_PATH) and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play(-1)

def stop_sync_alarm():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    cap_alarm.set(cv2.CAP_PROP_POS_FRAMES, 0)

print("Aplikasi Berjalan... Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap_webcam.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        if start_time is None: start_time = time.time()
        elapsed = time.time() - start_time
        if elapsed > SECOND_LIMIT:
            is_alarm_active = True
            play_sync_alarm()
    else:
        start_time = None
        is_alarm_active = False
        stop_sync_alarm()

    if is_alarm_active:
        sync_ms = pygame.mixer.music.get_pos() % duration_ms
        cap_alarm.set(cv2.CAP_PROP_POS_MSEC, sync_ms)
        ret_a, frame_a = cap_alarm.read()
        if ret_a:
            frame_res = cv2.resize(frame_a, (frame.shape[1], frame.shape[0]))
            cv2.imshow("Doomscroll Blocker", frame_res)
        else:
            cv2.imshow("Doomscroll Blocker", frame)
    else:
        if start_time:
            cv2.putText(frame, "GET BACK TO WORK!", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "SCANNING ACTIVE", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Doomscroll Blocker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_webcam.release()
cap_alarm.release()
cv2.destroyAllWindows()