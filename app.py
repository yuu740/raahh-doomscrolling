import cv2
import face_recognition
import time
import numpy as np
import pygame
import os


VIDEO_PATH = "raahh_fixed.mp4"
AUDIO_PATH = "raahh_audio.mp3"
SECOND_LIMIT = 1.5
SCALE = 0.25   

pygame.mixer.init()
cap_webcam = cv2.VideoCapture(0)
cap_alarm = cv2.VideoCapture(VIDEO_PATH)
start_time = None
is_alarm_active = False

def play_sync_alarm():
    if os.path.exists(AUDIO_PATH) and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play(-1) 

def stop_sync_alarm():
    pygame.mixer.music.stop()
    cap_alarm.set(cv2.CAP_PROP_POS_FRAMES, 0) 

print("Aplikasi Berjalan... Fokus ke layar!")

while True:
    ret, frame = cap_webcam.read()
    if not ret: break
    
    frame = cv2.addWeighted(frame, 0.8, np.zeros(frame.shape, frame.dtype), 0, 0)

    small_frame = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

    if len(face_locations) == 0:
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
        pos_ms = pygame.mixer.music.get_pos()
        cap_alarm.set(cv2.CAP_PROP_POS_MSEC, pos_ms)
        
        ret_a, frame_a = cap_alarm.read()
        if ret_a:
            h, w, _ = frame.shape
            frame_a = cv2.resize(frame_a, (int(w*0.8), int(h*0.8)))
            ah, aw, _ = frame_alarm = frame_a.shape
            
            y_offset = (h - ah) // 2
            x_offset = (w - aw) // 2
            
            frame[y_offset:y_offset+ah, x_offset:x_offset+aw] = frame_a
            
            cv2.rectangle(frame, (x_offset, y_offset), (x_offset+aw, y_offset+ah), (0, 0, 255), 5)
            cv2.putText(frame, "DOOMSCROLL DETECTED!", (x_offset+20, y_offset-20), 
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

    else:
        status_color = (0, 255, 0) if start_time is None else (0, 165, 255)
        cv2.circle(frame, (30, 30), 10, status_color, -1)
        cv2.putText(frame, "EYE TRACKING ACTIVE", (50, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        if start_time:
            sisa = max(0, round(SECOND_LIMIT - (time.time() - start_time), 1))
            
            bar_w = int((sisa / SECOND_LIMIT) * 200)
            cv2.rectangle(frame, (20, 60), (220, 80), (255, 255, 255), 1)
            cv2.rectangle(frame, (20, 60), (20 + bar_w, 80), (0, 0, 255), -1)

    cv2.imshow("Doomscroll Blocker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stop_sync_alarm()
cap_webcam.release()
cap_alarm.release()
cv2.destroyAllWindows()