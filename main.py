from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class CalculoPrimerPiso(BaseModel):
    cant: int
    Fe1: int
    Fe2: int
    Fe3: int
    Long1: float
    Long2: float
    Long3: float
    Long4: float
    Long5: float

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"Hello World"}

@app.post("/calculo/columna")
def columna_item(item: CalculoPrimerPiso):

    LongTotal = item.Long1+item.Long2+item.Long3+item.Long4+item.Long5

    cantBarByDefault = int(9/LongTotal)
    fe1CantByDefault = (item.Fe1*item.cant)/cantBarByDefault
    fe2CantByDefault = (item.Fe2*item.cant)/cantBarByDefault
    fe3CantByDefault = (item.Fe3*item.cant)/cantBarByDefault

    feCantByDefault = fe1CantByDefault + fe2CantByDefault + fe3CantByDefault

    TotalBar = (item.Fe1 + item.Fe2 + item.Fe3)*item.cant
    f1Bar = (item.Fe1)*item.cant
    f2Bar = (item.Fe2)*item.cant
    f3Bar = (item.Fe3)*item.cant

    LongResi = 9-LongTotal*cantBarByDefault

    result = {
        "TotalBar": TotalBar,
        "feCantByDefault": feCantByDefault,
        "fe1CantByDefault": fe1CantByDefault,
        "fe2CantByDefault": fe2CantByDefault,
        "fe3CantByDefault": fe3CantByDefault,
        "LongTotal": LongTotal,
        "LongResi": LongResi,
        "f1Bar": f1Bar,
        "f2Bar": f2Bar,
        "f3Bar": f3Bar}

    return result

@app.post("/calculo/zapata")
def zapata_item(item: CalculoPrimerPiso):

    longParrilla = item.Long1-(item.Long3*2)
    widthParrilla = item.Long2-(item.Long3*2)

    piezasL = longParrilla+(item.Long5*2)
    piezasA = widthParrilla+(item.Long5*2)
    cantidadPiezasL = round(longParrilla/item.Long4)

    separacionOptimizadaL = longParrilla/cantidadPiezasL

    cantidadPiezasA = round(widthParrilla/item.Long4)

    separacionOptimizadaA = widthParrilla/cantidadPiezasA

    cantidadPiezasLTotal = cantidadPiezasL*item.cant
    cantidadPiezasATotal = cantidadPiezasA*item.cant

    result = {
        "longParrilla": longParrilla,
        "widthParrilla": widthParrilla,
        "separacionOptimizadaL": separacionOptimizadaL,
        "separacionOptimizadaA": separacionOptimizadaA,
        "piezasL": piezasL,
        "piezasA": piezasA,
        "cantidadPiezasL": cantidadPiezasL,
        "cantidadPiezasA": cantidadPiezasA,
        "cantidadPiezasLTotal": cantidadPiezasLTotal,
        "cantidadPiezasATotal": cantidadPiezasATotal}

    return result

class seccion(BaseModel):
    Long: float
    Cant: int

class vigaPrimerPiso(BaseModel):
    fe1: float
    fe2: float
    recubriemiento: float
    gancho: float
    empalme: float
    secciones: List[seccion] = []

@app.post("/calculo/viga")
def viga_item(item: vigaPrimerPiso):
    result = []
    for secc in item.secciones:
        longWoEmpalme = secc.Long-(item.recubriemiento*2)+(item.gancho*2)
        empalmeNeeded = 1 if longWoEmpalme>9 else 0
        longPiezaTotal = longWoEmpalme+(empalmeNeeded*item.empalme)
        result.append(
            {
            "longWoEmpalme": longWoEmpalme,
            "empalmeNeeded": empalmeNeeded,
            "longPiezaTotal": longPiezaTotal
            }
        )
    return result

class distribucion(BaseModel): 
    cantidad: int
    separacion: float

class estriboPrimerPiso(BaseModel):
    ancho: float
    alto: float
    recubriemiento: float
    gancho: float
    secciones: List[seccion] = []
    distribuciones: List[distribucion] = []

@app.post("/calculo/estribo")
def estribos_item(item: estriboPrimerPiso):
    result = []

    piezaEstribo = (2*(item.ancho-(2*item.recubriemiento)))+(2*(item.alto-(2*item.recubriemiento)))+(2*item.gancho)
    print(piezaEstribo)
    estribosMedida = 0 

    resto = 0
    cantidadEstribos = 0
    for distri in item.distribuciones:
        estribosMedida += 2*(distri.cantidad*distri.separacion)
        resto = distri.separacion if distri.separacion>0 else resto
        cantidadEstribos += distri.cantidad
    print(estribosMedida)

    for secc in item.secciones:
        espacioIntermedio = secc.Long-estribosMedida
        estribosIntermedios = round((espacioIntermedio/resto)-1)
        totalEstribos = (2*(cantidadEstribos)) + estribosIntermedios
        longitudTotalEstribos = totalEstribos*piezaEstribo
        result.append(
            {
            "espacioIntermedio": espacioIntermedio,
            "estribosIntermedios": estribosIntermedios,
            "totalEstribos": totalEstribos,
            "longitudTotalEstribos": longitudTotalEstribos
            }
        )
    return result