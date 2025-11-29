import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# MATRICES DE PROYECCIÓN
# -------------------------------

def perspective_fov(fov_y, aspect, near, far):
    f = 1.0 / np.tan(fov_y / 2)
    M = np.zeros((4,4))
    M[0,0] = f / aspect
    M[1,1] = f
    M[2,2] = (far + near) / (near - far)
    M[2,3] = (2 * far * near) / (near - far)
    M[3,2] = -1.0
    return M

def orthographic(left, right, bottom, top, near, far):
    M = np.zeros((4,4))
    M[0,0] = 2.0 / (right - left)
    M[1,1] = 2.0 / (top - bottom)
    M[2,2] = -2.0 / (far - near)
    M[0,3] = -(right + left) / (right - left)
    M[1,3] = -(top + bottom) / (top - bottom)
    M[2,3] = -(far + near) / (far - near)
    M[3,3] = 1.0
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
    w = clip[3].copy()
    w[np.abs(w) < 1e-8] = 1e-8
    ndc = clip[:3] / w
    xy = ndc[:2].T
    z = ndc[2]
    return xy, z, ndc

# -------------------------------
# ESCENA 3D
# -------------------------------

np.random.seed(1)

xs = np.linspace(-1.5, 1.5, 6)
ys = np.linspace(-1.0, 1.0, 4)
zs = np.linspace(1.0, 6.0, 6)
grid = np.array(np.meshgrid(xs, ys, zs)).reshape(3, -1)

low = np.array([-2, -1, 1])
high = np.array([2, 1, 6])

rand = np.random.uniform(low[:,None], high[:,None], size=(3,200))

points = np.hstack([grid, rand])
ones = np.ones((1, points.shape[1]))
points_h = np.vstack([points, ones])

# -------------------------------
# CÁMARA
# -------------------------------
eye = np.array([0.0, 0.5, -1.0])
center = np.array([0.0, 0.0, 2.5])
up = np.array([0.0, 1.0, 0.0])
view = look_at(eye, center, up)

# -------------------------------
# PROYECCIONES
# -------------------------------
fov = np.deg2rad(60.0)
aspect = 1.0
near, far = 0.1, 20.0

P_persp = perspective_fov(fov, aspect, near, far)
P_ortho = orthographic(-2, 2, -2, 2, near, far)

xy_persp, z_persp, ndc_p = project_points(P_persp, view, points_h)
xy_ortho, z_ortho, ndc_o = project_points(P_ortho, view, points_h)

# -------------------------------
# VISUALIZACIÓN
# -------------------------------

fig, axes = plt.subplots(1,2, figsize=(12,6))

ax = axes[0]
sc = ax.scatter(xy_persp[:,0], xy_persp[:,1], c=z_persp, cmap='viridis', s=18)
ax.set_title("Proyección Perspectiva (NDC) — color por profundidad")
ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_aspect('equal')
plt.colorbar(sc, ax=ax)

ax2 = axes[1]
sc2 = ax2.scatter(xy_ortho[:,0], xy_ortho[:,1], c=z_ortho, cmap='plasma', s=18)
ax2.set_title("Proyección Ortográfica — color por profundidad")
ax2.set_xlim(-1,1); ax2.set_ylim(-1,1); ax2.set_aspect('equal')
plt.colorbar(sc2, ax=ax2)

plt.suptitle("Perspectiva vs Ortográfica — Coordenadas homogéneas")
plt.tight_layout()
plt.savefig("proyecciones_demo.png", dpi=200)
plt.show()
