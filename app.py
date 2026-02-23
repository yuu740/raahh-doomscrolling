import gradio as gr
import cv2
import face_recognition
import time
import numpy as np
import pygame 

pygame.mixer.init()
def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("raahh_audio.mp3") 
        pygame.mixer.music.play()

def stop_alarm():
    pygame.mixer.music.stop()

start_time = None
limit = 3
alarm_cap = None
video_path = "raahh_fixed.mp4"
frame_count = 0

def detect_doomscroll(image):
    global start_time, alarm_cap, frame_count
    
    if image is None: return None
    image = image.copy()
    frame_count += 1

    if frame_count % 5 == 0:
        small_frame = cv2.resize(image, (0, 0), fx=0.1, fy=0.1)
        
        face_found = len(face_recognition.face_locations(small_frame)) > 0

        if face_found:
            if start_time is None:
                start_time = time.time()
        else:
            start_time = None
            stop_alarm()
            if alarm_cap is not None:
                alarm_cap.release()
                alarm_cap = None

    if start_time:
        elapsed = time.time() - start_time
        if elapsed > limit:
            play_alarm() 
            
            if alarm_cap is None:
                alarm_cap = cv2.VideoCapture(video_path)
            
            ret, frame_alarm = alarm_cap.read()
            if not ret:
                alarm_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame_alarm = alarm_cap.read()
            
            if ret:
                frame_alarm = cv2.resize(frame_alarm, (image.shape[1], image.shape[0]))
                return cv2.cvtColor(frame_alarm, cv2.COLOR_BGR2RGB)
        else:
            cv2.putText(image, f"Fokus! Alarm dlm: {round(limit-elapsed, 1)}s", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    return image

with gr.Blocks(title="Anti-Doomscroll AI") as demo:
    gr.Markdown("# Doomscroll Blocker")
    with gr.Row():
        webcam_input = gr.Image(sources=["webcam"], streaming=True, label="Webcam")
        output_screen = gr.Image(label="Monitoring Screen")

    webcam_input.stream(fn=detect_doomscroll, inputs=webcam_input, outputs=output_screen)

if __name__ == "__main__":
    demo.launch()