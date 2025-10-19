import cv2
import numpy as np
import imageio
import matplotlib.pyplot as plt

# --- 1. Cargar imagen ---
img = cv2.imread('19-10-2024_Taller2_cv_3d/assets/Ejercicio3.png')
original = img.copy()

# --- 2. Convertir a escala de grises ---
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# --- 3. Umbralización (binarización) ---
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# --- 4. Detección de contornos ---
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# --- 5. Dibujar contornos, centroides y áreas ---
contoured = img.copy()
for c in contours:
    M = cv2.moments(c)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        area = cv2.contourArea(c)
        cv2.drawContours(contoured, [c], -1, (0, 255, 0), 2)
        cv2.circle(contoured, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(contoured, f"A={area:.0f}", (cx + 10, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# --- 6. Crear lista de pasos para el GIF ---
frames = []
steps = [
    ("Original", original),
    ("Grises", cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)),
    ("Binaria", cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)),
    ("Contornos", contoured)
]

for title, frame in steps:
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # agregar texto de título
    cv2.putText(frame_rgb, title, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    frames.append(frame_rgb)

# --- 7. Guardar GIF ---
imageio.mimsave("Ejercicio3_segmentacion.gif", frames, duration=1.0)

# --- 8. Mostrar última imagen en ventana ---
cv2.imshow("Contornos", contoured)
cv2.waitKey(0)
cv2.destroyAllWindows()
