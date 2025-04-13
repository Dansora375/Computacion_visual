import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
from io import BytesIO

# Original triangle coordinates in 2D
triangle = np.array([
    [0, 1, 0.5],  # X coordinates
    [0, 0, 1]     # Y coordinates
])

# Translation function using a 3x3 homogeneous transformation matrix
def translate(points, tx, ty):
    T = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return T @ points

# Rotation function around the origin
def rotate(points, angle_rad):
    R = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad),  np.cos(angle_rad), 0],
        [0, 0, 1]
    ])
    return R @ points

# Scaling function
def scale(points, sx, sy):
    S = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])
    return S @ points

# Convert triangle to homogeneous coordinates (3 rows)
triangle_homogeneous = np.vstack((triangle, np.ones((1, triangle.shape[1]))))

frames = 60  # Number of frames for the animation
output_gif = "transformacion.gif"
images = []

for t in range(frames):
    # Time-dependent parameters for animation
    angle = 2 * np.pi * t / frames               # Continuous rotation
    tx = np.sin(angle) * 2                       # Oscillating translation in X
    ty = np.cos(angle) * 2                       # Oscillating translation in Y
    sx = 1 + 0.5 * np.sin(angle)                 # Cyclic scale in X
    sy = 1 + 0.5 * np.cos(angle)                 # Cyclic scale in Y

    # Apply transformations in order: translation → rotation → scale
    transformed = translate(triangle_homogeneous, tx, ty)
    transformed = rotate(transformed, angle)
    transformed = scale(transformed, sx, sy)

    # Plot original and transformed triangle
    fig, ax = plt.subplots()
    ax.plot(*triangle[:2], 'bo-', label='Original')             # Blue: original triangle
    ax.plot(transformed[0, :], transformed[1, :], 'ro-', label='Transformed')  # Red: transformed triangle
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_title(f"Frame {t}")
    ax.legend()
    ax.set_aspect('equal')

    # Save image in memory (not to disk)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = iio.imread(buf)
    images.append(image)

    # Print individual transformation matrices to console (optional requirement)
    print(f"Frame {t}")
    print("Translation:\n", translate(np.eye(3), tx, ty))
    print("Rotation:\n", rotate(np.eye(3), angle))
    print("Scale:\n", scale(np.eye(3), sx, sy))
    print("\n\n\t\t\t\t\t\t\t\t\t\t")

# Export animated GIF from in-memory frames
iio.imwrite(output_gif, images, duration=1/15)
