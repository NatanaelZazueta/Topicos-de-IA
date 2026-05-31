import numpy as np
import pickle
import io
from app.core.config import settings

class RecognitionService:
    def __init__(self):
        self.indice   = []   # lista de (nombre, vectores, datos_estudiante)
        self.threshold = settings.THRESHOLD
        self._cargar_embeddings()

    def _cargar_embeddings(self):
        print(f"Cargando embeddings desde {settings.EMBEDDINGS_PATH}...")
        with open(settings.EMBEDDINGS_PATH, 'rb') as f:
            db = pickle.load(f)
        for nombre, vectores in db.items():
            self.indice.append((nombre, np.array(vectores)))
        print(f"  {len(self.indice)} estudiantes cargados.")

    def identificar(self, embedding: list[float], datos_db: dict) -> dict:
        """
        embedding  : vector 512-D de la cámara
        datos_db   : dict {nombre_carpeta: {id, nombre, carrera, semestre}}
        """
        emb = np.array(embedding, dtype=np.float32)
        emb = emb / np.linalg.norm(emb)

        mejor_nombre = None
        mejor_score  = -1.0

        for nombre, vectores in self.indice:
            scores = emb @ vectores.T
            score  = float(np.max(scores))
            if score > mejor_score:
                mejor_score  = score
                mejor_nombre = nombre

        if mejor_score >= self.threshold and mejor_nombre:
            # Buscar datos reales en el dict de PostgreSQL
            datos = datos_db.get(mejor_nombre)
            if datos:
                return {
                    "status":    "IDENTIFICADO",
                    "id":        datos["id"],
                    "nombre":    datos["nombre"],
                    "carrera":   datos["carrera"],
                    "semestre":  datos["semestre"],
                    "confianza": round(mejor_score, 4),
                }
            else:
                # Reconocido pero sin datos en BD
                return {
                    "status":    "IDENTIFICADO",
                    "id":        None,
                    "nombre":    mejor_nombre,
                    "carrera":   "Sin datos",
                    "semestre":  None,
                    "confianza": round(mejor_score, 4),
                }
        else:
            return {
                "status":    "DESCONOCIDO",
                "id":        None,
                "nombre":    None,
                "carrera":   None,
                "semestre":  None,
                "confianza": round(mejor_score, 4),
            }

    def recargar(self):
        self.indice = []
        self._cargar_embeddings()

recognition_service = RecognitionService()