import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# ---------------------------------------
# 1. FUNCIONES DE MATRICES DE PROYECCIÓN
# ---------------------------------------

def perspective_fov(fov_y, aspect, near, far):
    f = 1 / np.tan(fov_y / 2)
    M = np.zeros((4,4))
    M[0,0] = f / aspect
    M[1,1] = f
    M[2,2] = (far + near) / (near - far)
    M[2,3] = (2 * far * near) / (near - far)
    M[3,2] = -1
    return M

def orthographic(left, right, bottom, top, near, far):
    M = np.zeros((4,4))
    M[0,0] = 2/(right-left)
    M[1,1] = 2/(top-bottom)
    M[2,2] = -2/(far-near)
    M[0,3] = -(right+left)/(right-left)
    M[1,3] = -(top+bottom)/(top-bottom)
    M[2,3] = -(far+near)/(far-near)
    M[3,3] = 1
    return M

def look_at(eye, center, up):
    f = center - eye
    f = f / np.linalg.norm(f)
    u = up / np.linalg.norm(up)
    s = np.cross(f, u)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)
    M = np.eye(4)
    M[0,0:3] = s
    M[1,0:3] = u
    M[2,0:3] = -f
    T = np.eye(4)
    T[0:3,3] = -eye
    return M @ T

def project_points(P, view, pts):
    cam = view @ pts
    clip = P @ cam
    w = np.where(np.abs(clip[3]) < 1e-6, 1e-6, clip[3])
    ndc = clip[:3] / w
    xy = ndc[:2].T
    z = ndc[2]
    return xy, z

# ---------------------------------------
# 2. ESCENA DE PUNTOS
# ---------------------------------------

np.random.seed(1)

# grid 3D
xs = np.linspace(-1.5, 1.5, 6)
ys = np.linspace(-1.0, 1.0, 4)
zs = np.linspace(1.0, 6.0, 6)
grid = np.array(np.meshgrid(xs,ys,zs)).reshape(3,-1)

# puntos aleatorios con rangos correctos
low  = np.array([-2, -1, 1]).reshape(3,1)
high = np.array([ 2,  1, 6]).reshape(3,1)
rand = low + (high - low) * np.random.rand(3, 200)

points = np.hstack([grid, rand])
points_h = np.vstack([points, np.ones((1,points.shape[1]))])

# ---------------------------------------
# 3. CÁMARA Y PROYECCIONES
# ---------------------------------------

eye = np.array([0,1,-1])
center = np.array([0,0,2.5])
up = np.array([0,1,0])
base_view = look_at(eye, center, up)

fov = np.deg2rad(60)
aspect = 1
near, far = 0.1, 20

P_p = perspective_fov(fov, aspect, near, far)
P_o = orthographic(-2,2,-2,2,near,far)

# ---------------------------------------
# 4. GENERAR FRAMES Y GUARDAR GIF
# ---------------------------------------

frames = []
os.makedirs("frames", exist_ok=True)

for i in range(40):
    angle = i * 0.12
    rotY = np.array([
        [ np.cos(angle), 0, np.sin(angle), 0],
        [ 0,             1, 0,             0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [ 0,             0, 0,             1]
    ])

    view = base_view @ rotY

    xy_p, z_p = project_points(P_p, view, points_h)
    xy_o, z_o = project_points(P_o, view, points_h)

    fig, ax = plt.subplots(1,2, figsize=(8,4))

    sc1 = ax[0].scatter(xy_p[:,0], xy_p[:,1], c=z_p, cmap='viridis', s=14)
    ax[0].set_title("Perspectiva")
    ax[0].set_xlim(-1,1); ax[0].set_ylim(-1,1); ax[0].set_aspect("equal")

    sc2 = ax[1].scatter(xy_o[:,0], xy_o[:,1], c=z_o, cmap='plasma', s=14)
    ax[1].set_title("Ortográfica")
    ax[1].set_xlim(-1,1); ax[1].set_ylim(-1,1); ax[1].set_aspect("equal")

    plt.tight_layout()
    fname = f"frames/frame_{i}.png"
    fig.savefig(fname)
    plt.close(fig)

    frames.append(imageio.imread(fname))

imageio.mimsave("proyecciones.gif", frames, duration=0.1)

print("✅ GIF generado correctamente como: proyecciones.gif")
