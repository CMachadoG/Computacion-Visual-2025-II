import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- 1️⃣ Cargar imagen ---
img = cv2.imread("19-10-2024_Taller2_cv_3d/assets/Ejercicio2.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# --- 2️⃣ Escala de grises ---
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# --- 3️⃣ Filtros básicos ---
blur = cv2.GaussianBlur(gray, (5, 5), 0)
sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

# --- 4️⃣ Detección de bordes ---
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_combined = cv2.magnitude(sobelx, sobely)
laplacian = cv2.Laplacian(gray, cv2.CV_64F)

# --- 5️⃣ Convertir resultados a rango 0–255 para visualización ---
sobelx = cv2.convertScaleAbs(sobelx)
sobely = cv2.convertScaleAbs(sobely)
sobel_combined = cv2.convertScaleAbs(sobel_combined)
laplacian = cv2.convertScaleAbs(laplacian)

# --- 6️⃣ Mostrar comparaciones ---
titles = [
    "Original",
    "Grises",
    "Blur (Gaussiano)",
    "Sharpen",
    "Sobel X",
    "Sobel Y",
    "Sobel Magnitud",
    "Laplaciano"
]
images = [
    img,
    cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB),
    cv2.cvtColor(blur, cv2.COLOR_GRAY2RGB),
    cv2.cvtColor(sharpen, cv2.COLOR_GRAY2RGB),
    cv2.cvtColor(sobelx, cv2.COLOR_GRAY2RGB),
    cv2.cvtColor(sobely, cv2.COLOR_GRAY2RGB),
    cv2.cvtColor(sobel_combined, cv2.COLOR_GRAY2RGB),
    cv2.cvtColor(laplacian, cv2.COLOR_GRAY2RGB)
]

fig, axs = plt.subplots(2, 4, figsize=(12, 6))
axs = axs.ravel()

for i in range(len(images)):
    axs[i].imshow(images[i])
    axs[i].set_title(titles[i])
    axs[i].axis('off')

plt.tight_layout()
plt.savefig("comparacion_filtros_bordes.png")
plt.close()

# --- 7️⃣ Crear GIF ---
frames = [Image.fromarray(img) for img in images]
frames[0].save(
    "Ejercicio2_comparacion.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1000,  # milisegundos por cuadro
    loop=0
)
    
