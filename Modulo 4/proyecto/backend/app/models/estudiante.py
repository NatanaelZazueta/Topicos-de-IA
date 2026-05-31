from sqlalchemy import Column, String, Integer, LargeBinary
from app.models.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes_itc"

    id       = Column(String(20), primary_key=True)
    nombre   = Column(String(100))
    carrera  = Column(String(100))
    semestre = Column(Integer)
    encoding = Column(LargeBinary)