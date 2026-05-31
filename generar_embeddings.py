import cv2
import os
import numpy as np
import pickle
from insightface.app import FaceAnalysis

PROCESSED = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\processed"
SALIDA    = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\embeddings.pkl"

# det_size vuelve a 640x640 para evitar el bug de shapes
app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.35)

# Cargar sesión de reconocimiento directamente para el fallback
rec_session  = app.models['recognition'].session
rec_input    = rec_session.get_inputs()[0].name

def embedding_directo(img_112):
    """Extrae embedding sin pasar por el detector."""
    img = cv2.resize(img_112, (112, 112))
    img = img.astype(np.float32)
    img = (img - 127.5) / 127.5
    img = img.transpose(2, 0, 1)[np.newaxis]          # (1,3,112,112)
    result = rec_session.run(None, {rec_input: img})
    emb = result[0][0]
    return emb / np.linalg.norm(emb)

embeddings_db = {}
total_imgs    = 0
total_skip    = 0

carpetas = sorted(os.listdir(PROCESSED))
print(f"Generando embeddings para {len(carpetas)} estudiantes...\n")

for idx, carpeta in enumerate(carpetas, 1):
    ruta = os.path.join(PROCESSED, carpeta)
    if not os.path.isdir(ruta):
        continue

    fotos = sorted([f for f in os.listdir(ruta) if f.endswith('.jpg')])
    vectores = []

    for foto in fotos:
        img = cv2.imread(os.path.join(ruta, foto))
        if img is None:
            continue

        try:
            faces = app.get(img)
            if faces:
                emb = faces[0].normed_embedding
            else:
                # Fallback: la imagen ya es 112x112, extraer directo
                emb = embedding_directo(img)
        except Exception:
            emb = embedding_directo(img)

        vectores.append(emb)
        total_imgs += 1

    if vectores:
        embeddings_db[carpeta] = np.array(vectores)
        print(f"  [{idx:>3}/{len(carpetas)}] {carpeta:<45} {len(vectores):>4} embeddings")
    else:
        total_skip += 1
        print(f"  [{idx:>3}/{len(carpetas)}] {carpeta:<45} SIN EMBEDDINGS")

with open(SALIDA, 'wb') as f:
    pickle.dump(embeddings_db, f)

print("\n" + "="*55)
print(f"  Estudiantes procesados : {len(embeddings_db)}")
print(f"  Embeddings generados   : {total_imgs}")
print(f"  Estudiantes sin emb.   : {total_skip}")
print(f"  Archivo guardado       : {SALIDA}")
print("="*55)