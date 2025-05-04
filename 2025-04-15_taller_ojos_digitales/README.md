# 🧪 Taller - Ojos Digitales: Introducción a la Visión Artificial

📅 Fecha  
[Fecha del Taller, ej: 2025-04-15] – Fecha de realización

---

🎯 Objetivo del Taller  
Entender los fundamentos de la percepción visual artificial mediante el procesamiento básico de imágenes. Se exploran conceptos como imágenes en escala de grises, aplicación de filtros convolucionales y detección de bordes utilizando la biblioteca OpenCV en Python.

---

🧠 Conceptos Aprendidos

✅ Carga y manipulación de imágenes digitales.
✅ Conversión de imágenes a diferentes espacios de color (Color a Grises).
✅ Aplicación de filtros convolucionales (suavizado, enfoque) mediante kernels.
✅ Detección de bordes utilizando operadores basados en gradientes (Sobel) y segundas derivadas (Laplaciano).
✅ Visualización de resultados intermedios del procesamiento de imágenes.

---

🔧 Herramientas y Entornos

- Python
- `opencv-python`
- `numpy`
- `matplotlib` (opcional para visualización alternativa)

---

📁 Estructura del Proyecto

[Nombre de tu carpeta principal, ej: 2025-04-15_taller_ojos_digitales]/<br>
├── datos/<br>
│   └── flor.jpg  <br>
├── entorno/python/<br>
│   └── ojos_digitales.py  <br>
├── resultados/<br>
│   └── imagenes_vision_arwtificial.gif  <br>
└── README.md

---

🧪 Implementación

🔹 Etapas realizadas

1. Carga de una imagen a color desde un archivo.
2. Conversión de la imagen cargada a escala de grises.
3. Aplicación de un filtro de suavizado (Blur) y un filtro de enfoque (Sharpening).
4. Implementación de la detección de bordes utilizando los filtros de Sobel (horizontal, vertical y combinado) y el filtro Laplaciano.
5. Visualización de la imagen original y los resultados de cada paso de procesamiento (escala de grises, filtros, detección de bordes).

---

### 🖼️ Procesamiento Básico de Imágenes

**Descripción:**  
El script carga una imagen a color, la convierte a escala de grises y aplica filtros comunes como el suavizado Gaussiano y un filtro de enfoque personalizado. Estos pasos iniciales son fundamentales para preparar la imagen para análisis posteriores.

**Código relevante:**


```python
# Cargar imagen y convertir a gris
img_color = cv2.imread(image_path)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Aplicar Sharpening
kernel_sharpening = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
img_sharpened = cv2.filter2D(img_gray, -1, kernel_sharpening)
# Detección de bordes con Sobel
sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=5)
abs_sobelx = cv2.convertScaleAbs(sobelx)
sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=5)
abs_sobely = cv2.convertScaleAbs(sobely)
sobel_combined = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)

# Detección de bordes con Laplaciano
laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
abs_laplacian = cv2.convertScaleAbs(laplacian)
```
---


**GIF del visor interactivo:**  
![Visualización pyhon results](resultados/imagenes_vision_artificial.gif)

🧩 Prompts Usados

"Carga una imagen a color en Python usando OpenCV y conviértela a escala de grises."
"Aplica un filtro de suavizado (blur) y un filtro de enfoque (sharpening) a una imagen en escala de grises con OpenCV."
"Implementa la detección de bordes en una imagen usando los filtros de Sobel y Laplaciano con OpenCV en Python. Muestra los resultados de Sobel X, Sobel Y, Sobel combinado y Laplaciano."
"Muestra las imágenes resultantes de los filtros y la detección de bordes usando cv2.imshow."

---

💬 Reflexión Final

Este taller proporcionó una base sólida para entender cómo los computadores "ven" y procesan imágenes. Trabajar con escala de grises y kernels para filtros hizo muy tangible el concepto de convolución. La comparación entre los diferentes métodos de detección de bordes (Sobel vs. Laplaciano) ayudó a comprender sus sensibilidades a diferentes tipos de cambios de intensidad.

Una dificultad inicial fue entender la importancia de los tipos de datos de salida de funciones como cv2.Sobel y cv2.Laplacian (que a menudo requieren cv2.CV_64F) y la necesidad de convertir los resultados (cv2.convertScaleAbs) para poder visualizarlos correctamente como imágenes de 8 bits. La manipulación de kernels con NumPy también fue un buen repaso del álgebra matricial aplicada al procesamiento de imágenes. Este es un excelente primer paso hacia tareas más complejas como la segmentación y el reconocimiento de objetos.