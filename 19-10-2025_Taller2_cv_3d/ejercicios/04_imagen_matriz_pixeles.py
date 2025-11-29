import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- 1️⃣ Cargar imagen ---
img = cv2.imread("19-10-2024_Taller2_cv_3d/assets/Ejercicio4.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV usa BGR, se pasa a RGB

# --- 2️⃣ Separar canales RGB ---
r, g, b = cv2.split(img)
zeros = np.zeros_like(r)
img_r = cv2.merge([r, zeros, zeros])
img_g = cv2.merge([zeros, g, zeros])
img_b = cv2.merge([zeros, zeros, b])

# --- 3️⃣ Modificar región por slicing ---
modificada = img.copy()
h, w, _ = img.shape
modificada[h//4:h//2, w//4:w//2] = [255, 0, 0]  # cuadrado rojo al centro

# --- 4️⃣ Histograma de intensidades (por canal) ---
plt.figure(figsize=(10,4))
plt.title("Histograma por canal")
plt.xlabel("Intensidad")
plt.ylabel("Frecuencia")
plt.hist(r.ravel(), bins=256, color='red', alpha=0.5)
plt.hist(g.ravel(), bins=256, color='green', alpha=0.5)
plt.hist(b.ravel(), bins=256, color='blue', alpha=0.5)
plt.tight_layout()
plt.savefig("histograma_ej4.png")
plt.close()

# --- 5️⃣ Ajuste de brillo y contraste ---
alpha = 1.3  # contraste
beta = 40    # brillo
ajustada = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

# --- 6️⃣ Mostrar resultados ---
cv2.imshow("Original", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
cv2.imshow("Modificada (slicing)", cv2.cvtColor(modificada, cv2.COLOR_RGB2BGR))
cv2.imshow("Brillo/Contraste", cv2.cvtColor(ajustada, cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()

# --- 7️⃣ Guardar comparativa en un GIF ---
frames = [
    Image.fromarray(img),
    Image.fromarray(modificada),
    Image.fromarray(ajustada)
]
frames[0].save(
    "Ejercicio4_comparacion.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1000,
    loop=0
)
