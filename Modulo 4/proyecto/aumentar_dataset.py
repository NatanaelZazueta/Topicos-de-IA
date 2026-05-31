import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis

ORIGEN  = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\raw"
DESTINO = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\processed"

VARIACIONES = 11   # fotos generadas por cada foto original
IMG_SIZE    = 112  # tamaño estándar ArcFace

print("Cargando detector facial...")
app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
print("Listo.\n")

# ── Funciones de augmentación ──────────────────────────────

def ajustar_brillo(img, factor):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:,:,2] = np.clip(hsv[:,:,2] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

def rotar(img, angulo):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angulo, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

def agregar_ruido(img, intensidad=15):
    ruido = np.random.randint(-intensidad, intensidad, img.shape, dtype=np.int16)
    return np.clip(img.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

def desenfoque(img, k=3):
    return cv2.GaussianBlur(img, (k, k), 0)

def flip_horizontal(img):
    return cv2.flip(img, 1)

def ajustar_contraste(img, alpha):
    return np.clip(img.astype(np.float32) * alpha, 0, 255).astype(np.uint8)

def generar_variaciones(rostro):
    return [
        rostro,                          # 1. original
        rotar(rostro, 10),               # 2. rotado +10°
        rotar(rostro, -10),              # 3. rotado -10°
        flip_horizontal(rostro),         # 4. espejo
        ajustar_brillo(rostro, 1.4),     # 5. más brillo
        ajustar_brillo(rostro, 0.6),     # 6. menos brillo
        ajustar_contraste(rostro, 1.3),  # 7. más contraste
        ajustar_contraste(rostro, 0.75), # 8. menos contraste
        agregar_ruido(rostro, 12),       # 9. ruido
        desenfoque(rostro, 3),           # 10. desenfoque
        rotar(flip_horizontal(rostro), 8) # 11. espejo + rotado
    ]

# ── Procesamiento principal ────────────────────────────────

def recortar_rostro(img):
    """Detecta, alinea y recorta el rostro principal a 112×112."""
    faces = app.get(img)
    if not faces:
        return None
    face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))
    if face.det_score < 0.6:
        return None

    x1, y1, x2, y2 = face.bbox.astype(int)
    # Padding del 15%
    pad_x = int((x2 - x1) * 0.15)
    pad_y = int((y2 - y1) * 0.15)
    h, w  = img.shape[:2]
    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(w, x2 + pad_x)
    y2 = min(h, y2 + pad_y)

    rostro = img[y1:y2, x1:x2]
    return cv2.resize(rostro, (IMG_SIZE, IMG_SIZE))

total_ok    = 0
total_skip  = 0
sin_rostro  = []

carpetas = sorted(os.listdir(ORIGEN))
print(f"Procesando {len(carpetas)} estudiantes...\n")

for idx, carpeta in enumerate(carpetas, 1):
    ruta_origen  = os.path.join(ORIGEN, carpeta)
    ruta_destino = os.path.join(DESTINO, carpeta)

    if not os.path.isdir(ruta_origen):
        continue

    fotos = [f for f in os.listdir(ruta_origen)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not fotos:
        sin_rostro.append(carpeta)
        continue

    os.makedirs(ruta_destino, exist_ok=True)
    guardadas = 0

    for foto in fotos:
        img = cv2.imread(os.path.join(ruta_origen, foto))
        if img is None:
            continue

        rostro = recortar_rostro(img)
        if rostro is None:
            total_skip += 1
            continue

        for v_idx, variacion in enumerate(generar_variaciones(rostro)):
            nombre = f"{foto.replace('.jpg','').replace('.jpeg','').replace('.png','')}_{str(v_idx+1).zfill(2)}.jpg"
            cv2.imwrite(os.path.join(ruta_destino, nombre), variacion)
            guardadas += 1

    total_ok += guardadas
    print(f"  [{idx:>3}/{len(carpetas)}] {carpeta:<45} → {guardadas} imágenes")

print("\n" + "="*55)
print(f"  Imágenes generadas total : {total_ok}")
print(f"  Fotos sin rostro (skip)  : {total_skip}")
if sin_rostro:
    print(f"  Estudiantes sin fotos    : {len(sin_rostro)}")
    for s in sin_rostro:
        print(f"    - {s}")
print("="*55)
print(f"\nDataset procesado en: {DESTINO}")