from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import json
import requests

url = 'https://main--astounding-scone-dc5764.netlify.app/.netlify/functions/api/cortes'

mydb = mysql.connector.connect(
  host="t07cxyau6qg7o5nz.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
  user="hjrsm3o5ntv2zaqp",
  password="rhqknldvk1o8luoy",
  database="g3i4dd7nd3sqo8m8"
)

mycursor = mydb.cursor()

class Columna(BaseModel):
    cant: Optional[int]
    Fe1: Optional[int]
    Fe2: Optional[int]
    FeE: Optional[int]
    Long1: Optional[float]
    Long2: Optional[float]
    Long3: Optional[float]
    Long4: Optional[float]
    Long5: Optional[float]
    Long6: Optional[float]
    Long7: Optional[float]
    Long8: Optional[float]
    Long9: Optional[float]
    e1C: Optional[int]
    e2C: Optional[int]
    e3C: Optional[int]
    eResto: Optional[float]
    e1S: Optional[float]
    e2S: Optional[float]
    e3S: Optional[float]
    eRestoS: Optional[float]

class Zapata(BaseModel):
    cant: Optional[int]
    Long1: Optional[float]
    Long2: Optional[float]
    Long3: Optional[float]
    Long4: Optional[float]
    Long5: Optional[float]

class Seccion(BaseModel):
    sMeasure: float
    sCant: int

class Luz(BaseModel):
    lz: Optional[float]
    lzC: Optional[int]

class Viga(BaseModel):
    fe1: Optional[int]
    fe2: Optional[int]
    Long1: Optional[float]
    Long2: Optional[float]
    Long3: Optional[float]
    Long4: Optional[float]
    Long5: Optional[float]
    Long6: Optional[float]

    secciones: List[Seccion] = []

    e1C: Optional[int]
    e2C: Optional[int]
    e3C: Optional[int]
    eResto: Optional[float]
    e1S: Optional[float]
    e2S: Optional[float]
    e3S: Optional[float]
    eRestoS: Optional[float]

    luces: List[Luz] = []

class OneItem(BaseModel):
    user : str
    cotizacion: str
    ibobjecto: str
    
    m1: float
    m2: float
    m3: float
    m4: float
    m5: float
    m6: float
    m7: float
    m8: float
    m9: float

    tipo: str
    cantidadRepeticiones: int

    acero1Tipo: str
    acero1Cantidad: int

    acero2Tipo: str
    acero2Cantidad: int

    aceroETipo: str
    aceroECantidad: int

    e1C: Optional[int]
    e2C: Optional[int]
    e3C: Optional[int]
    eResto: str
    e1S: Optional[float]
    e2S: Optional[float]
    e3S: Optional[float]
    eRestoS: Optional[float]
    
    secciones: List[Seccion] = []

    luces: List[Luz] = []

class OptimoItem(BaseModel):
    user : str
    cotizacion: str

app = FastAPI()

@app.post("/calculo/columna")
def columna_item(item: Columna):

    LargoAcero1 = item.Long3+item.Long4+item.Long5+item.Long6+item.Long7
    LargoAcero2 = item.Long3+item.Long4+item.Long5+item.Long6+item.Long7

    cantidadAcero1Total = item.Fe1 * item.cant
    cantidadAcero2Total = item.Fe2 * item.cant

    LongEstribo = (2*(item.Long1-(2*item.Long9)))+(2*(item.Long2-(2*item.Long9)))+(2*item.Long8)
    EspCubEstrMed = (2*((item.e1C*item.e1S)+(item.e2C*item.e2S)+(item.e3C*item.e3S)))
    EspacioIntermedio = item.Long4-EspCubEstrMed

    EstribosIntermedios = round((EspacioIntermedio/item.eRestoS)-1)
    TotalEstrColumna = (2*(item.e1C+item.e2C+item.e3C))+EstribosIntermedios
    TotalEstrTotal = TotalEstrColumna*item.cant

    result = {
        "LargoAcero1": LargoAcero1,
        "LargoAcero2": LargoAcero2,
        "cantidadAcero1Total": cantidadAcero1Total,
        "cantidadAcero2Total": cantidadAcero2Total,
        "LongEstribo": LongEstribo,
        "EspCubEstrMed": EspCubEstrMed,
        "EspacioIntermedio": EspacioIntermedio,
        "TotalEstrColumna": TotalEstrColumna,
        "TotalEstrTotal": TotalEstrTotal
    }

    return result

@app.post("/calculo/zapata")
def zapata_item(item: Zapata):

    longParrilla = item.Long1-(item.Long5*2)
    widthParrilla = item.Long2-(item.Long5*2)

    piezasL = longParrilla+(item.Long4*2)
    piezasA = widthParrilla+(item.Long4*2)
    cantidadPiezasL = round(longParrilla/item.Long3)

    cantidadPiezasA = round(widthParrilla/item.Long3)

    cantidadPiezasLTotal = cantidadPiezasL*item.cant
    cantidadPiezasATotal = cantidadPiezasA*item.cant

    result = {
        "longParrilla": longParrilla,
        "widthParrilla": widthParrilla,
        "piezasL": piezasL,
        "piezasA": piezasA,
        "cantidadPiezasL": cantidadPiezasL,
        "cantidadPiezasA": cantidadPiezasA,
        "cantidadPiezasLTotal": cantidadPiezasLTotal,
        "cantidadPiezasATotal": cantidadPiezasATotal
    }

    return result

@app.post("/calculo/viga")
def viga_item(item: Viga):

    seccionRetorno =[]

    for seccion in item.secciones:
        sLong =(seccion.sMeasure-(item.Long6*2)+(2*item.Long3))
        if (seccion.sMeasure-(item.Long6*2)+(2*item.Long3))>9 :
            sLong += item.Long4
        SFe1=item.fe1*seccion.sCant
        SFe2=item.fe2*seccion.sCant

        seccionRetorno.append({
            "sLong":sLong,
            "SFe1":SFe1,
            "SFe2":SFe2
        })

    EspCubEstrMedida = (2*((item.e1C*item.e1S)+(item.e2C*item.e2S)+(item.e3C*item.e3S)))
    FeELong = (2*(item.Long1-(2*item.Long6)))+(2*(item.Long2-(2*item.Long6)))+(2*item.Long5)
    TotalEstribos = 0
    lucesRetorno =[]
    for luz in item.luces:
        estrLuz=(2*(item.e1C+item.e2C+item.e3C))+(round(((luz.lz-EspCubEstrMedida)/item.eRestoS)-1))
        estrLuzCant = estrLuz*luz.lzC
        TotalEstribos += estrLuzCant

        lucesRetorno.append({
            "estrLuz":estrLuz,
            "estrLuzCant":estrLuzCant
        })

    return {
        "seccion":seccionRetorno,
        "EspCubEstrMedida":EspCubEstrMedida,
        "FeELong":FeELong,
        "lucesRetorno":lucesRetorno,
        "TotalEstribos":TotalEstribos
    }

@app.post("/calculo/one")
def oneCalculo(item: OneItem):
    result = {}
    if item.tipo == 'columna':
        columna = Columna()
        columna.cant = item.cantidadRepeticiones
        columna.Fe1 = item.acero1Cantidad
        columna.Fe2 = item.acero2Cantidad
        columna.FeE = item.aceroECantidad
        columna.Long1 = item.m1
        columna.Long2 = item.m2
        columna.Long3 = item.m3
        columna.Long4 = item.m4
        columna.Long5 = item.m5
        columna.Long6 = item.m6
        columna.Long7 = item.m7
        columna.Long8 = item.m8
        columna.Long9 = item.m9
        
        columna.e1C = item.e1C
        columna.e2C = item.e2C
        columna.e3C = item.e3C
        columna.eResto = item.eResto
        columna.e1S = item.e1S
        columna.e2S = item.e2S
        columna.e3S = item.e3S
        columna.eRestoS = item.eRestoS
        
        preResult = columna_item(columna)
        seccion=[]

        seccion.append({
            "sLong":preResult["LargoAcero1"],
            "SFe1":preResult["cantidadAcero1Total"],
            "SFe2":preResult["cantidadAcero2Total"]
        })
        result = {
            "seccion" : seccion,
            "FeELong" : preResult["LongEstribo"],
            "FeELongCantidad": preResult["TotalEstrTotal"],
            "lucesRetorno": [],
        }
        

        insertOneItem(item, preResult)

    if item.tipo == 'zapata':
        zapata = Zapata()
        zapata.cant = item.cantidadRepeticiones
        zapata.Long1 = item.m3
        zapata.Long2 = item.m4
        zapata.Long3 = item.m5
        zapata.Long4 = item.m6
        zapata.Long5 = item.m7

        preResult = zapata_item(zapata)
        seccion = []
        seccion.append({
            "sLong":preResult["piezasL"],
            "SFe1":preResult["cantidadPiezasLTotal"],
            "SFe2":0
        })
        seccion.append({
            "sLong":preResult["piezasA"],
            "SFe1":preResult["cantidadPiezasATotal"],
            "SFe2":0
        })

        result = {
            "FeELong" : 0,
            "FeELongCantidad": 0,
            "seccion" : seccion,
            "lucesRetorno": [],
        }

        insertOneItem(item, preResult)

    if item.tipo == 'vigas':
        viga = Viga()
        viga.fe1 = item.acero1Cantidad
        viga.fe2 = item.acero2Cantidad
        viga.Long1 = item.m1
        viga.Long2 = item.m2
        viga.Long3 = item.m3
        viga.Long4 = item.m4
        viga.Long5 = item.m8
        viga.Long6 = item.m9
        
        viga.secciones = item.secciones

        viga.luces = item.luces

        viga.e1C = item.e1C
        viga.e2C = item.e2C
        viga.e3C = item.e3C
        viga.eResto = item.eResto
        viga.e1S = item.e1S
        viga.e2S = item.e2S
        viga.e3S = item.e3S
        viga.eRestoS = item.eRestoS

        preResult = viga_item(viga)

        result = {
            "FeELong" : preResult["FeELong"],
            "FeELongCantidad" : preResult["TotalEstribos"],
            "seccion": preResult["seccion"],
            "lucesRetorno": preResult["lucesRetorno"],
        }
        insertOneItem(item, preResult)

    return result

@app.post("/calculo/optimo")
def optimoCalculos(OptiItem: OptimoItem):
    sql = "SELECT * FROM oneitem WHERE user ='"+OptiItem.user+"' AND cotizacion = '"+OptiItem.cotizacion+"'"
    print(sql)
    mycursor.execute(sql)

    myresults = mycursor.fetchall()

    tablas = {}

    for c in myresults:
        #print(c)
        request = json.loads(c[14])
        response = json.loads(c[15])
        #print(request)
        #print(response)
        if(request["tipo"] == "columna"):

            if(tablas.get( str(request["acero1Tipo"]) ) == None):
                tablas[ str(request["acero1Tipo"] ) ] = {} 
            if tablas.get( str(request["acero1Tipo"]) ).get( response["LongTotal"] ) == None :
                tablas.get( str(request["acero1Tipo"]) )[ response["LongTotal"] ] = response["f1Bar"]
            else:
                cant = tablas.get( str(request["acero1Tipo"]) )[ response["LongTotal"] ]
                tablas.get( str(request["acero1Tipo"]) )[ response["LongTotal"] ] = response["f1Bar"] + cant

            if(tablas.get(str(request["acero2Tipo"])) == None):
                tablas[ str(request["acero2Tipo"] ) ] = {} 
            if tablas.get( str(request["acero2Tipo"]) ).get( response["LongTotal"] ) == None :
                tablas.get( str(request["acero2Tipo"]) )[ response["LongTotal"] ] = response["f2Bar"]
            else:
                cant = tablas.get( str(request["acero2Tipo"]) )[ response["LongTotal"] ]
                tablas.get( str(request["acero2Tipo"]) )[ response["LongTotal"] ] = response["f2Bar"] + cant


        if(request["tipo"] == "zapata"):

            if(tablas.get( str(request["acero1Tipo"]) ) == None):
                tablas[ str(request["acero1Tipo"] ) ] = {} 
            
            if tablas.get( str(request["acero1Tipo"]) ).get( response["piezasL"] ) == None :
                tablas.get( str(request["acero1Tipo"]) )[ response["piezasL"] ] = response["cantidadPiezasLTotal"]
            else:
                cant = tablas.get( str(request["acero1Tipo"]) )[ response["piezasL"] ]
                tablas.get( str(request["acero1Tipo"]) )[ response["piezasL"] ] = response["cantidadPiezasLTotal"] + cant

            if tablas.get( str(request["acero1Tipo"]) ).get( response["piezasA"] ) == None :
                tablas.get( str(request["acero1Tipo"]) )[ response["piezasA"] ] = response["cantidadPiezasATotal"]
            else:
                cant = tablas.get( str(request["acero1Tipo"]) )[ response["piezasA"] ]
                tablas.get( str(request["acero1Tipo"]) )[ response["piezasA"] ] = response["cantidadPiezasATotal"] + cant
                
    resultFinal = []
    for keytabla in tablas.keys():
        measureKeys =tablas.get(keytabla)
        cutList = []
        for measure in measureKeys.keys():

            measureFloat = float(measure)
            cantidadMF = int(measureKeys.get(measure))

            cutList.append({
                "length" : int(measureFloat*100),
                "amount" : cantidadMF
            })

        request = {
            "maxCutLength"  : 900,
            "cutList"       : cutList
        }   

        x = requests.post(url, json = request)

        apiResponse = x.json()

        resultFinal.append({

            "cantidad" :apiResponse.get("numberOfMaterial"),
            "fierro" : keytabla,
            "cortes" : apiResponse.get("listOfCutsFinal")
        })

    return resultFinal

def insertOneItem(item: OneItem, preResult):

    sql = "SELECT * FROM oneitem WHERE ibobjecto ='"+item.ibobjecto+"';"
    print(sql)
    mycursor.execute(sql)

    myresults = mycursor.fetchall()
    if myresults != None:
        sql = "DELETE FROM oneitem WHERE (`ibobjecto` = '"+item.ibobjecto+"');"
        print(sql)
        mycursor.execute(sql)

    sql = "INSERT INTO oneitem (user, cotizacion, ibobjecto, tipo, jsonRequest, jsonResponse) VALUES (%s, %s, %s, %s, %s, %s)"
    val = ( 
        item.user,
        item.cotizacion,
        item.ibobjecto,
        item.tipo,
        json.dumps(item.dict()),
        json.dumps(preResult) )

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


