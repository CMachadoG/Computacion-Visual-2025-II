import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- 1️⃣ Cargar imagen ---
img = cv2.imread("19-10-2024_Taller2_cv_3d/assets/Ejercicio10.jpeg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# --- 2️⃣ Convertir a otros modelos de color ---
img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
img_lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# --- 3️⃣ Simulación: visión daltónica (deuteranopia aproximada) ---
# Matriz de simulación aproximada (fuente: Machado et al.)
matrix_deuter = np.array([
    [0.367, 0.861, -0.228],
    [0.280, 0.673,  0.047],
    [-0.012, 0.043, 0.969]
])

sim_daltonico = img.reshape(-1, 3).dot(matrix_deuter.T)
sim_daltonico = np.clip(sim_daltonico, 0, 255).reshape(img.shape).astype(np.uint8)

# --- 4️⃣ Mostrar comparaciones ---
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
axs = axs.ravel()

axs[0].imshow(img)
axs[0].set_title("Original (RGB)")

axs[1].imshow(cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB))
axs[1].set_title("Modelo HSV")

axs[2].imshow(cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB))
axs[2].set_title("Modelo LAB")

axs[3].imshow(img_gray, cmap='gray')
axs[3].set_title("Escala de grises")

axs[4].imshow(sim_daltonico)
axs[4].set_title("Simulación Daltónica")

axs[5].axis("off")

for ax in axs:
    ax.axis("off")

plt.tight_layout()
plt.savefig("comparacion_modelos_color.png")
plt.close()

# --- 5️⃣ Guardar GIF comparativo ---
frames = [
    Image.fromarray(img),
    Image.fromarray(cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)),
    Image.fromarray(cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB)),
    Image.fromarray(img_gray),
    Image.fromarray(sim_daltonico)
]
frames[0].save(
    "Ejercicio10_comparacion.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1200,
    loop=0
)

