import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
from io import BytesIO

# Coordenadas del triángulo original en 2D
triangle = np.array([
    [0, 1, 0.5],  # Coordenadas X
    [0, 0, 1]     # Coordenadas Y
])

# Función de traslación usando matriz homogénea 3x3
def translate(points, tx, ty):
    T = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return T @ points

# Función de rotación alrededor del origen
def rotate(points, angle_rad):
    R = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad),  np.cos(angle_rad), 0],
        [0, 0, 1]
    ])
    return R @ points

# Función de escala
def scale(points, sx, sy):
    S = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])
    return S @ points

# Convertir el triángulo a coordenadas homogéneas (3 filas)
triangle_homogeneous = np.vstack((triangle, np.ones((1, triangle.shape[1]))))

frames = 60  # Número de fotogramas para la animación
output_gif = "transformacion.gif"
images = []

for t in range(frames):
    # Parámetros variables en el tiempo para la animación
    angle = 2 * np.pi * t / frames                    # Rotación continua
    tx = np.sin(angle) * 2                            # Traslación oscilante en X
    ty = np.cos(angle) * 2                            # Traslación oscilante en Y
    sx = 1 + 0.5 * np.sin(angle)                      # Escala cíclica en X
    sy = 1 + 0.5 * np.cos(angle)                      # Escala cíclica en Y

    # Aplicar transformaciones con matrices (en orden: traslación → rotación → escala)
    transformed = translate(triangle_homogeneous, tx, ty)
    transformed = rotate(transformed, angle)
    transformed = scale(transformed, sx, sy)

    # Visualización del triángulo original y transformado
    fig, ax = plt.subplots()
    ax.plot(*triangle[:2], 'bo-', label='Original')           # Triángulo azul (original)
    ax.plot(transformed[0, :], transformed[1, :], 'ro-', label='Transformado')  # Rojo: transformado
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_title(f"Frame {t}")
    ax.legend()
    ax.set_aspect('equal')

    # Guardar imagen temporal en memoria (no en disco)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = iio.imread(buf)
    images.append(image)

    # Mostrar matrices de transformación individuales por consola (requisito opcional)
    print(f"Frame {t}")
    print("Translación:\n", translate(np.eye(3), tx, ty))
    print("Rotación:\n", rotate(np.eye(3), angle))
    print("Escala:\n", scale(np.eye(3), sx, sy))
    print("\n\n\t\t\t\t\t\t\t\t\t\t")

# Crear el GIF animado a partir de los frames generados en memoria
iio.imwrite(output_gif, images, duration=1/15)
