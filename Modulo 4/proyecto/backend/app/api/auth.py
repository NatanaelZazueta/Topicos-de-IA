from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# Usuarios hardcodeados por ahora (luego conectamos PostgreSQL)
USUARIOS = {
    "admin@itc.edu": {
        "password": hash_password("admin123"),
        "rol": "ADMIN",
        "nombre": "Administrador"
    },
    "docente@itc.edu": {
        "password": hash_password("docente123"),
        "rol": "DOCENTE",
        "nombre": "Docente Demo"
    }
}

class LoginRequest(BaseModel):
    email:    str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    usuario = USUARIOS.get(req.email)
    if not usuario or not verify_password(req.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({
        "sub":    req.email,
        "rol":    usuario["rol"],
        "nombre": usuario["nombre"]
    })
    return {
        "access_token": token,
        "token_type":   "bearer",
        "rol":          usuario["rol"],
        "nombre":       usuario["nombre"]
    }