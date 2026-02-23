import cv2
import face_recognition
import time
import numpy as np
import pygame
import os

VIDEO_PATH = "raahh_fixed.mp4"
AUDIO_PATH = "raahh_audio.mp3"
LIMIT_DETIK = 1.5
SCALE = 0.25   

pygame.mixer.init()
cap_webcam = cv2.VideoCapture(0)
cap_alarm = None
start_time = None
is_alarm_active = False

def play_sound():
    if os.path.exists(AUDIO_PATH) and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play(-1) 

def stop_sound():
    pygame.mixer.music.stop()

print("Aplikasi Berjalan... Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap_webcam.read()
    if not ret: break

    small_frame = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

    if len(face_locations) == 0:
        if start_time is None:
            start_time = time.time()
        
        elapsed = time.time() - start_time
        
        if elapsed > LIMIT_DETIK:
            is_alarm_active = True
            play_sound()
    else:
        start_time = None
        is_alarm_active = False
        stop_sound()
        if cap_alarm is not None:
            cap_alarm.release()
            cap_alarm = None

    if is_alarm_active:
        if cap_alarm is None:
            cap_alarm = cv2.VideoCapture(VIDEO_PATH)
        
        ret_a, frame_a = cap_alarm.read()
        if not ret_a:
            cap_alarm.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_a, frame_a = cap_alarm.read()
        
        cv2.imshow("Doomscroll Blocker", frame_a)
    else:
        if start_time:
            sisa = round(LIMIT_DETIK - (time.time() - start_time), 1)
            cv2.putText(frame, f"Deteksi Melirik: {max(0, sisa)}s", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        
        cv2.imshow("Doomscroll Blocker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stop_sound()
cap_webcam.release()
if cap_alarm: cap_alarm.release()
cv2.destroyAllWindows()