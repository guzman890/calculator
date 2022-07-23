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
    return {"message":"Hello TutLinks.com"}

@app.post("/calculo")
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