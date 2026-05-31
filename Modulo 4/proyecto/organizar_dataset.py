import os
import shutil

ORIGEN = r"C:\Users\Christian\Downloads\users\users"
DESTINO = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\raw"

print("Organizando dataset...")
print(f"Origen:  {ORIGEN}")
print(f"Destino: {DESTINO}\n")

os.makedirs(DESTINO, exist_ok=True)

copiados = 0
estudiantes = 0
errores = []

for carpeta in os.listdir(ORIGEN):
    ruta_carpeta = os.path.join(ORIGEN, carpeta)

    if not os.path.isdir(ruta_carpeta):
        continue

    # Crear carpeta destino con el mismo nombre
    destino_carpeta = os.path.join(DESTINO, carpeta)
    os.makedirs(destino_carpeta, exist_ok=True)

    fotos = [f for f in os.listdir(ruta_carpeta)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not fotos:
        errores.append(f"  Sin fotos: {carpeta}")
        continue

    for i, foto in enumerate(fotos):
        origen_foto  = os.path.join(ruta_carpeta, foto)
        # Renombrar a 001.jpg, 002.jpg, etc.
        destino_foto = os.path.join(destino_carpeta, f"{str(i+1).zfill(3)}.jpg")
        shutil.copy2(origen_foto, destino_foto)
        copiados += 1

    estudiantes += 1
    print(f"  ✓ {carpeta:<40} {len(fotos)} foto(s)")

print("\n" + "="*50)
print(f"  Estudiantes procesados : {estudiantes}")
print(f"  Fotos copiadas         : {copiados}")
print(f"  Promedio fotos/alumno  : {copiados/estudiantes:.1f}" if estudiantes else "")
if errores:
    print(f"\n  Carpetas sin fotos ({len(errores)}):")
    for e in errores:
        print(e)
print("="*50)
print("\nDataset listo en:", DESTINO)