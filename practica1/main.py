import cv2
import numpy as np
import glob

# Definir dimensiones del tablero (esquinas internas)
chessboard_size = (9, 6)

# Criterio de terminación de subpixeles
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Preparar puntos 3D (0,0,0 ... 8,5,0)
objp = np.zeros((np.prod(chessboard_size), 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

objpoints = [] # Puntos 3D
imgpoints = [] # Puntos 2D

# Cargar imágenes del tablero
images = glob.glob('chessboard/*.jpg') + glob.glob('chessboard/*.jpeg')
print("Imágenes encontradas:", len(images))

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

# Calibración
if len(objpoints) > 0 and len(imgpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )
    print("Matriz de la cámara:\n", mtx)
    print("Coeficientes de distorsión:\n", dist)
else:
    print("No se detectaron esquinas en las imágenes. Revisa las fotos del tablero.")


# Corrección de una imagen de prueba
img = cv2.imread(images[0])
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
cv2.imwrite('calibrated_result.jpg', dst)
