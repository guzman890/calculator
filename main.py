from fastapi import FastAPI
from pydantic import BaseModel

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
def create_item(item: CalculoPrimerPiso):

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
def create_item(item: CalculoPrimerPiso):

    longParrilla = item.Long1-(item.Long3*2)
    widthParrilla = item.Long2-(item.Long3*2)
    separacionOptimizadaL = longParrilla/cantidadPiezasL
    separacionOptimizadaA = widthParrilla/cantidadPiezasL

    piezasL = longParrilla+(item.Long5*2)
    piezasA = widthParrilla+(item.Long5*2)
    cantidadPiezasL = round(longParrilla/item.Long4)
    cantidadPiezasA = round(widthParrilla/item.Long4)
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

@app.post("/calculo/viga")
def create_item(item: CalculoPrimerPiso):
    
    longWoEmpalme = item.Long4-(item.Long1*2)+(item.Long2*2)
    empalmeNeeded = 1 if longWoEmpalme>9 else 0
    longPiezaTotal = longWoEmpalme+(empalmeNeeded*item.Long3)

    result = {
        "longWoEmpalme": longWoEmpalme,
        "empalmeNeeded": empalmeNeeded,
        "longPiezaTotal": longPiezaTotal}

    return result