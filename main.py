from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import uvicorn
from mail import enviar_correo_orden

app = FastAPI(
    title="Servicio de Correo - SENAE",
    description="API para envío de correos electrónicos con documentos adjuntos",
    version="1.0.0"
)

# Configurar CORS para permitir llamadas desde PHP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrdenEmailRequest(BaseModel):
    """
    Modelo de datos para envío de email de orden de movilización
    """
    destinatario: EmailStr
    numero_orden: str
    conductor_nombre: str
    ciudad: str
    destino: str
    fecha_inicio: str
    fecha_fin: str
    archivo_pdf_path: Optional[str] = None

@app.get("/")
async def root():
    """
    Endpoint raíz para verificar que el servicio está corriendo
    """
    return {
        "servicio": "Servicio de Correo SENAE",
        "estado": "activo",
        "version": "1.0.0",
        "status": "ok"
    }


#Endpoint para enviar email de orden de movilización con PDF adjunto
@app.post("/enviar-orden")
async def enviar_orden_email(request: OrdenEmailRequest):

    try:
        resultado = enviar_correo_orden(
            destinatario=request.destinatario,
            numero_orden=request.numero_orden,
            conductor_nombre=request.conductor_nombre,
            ciudad=request.ciudad,
            destino=request.destino,
            fecha_inicio=request.fecha_inicio,
            fecha_fin=request.fecha_fin,
            archivo_pdf_path=request.archivo_pdf_path
        )

        if resultado['exito']:
            return {
                "resultado": "EXITOSO",
                "mensaje": resultado['mensaje'],
                "id_mensaje": resultado['id_mensaje']
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=resultado['mensaje']
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar email: {str(e)}"
        )

if __name__ == "__main__":
    # Ejecutar servidor en puerto 8000
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
