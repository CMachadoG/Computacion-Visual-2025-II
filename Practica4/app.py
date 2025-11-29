import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import numpy as np
# 💡 SOLUCIÓN FINAL: Importar el tipo de dato Protobuf necesario para el dibujo
from mediapipe.framework.formats import landmark_pb2 

# --- 1. CONFIGURACIÓN DE MEDIAPIPE ---
MODEL_PATH = 'hand_landmarker.task' 
THUMB_TIP = 4
INDEX_FINGER_TIP = 8
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),        # Índice
    (5, 9), (9, 10), (10, 11), (11, 12),   # Medio
    (9, 13), (13, 14), (14, 15), (15, 16), # Anular
    (13, 17), (17, 18), (18, 19), (19, 20),# Meñique
    (0, 17) # Base de la palma
]

hand_results_global = None 
capture_flag = False 

def calculate_distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def process_results(result, output_image, timestamp_ms):
    global hand_results_global
    hand_results_global = result

options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.LIVE_STREAM,
    num_hands=1,
    result_callback=process_results)

# --- 2. LÓGICA DE INTERACCIÓN Y CÁLCULO DE FPS ---

def main():
    global hand_results_global, capture_flag
    
    with vision.HandLandmarker.create_from_options(options) as landmarker:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return

        prev_time = time.time()
        frame_count = 0
        fps = 0.0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            # 1. Detección (Asíncrona)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb) 
            timestamp = int(time.time() * 1000)
            landmarker.detect_async(mp_image, timestamp)
            
            # 2. Lógica de Interacción (Síncrona)
            interaction_text = "Estado: Normal"
            
            # BLOQUE PRINCIPAL DE DETECCIÓN DE MANOS
            if hand_results_global and hand_results_global.hand_landmarks:
                
                landmarks = hand_results_global.hand_landmarks[0]
                
                # --- REGLA 1: GESTO "PINCH" (Pausa) ---
                p1 = landmarks[THUMB_TIP]
                p2 = landmarks[INDEX_FINGER_TIP]
                distance = calculate_distance(p1, p2)
                PINCH_THRESHOLD = 0.05 
                
                if distance < PINCH_THRESHOLD:
                    interaction_text = "PAUSA ACTIVADA (PINCH) ⏸️"
                
                # --- REGLA 2: GESTO "MANO ABIERTA" (Captura) ---
                fingers_up = 0
                finger_tips = [8, 12, 16, 20]
                finger_bases = [5, 9, 13, 17]
                
                for tip_idx, base_idx in zip(finger_tips, finger_bases):
                    if landmarks[tip_idx].y < landmarks[base_idx].y:
                        fingers_up += 1

                if fingers_up == 4 and distance >= PINCH_THRESHOLD:
                    interaction_text = "MANO ABIERTA (Captura) 📸"
                    if not capture_flag:
                        filename = f"captura_{int(time.time())}.png"
                        cv2.imwrite(filename, frame)
                        print(f"-> Captura guardada como: {filename}")
                        capture_flag = True
                else:
                    capture_flag = False 
                
                # 🛠️ CONVERSIÓN DE FORMATO PARA EL DIBUJO
                H, W, _ = frame.shape
                
                # 1. Dibujar las Conexiones
                for connection in HAND_CONNECTIONS:
                    p1_idx, p2_idx = connection
                    p1 = landmarks[p1_idx]
                    p2 = landmarks[p2_idx]
                    
                    # Convertir coordenadas normalizadas (0-1) a coordenadas de píxel
                    x1, y1 = int(p1.x * W), int(p1.y * H)
                    x2, y2 = int(p2.x * W), int(p2.y * H)
                    
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2) # Línea magenta

                # 2. Dibujar los Landmarks (puntos)
                for landmark in landmarks:
                    x, y = int(landmark.x * W), int(landmark.y * H)
                    cv2.circle(frame, (x, y), 5, (0, 255, 255), -1)
            
            # 3. Cálculo de FPS y Estabilidad
            current_time = time.time()
            frame_count += 1
            if current_time - prev_time >= 1: 
                fps = frame_count / (current_time - prev_time)
                prev_time = current_time
                frame_count = 0
                print(f"FPS Actual: {fps:.2f}")

            # Mostrar texto y FPS en el frame
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, interaction_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('MediaPipe Gestures', frame)

            if cv2.waitKey(5) & 0xFF == 27: 
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()