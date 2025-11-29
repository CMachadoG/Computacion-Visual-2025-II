import pygame
import numpy as np
from scipy.signal import butter, filtfilt

# --- Inicialización ---
pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación BCI (EEG Sintético Interactivo)")

font = pygame.font.SysFont("consolas", 20)
clock = pygame.time.Clock()

# --- Configuración EEG sintético ---
fs = 60
t = np.linspace(0, 1, fs)
alpha_base = np.sin(2 * np.pi * 10 * t)
beta_base = np.sin(2 * np.pi * 20 * t)

# --- Filtros ---
def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low, high = lowcut / nyq, highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

b_alpha, a_alpha = butter_bandpass(8, 12, fs)
b_beta, a_beta = butter_bandpass(15, 25, fs)

# --- Sliders ---
slider_alpha = 0.5
slider_beta = 0.5
slider_smooth = 0.3

def draw_slider(x, y, value, label):
    pygame.draw.rect(screen, (80, 80, 80), (x, y, 200, 10))
    pygame.draw.circle(screen, (255, 255, 255), (x + int(200 * value), y + 5), 8)
    text = font.render(f"{label}: {value:.2f}", True, (255, 255, 255))
    screen.blit(text, (x, y - 25))

# --- Variables dinámicas ---
prev_signal = 0
wave_buffer = np.full(WIDTH, HEIGHT - 40)

# --- Loop principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Control de sliders
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if 100 <= mx <= 300:
                if 480 <= my <= 490: slider_alpha = (mx - 100) / 200
                if 530 <= my <= 540: slider_beta = (mx - 100) / 200
                if 580 <= my <= 590: slider_smooth = (mx - 100) / 200

    # --- Generar EEG sintético ---
    noise = np.random.normal(0, 0.3, fs)
    signal = slider_alpha * alpha_base + slider_beta * beta_base + noise

    filtered_alpha = filtfilt(b_alpha, a_alpha, signal)
    filtered_beta = filtfilt(b_beta, a_beta, signal)

    combined_signal = 0.6 * filtered_alpha + 0.4 * filtered_beta
    instant_power = np.mean(combined_signal ** 2)

    # --- Suavizado temporal ---
    prev_signal = (1 - slider_smooth) * prev_signal + slider_smooth * np.mean(combined_signal)
    normalized_signal = np.clip((prev_signal + 1) / 2, 0, 1)

    # --- Control visual (tamaño y color) ---
    power_scale = np.interp(instant_power, [0.01, 0.5], [0.5, 2.0])
    circle_radius = int(80 * power_scale)
    circle_radius = max(60, min(250, circle_radius))

    # Utilidad para asegurar que el color sea válido
    def clamp(x, min_val=0, max_val=255):
        return max(min_val, min(int(x), max_val))

    # Color basado en sliders
    r = clamp(slider_alpha * 255)
    g = clamp(slider_beta * 255)
    b = clamp(slider_smooth * 255)

    color_mix = (r, g, b)

    # --- Dibujar escena ---
    screen.fill((10, 10, 25))

    # Círculo principal
    pygame.draw.circle(screen, color_mix, (WIDTH // 2, HEIGHT // 2 - 120), circle_radius)

    # --- Actualizar onda EEG ---
    base_line = HEIGHT - 50
    wave_y = int(base_line - prev_signal * 120)
    wave_buffer = np.roll(wave_buffer, -1)
    wave_buffer[-1] = wave_y

    # Onda EEG visible
    for x in range(WIDTH - 1):
        pygame.draw.line(screen, (0, 200, 255),
                         (x, wave_buffer[x]),
                         (x + 1, wave_buffer[x + 1]), 2)

    pygame.draw.line(screen, (60, 60, 60), (0, base_line), (WIDTH, base_line), 2)

    # --- Sliders ---
    draw_slider(100, 480, slider_alpha, "Alpha (8–12Hz)")
    draw_slider(100, 530, slider_beta, "Beta (15–25Hz)")
    draw_slider(100, 580, slider_smooth, "Suavizado")

    # Texto informativo
    screen.blit(font.render("Control BCI: Relajación ↔ Concentración", True, (200, 200, 200)), (100, 430))
    screen.blit(font.render("Visual EEG con tamaño y color dinámicos", True, (200, 200, 200)), (100, 620))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
