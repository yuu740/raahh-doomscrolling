import gradio as gr
import cv2
import face_recognition
import time
import numpy as np


start_time = None
limit = 10  # Detik

def detect_doomscroll(image):
    global start_time
    
    if image is None:
        return None

    small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    
    face_locations = face_recognition.face_locations(small_frame)

    if len(face_locations) > 0:
        if start_time is None:
            start_time = time.time()
        
        elapsed = time.time() - start_time
        
        if elapsed > limit:
            overlay = image.copy()
            cv2.rectangle(overlay, (0,0), (image.shape[1], image.shape[0]), (0,0,255), -1)
            image = cv2.addWeighted(overlay, 0.5, image, 0.5, 0)
            
            cv2.putText(image, "STOP DOOMSCROLLING!", (50, image.shape[0]//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 4)
        else:
            countdown = int(limit - elapsed)
            cv2.putText(image, f"Sisa waktu: {countdown}s", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        start_time = None
        
    return image

demo = gr.Interface(
    fn=detect_doomscroll,
    inputs=gr.Image(sources=["webcam"], streaming=True),
    outputs="image",
    live=True,
    title="Doomscroll Blocker (Dlib Version)",
    description="Dekatkan wajah ke kamera. Jika lebih dari 10 detik, alarm merah akan muncul."
)

if __name__ == "__main__":
    demo.launch()