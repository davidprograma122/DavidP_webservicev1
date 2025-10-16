
from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo
import random

ahora = datetime.now()
hora_actual = ahora.time()

app= FastAPI()
country_timezones ={
    "CO": "America/Bogota",
    "AR": "America/Argentina/Buenos_Aires",
    "CL": "America/Santiago",
    "PE": "America/Lima",
    "MX": "America/Mexico_City",
    "EC": "America/Guayaquil",
    "VE": "America/Caracas",
}




@app.get("/")
async def root():
    return {"message": "Hola David"}

@app.get("/time/{iso_code}")
async def get_time(iso_code: str):
    iso = iso_code.upper()
    timezoe_str = country_timezones.get(iso)
    tz = ZoneInfo(timezoe_str)
    return {"time": datetime.now(tz)}



@app.get("/saludo/{nombre}")
async def saludar(nombre: str):
    return {"saludo": f"Hola {nombre}, bienvenido al webservice"}






ciudades_imbabura = {
    "IBARRA": "Ibarra",
    "OTAVALO": "Otavalo",
    "COTACACHI": "Cotacachi",
    "ANTONIO_ANTE": "Antonio Ante",
    "PIMAMPIRO": "Pimampiro",
    "URCUQUI": "Urcuquí"
}


#DEBER SIMULACION DE CLIMA
@app.get("/clima_random/{ciudad}")
async def clima_simulado(ciudad: str):
    # Verificar si la ciudad está en Imbabura
    ciudad_upper = ciudad.upper().replace(" ", "_")

    if ciudad_upper not in ciudades_imbabura:
        return {
            "error": f"La ciudad '{ciudad}' no está en la provincia de Imbabura",
        }

    nombre_ciudad = ciudades_imbabura[ciudad_upper]

    # Simula datos de clima aleatorios
    temperatura = random.randint(10, 30)
    humedad = random.randint(30, 90)

    condiciones = ["Soleado", "Nublado", "Parcialmente nublado", "Lluvioso", "Tormenta electrica"]
    condicion = random.choice(condiciones)

    # Determina recomendación por condiciones
    if condicion in ["Lluvioso", "Tormenta electrica"]:
        recomendacion = "Lleva paraguas"
    elif temperatura > 24:
        recomendacion = "Usa protector solar y mantente hidratado"
    elif temperatura < 18:
        recomendacion = "Considera llevar una chaqueta"
    else:
        recomendacion = "Buen día para salir"

    return {
        "ciudad": nombre_ciudad,
        "temperatura": f"{temperatura} °C",
        "humedad": f"{humedad}%",
        "condicion": condicion,
        "recomendacion": recomendacion
    }


