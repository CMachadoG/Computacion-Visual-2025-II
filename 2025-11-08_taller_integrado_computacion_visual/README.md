# Taller Integrado – Computación Visual  
## Simulación BCI + Proyecciones 3D

---

# 10. Simulación BCI – EEG Sintético Interactivo
Este ejercicio implementa una simulación de señales EEG sintéticas utilizando bandas Alpha (8–12 Hz) y Beta (15–25 Hz).  
Las señales pasan por filtros Butterworth y se combinan para generar un control visual:

- El tamaño del círculo depende de la energía del EEG.
- El color depende de la intensidad relativa de Alpha, Beta y del suavizado.
- Los sliders permiten modificar Alpha, Beta y el suavizado temporal en tiempo real (PyGame).

### Archivo
``python/10_SimulacionBCI.py``

### Dependencias
- numpy  
- scipy  
- pygame  

### Ejecución
``python python/10_SimulacionBCI.py``

---

# 11. Espacios Proyectivos y Matrices de Proyección  
Este ejercicio implementa:

- Coordenadas homogéneas  
- Matriz de proyección **perspectiva**
- Matriz de proyección **ortográfica**
- Transformación de vista usando *LookAt*
- Visualización de profundidad (NDC)
- Comparación clara entre ambas proyecciones
- Versión interactiva en Three.js

Incluye también una animación .gif generada desde Python.

### Archivos
Python:
- ``python/11_proyecciones/11_proyecciones_demo.py``  
- ``python/11_proyecciones/11_proyecciones_gif.py``  

Three.js:
- ``threejs/11_proyecciones/index.html``

### Dependencias Python
- numpy  
- matplotlib  
- imageio  

### Ejecución
``python python/11_proyecciones/11_proyecciones_demo.py``  
``python python/11_proyecciones/11_proyecciones_gif.py``  

---

# 3. Estructura del Proyecto

proyecto/  
├── gifs/  
│   ├── bci_simulacion.gif  
│   ├── proyecciones.gif  
├── python/  
│   ├── 10_simulacionBCI.py  
│   └── 11_proyecciones/  
│       ├── 11_proyecciones_demo.py  
│       └── 11_proyecciones_gif.py  
└── threejs/  
    └── 11_proyecciones/  
        └── index.html  

---

# 4. Notas finales
Ambas simulaciones están diseñadas para ayudar a comprender:

- Cómo las señales EEG pueden usarse para control visual
- Cómo funcionan las proyecciones 3D usando coordenadas homogéneas
- Cómo comparar ortográfica vs perspectiva
- Cómo construir una vista con LookAt
- Cómo renderizar y visualizar profundidad

