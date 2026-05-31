import os

PROCESSED = r"C:\Users\Christian\Downloads\Reconocimiento_Facial_ITC\dataset\processed"

total_estudiantes = 0
total_imagenes    = 0
criticos          = []  # menos de 11 imágenes (menos de 1 foto original)
bajos             = []  # entre 11 y 21 (1-2 fotos originales)
normales          = []  # 22-32
buenos            = []  # 33+

for carpeta in sorted(os.listdir(PROCESSED)):
    ruta = os.path.join(PROCESSED, carpeta)
    if not os.path.isdir(ruta):
        continue

    imgs = len([f for f in os.listdir(ruta) if f.endswith('.jpg')])
    total_estudiantes += 1
    total_imagenes    += imgs

    if imgs < 11:
        criticos.append((carpeta, imgs))
    elif imgs < 22:
        bajos.append((carpeta, imgs))
    elif imgs < 33:
        normales.append((carpeta, imgs))
    else:
        buenos.append((carpeta, imgs))

print("="*55)
print("  RESUMEN DEL DATASET")
print("="*55)
print(f"  Total estudiantes : {total_estudiantes}")
print(f"  Total imágenes    : {total_imagenes}")
print(f"  Promedio imgs/est : {total_imagenes/total_estudiantes:.1f}")
print()
print(f"  ✓ Bien  (33+ imgs) : {len(buenos)} estudiantes")
print(f"  ~ OK    (22-32)    : {len(normales)} estudiantes")
print(f"  ↓ Bajo  (11-21)    : {len(bajos)} estudiantes")
print(f"  ✗ Crítico (<11)    : {len(criticos)} estudiantes")
print("="*55)

if criticos:
    print("\nEstudiantes CRÍTICOS:")
    for nombre, n in criticos:
        print(f"  ✗ {nombre:<45} {n} imgs")

if bajos:
    print(f"\nEstudiantes BAJOS ({len(bajos)}):")
    for nombre, n in bajos:
        print(f"  ↓ {nombre:<45} {n} imgs")