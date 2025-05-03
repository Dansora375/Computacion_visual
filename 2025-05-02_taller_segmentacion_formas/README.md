## 🧪 Segmentando el Mundo: Binarización y Reconocimiento de Formas
**📅 Fecha**

2025-05-02

**🎯 Objetivo del Taller**

Aplicar técnicas básicas de segmentación en imágenes mediante umbralización y detección de formas simples. El objetivo es comprender cómo identificar regiones de interés mediante procesos de binarización, análisis de contornos y extracción de características geométricas.

**🧠 Conceptos Aprendidos**

* ✅ Carga y visualización de imágenes en escala de grises con OpenCV.
* ✅ Aplicación de binarización por umbral fijo y umbral adaptativo.
* ✅ Detección de contornos con `cv2.findContours()` y representación gráfica.
* ✅ Cálculo del centro de masa mediante momentos (`cv2.moments()`).
* ✅ Dibujo de bounding boxes para formas detectadas.
* ✅ Obtención de métricas básicas como cantidad de formas, área y perímetro promedio.
* Bonus: Espacio para integración con webcam o secuencias de imágenes (en tiempo real).

**🔧 Herramientas y Entornos**

* Python (Jupyter Notebook o Google Colab)
* OpenCV (`opencv-python-headless`)
* NumPy
* Matplotlib

**📁 Estructura del Proyecto**

2025-05-02_taller_segmentacion_formas/<br>
├── datos/<br>
│   └── mano.jpg<br>
├── entorno/<br>
│   └── python.ipynb<br>
├── resultados/<br>
│   ├── centro_masa.png<br>
│   ├── contornos.png<br>
│   └── umbrales.png<br>
└── README.md

**🧪 Implementación**

🔹 Etapas realizadas

1.  Carga de la imagen en escala de grises.
2.  Aplicación de segmentación binaria (fijo y adaptativo).
3.  Extracción de contornos y dibujo sobre la imagen original.
4.  Cálculo del centro de masa y rectángulos envolventes.
5.  Obtención de estadísticas geométricas: número, área y perímetro promedio.

---

**💻 Código Relevante**

Aquí se presentan fragmentos clave del código Python utilizado en el taller para cada etapa del proceso de segmentación y análisis.



```python
# 1. Cargar imagen en escala de grises
img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

# 2. Umbral fijo
_, binary_fixed = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# 3. Umbral adaptativo
binary_adapt = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, blockSize=11, C=2
)

# 4. Detección de contornos
contours, _ = cv2.findContours(binary_fixed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contours = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

# 5. Centro de masa y bounding box
img_shapes = img_contours.copy()
areas, perimeters = [], []

for c in contours:
    # Centro de masa
    M = cv2.moments(c)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.circle(img_shapes, (cx, cy), 4, (0, 0, 255), -1)

    # Bounding box
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(img_shapes, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Métricas
    areas.append(cv2.contourArea(c))
    perimeters.append(cv2.arcLength(c, True))

# 6. Métricas generales
num_formas = len(contours)
area_prom = sum(areas) / num_formas if num_formas else 0
perim_prom = sum(perimeters) / num_formas if num_formas else 0

print("Número de formas:", num_formas)
print("Área promedio:", area_prom)
print("Perímetro promedio:", perim_prom)
```


**🖼️ Resultados**

Imagen original:

![Imagen origina](datos/mano.jpg)

Binarización por umbral fijo y adaptativo:

![Imagen origina](resultados/umbrales.png)

Contornos detectados:

![Imagen origina](resultados/contornos.png)

Centro de masa + Bounding boxes:

![Imagen origina](resultados/centro_masa.png)

**🧩 Prompts Usados**

* “Aplica segmentación de imágenes con OpenCV usando umbral fijo y adaptativo, encuentra contornos, calcula centros de masa y bounding boxes, y muestra métricas básicas como área y perímetro promedio.”
* “Prepara notebook en Colab con espacio para cargar la imagen desde ruta personalizada.”

**💬 Reflexión Final**

Este taller fue clave para entender cómo identificar regiones significativas en una imagen usando técnicas simples pero poderosas de visión por computador.

La binarización nos permitió destacar formas, y gracias a `cv2.findContours()` fue posible extraerlas y analizarlas geométricamente.

El uso de momentos para encontrar el centro de masa resultó muy útil, al igual que visualizar bounding boxes para tener una idea clara de la dimensión de cada forma.

Una dificultad inicial fue elegir un buen umbral y ajustar parámetros para obtener una segmentación efectiva, especialmente en imágenes con ruido o iluminación no uniforme.