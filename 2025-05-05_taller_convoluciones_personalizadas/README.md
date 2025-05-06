# 🧪 Convoluciones Manuales vs OpenCV

📅 Fecha  
2025-05-05 – Fecha  

---

🎯 Objetivo del Taller  
Implementar manualmente el proceso de convolución 2D sobre una imagen en escala de grises, usando matrices (kernels) personalizadas en NumPy, y comparar los resultados visuales con los obtenidos a través de funciones de OpenCV. Se busca entender a profundidad cómo se modifica la información de una imagen mediante operaciones matriciales básicas.

---

🧠 Conceptos Aprendidos

- ✅ Convolución 2D manual con NumPy
- ✅ Aplicación de kernels para suavizado, enfoque y detección de bordes
- ✅ Comparación entre implementación propia y `cv2.filter2D()`
- Bonus: Interactividad con `cv2.createTrackbar` para modificar filtros en tiempo real

---

🔧 Herramientas y Entornos

- Python (opencv-python, numpy, matplotlib)
- VSCode con extensión Jupyter
- Requiere entorno local con GUI para ejecutar `cv2.namedWindow` (bonus)

---

📁 Estructura del Proyecto

2025-05-05_taller_convoluciones_manual/<br>
├── datos/ # Imagen base<br>
│   └── flor.jpg<br>
├── entorno/ <br>
│   └── python.ipynb<br>
├── resultados/<br>
│   └── resultados_convolucion.gif<br>
├── README.md  

---

🧪 Implementación

🔹 Etapas realizadas

1. Carga de la imagen en escala de grises desde carpeta `datos/`.
2. Implementación manual de una función `convolve2d_manual()` que aplica un kernel 2D sobre la imagen usando NumPy.
3. Diseño y prueba de tres kernels:
   - Enfocar (sharpen)
   - Suavizado (blur)
   - Detección de esquinas (Sobel combinado)
4. Comparación de los resultados visuales con `cv2.filter2D()` para cada kernel.
5. BONUS: Se creó una interfaz interactiva con sliders (`cv2.createTrackbar`) para modificar los valores del kernel de enfoque en tiempo real. (Requiere entorno con GUI)

🔹 Código relevante

**Convolución 2D manual con padding:**
```python
def convolve2d_manual(img, kernel):
    h, w = img.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    output = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            output[i, j] = np.clip(np.sum(region * kernel), 0, 255)
    
    return output.astype(np.uint8)

```

**Comparación con OpenCV:**
```python

sharpen_kernel = np.array([[0, -1,  0],
                           [-1, 5, -1],
                           [0, -1,  0]])
sharpened_manual = convolve2d_manual(img, sharpen_kernel)
sharpened_cv = cv2.filter2D(img, -1, sharpen_kernel)
```

**Interfaz interactiva con cv2.createTrackbar (bonus):**

```python
def nothing(x): pass
cv2.namedWindow('Sharpen Interactivo')
cv2.createTrackbar('Centro', 'Sharpen Interactivo', 5, 10, nothing)
cv2.createTrackbar('Bordes', 'Sharpen Interactivo', 1, 10, nothing)

```

📊 Resultados Visuales

✅ Este taller incluye una visualización comparativa entre resultados manuales y de OpenCV:

Comparación de resultados

![Comparación de resultados](resultados/Convoluciones%20Personalizadas.gif)

🧩 Prompts Usados

"Implementa una función manual de convolución 2D con NumPy que aplique un kernel sobre una imagen en escala de grises."

"Crea y aplica kernels para enfoque, suavizado y detección de bordes. Compara los resultados con cv2.filter2D."

"Haz una interfaz interactiva con sliders para ajustar un kernel de enfoque en tiempo real con OpenCV."

💬 Reflexión Final

Este taller fue clave para entender la lógica detrás del procesamiento de imágenes en bajo nivel, especialmente cómo los kernels afectan directamente a los píxeles vecinos mediante sumas ponderadas. Implementar manualmente la convolución 2D permite visualizar mejor los efectos que tiene cada coeficiente del kernel sobre la imagen resultante.

Comparar los resultados con OpenCV mostró la eficiencia y precisión de las funciones optimizadas, pero también reforzó el valor de conocer su funcionamiento interno. La parte más desafiante fue la interfaz interactiva, que solo puede ejecutarse en un entorno con GUI. A futuro, me interesaría adaptar esta lógica a filtros dinámicos aplicados en tiempo real con cámara o video.
