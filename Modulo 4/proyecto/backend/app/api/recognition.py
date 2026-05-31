from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import numpy as np
import cv2
from insightface.app import FaceAnalysis
from app.services.recognition_service import recognition_service
from app.models.database import get_db
from app.models.estudiante import Estudiante
from app.core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router   = APIRouter(prefix="/api/v1", tags=["Reconocimiento"])
security = HTTPBearer()

# Cargar InsightFace una sola vez
face_app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.35)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    return payload

@router.post("/identificar")
async def identificar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    # Leer imagen
    contents = await file.read()
    nparr    = np.frombuffer(contents, np.uint8)
    frame    = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        raise HTTPException(status_code=400, detail="Imagen inválida")

    # Detectar rostro y extraer embedding
    faces = face_app.get(frame)
    if not faces:
        return {"status": "SIN_ROSTRO", "confianza": 0.0}

    # Tomar el rostro más grande
    face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))

    if face.det_score < 0.35:
        return {"status": "SIN_ROSTRO", "confianza": 0.0}

    embedding = face.normed_embedding.tolist()

    # Cargar estudiantes de PostgreSQL
    result      = await db.execute(select(Estudiante))
    estudiantes = result.scalars().all()
    datos_db    = {}
    for e in estudiantes:
        datos_db[e.nombre] = {
            "id":       e.id,
            "nombre":   e.nombre,
            "carrera":  e.carrera,
            "semestre": e.semestre,
        }

    return recognition_service.identificar(embedding, datos_db)

@router.get("/estudiantes")
async def listar_estudiantes(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    result      = await db.execute(select(Estudiante))
    estudiantes = result.scalars().all()
    return [
        {"id": e.id, "nombre": e.nombre,
         "carrera": e.carrera, "semestre": e.semestre}
        for e in estudiantes
    ]

@router.post("/recargar")
async def recargar(user = Depends(get_current_user)):
    recognition_service.recargar()
    return {"mensaje": "Embeddings recargados",
            "estudiantes": len(recognition_service.indice)}