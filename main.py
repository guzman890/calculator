from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import json
import requests

url = 'https://main--astounding-scone-dc5764.netlify.app/.netlify/functions/api/cortes'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="db_test"
)

mycursor = mydb.cursor()

class CalculoPrimerPiso(BaseModel):
    cant: Optional[int]
    Fe1: Optional[int]
    Fe2: Optional[int]
    Fe3: Optional[int]
    Long1: Optional[float]
    Long2: Optional[float]
    Long3: Optional[float]
    Long4: Optional[float]
    Long5: Optional[float]

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

class OneItem(BaseModel):
    user : str
    cotizacion: str
    ibobjecto: str
    tipo: str
    cantidadRepeticiones: int
    acero1Tipo: str
    acero1Cantidad: int
    acero2Tipo: str
    acero2Cantidad: int
    m1: float
    m2: float
    m3: float
    m4: float
    m5: float

class calculoAll(BaseModel):
    columna: List[CalculoPrimerPiso] = []
    zapata: List[CalculoPrimerPiso] = []
    viga: List[vigaPrimerPiso] = []
    estribo: List[estriboPrimerPiso] = [] 

class OptimoItem(BaseModel):
    user : str
    cotizacion: str

class PzNItem(BaseModel):
    PzNPartida: str
    PzNMaterial: str
    PzNMedida: int
    PzNRepeticiones: float


app = FastAPI()

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


@app.post("/calculo/estribo")
def estribos_item(item: estriboPrimerPiso):
    detalle = []

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
        detalle.append(
            {
            "espacioIntermedio": espacioIntermedio,
            "estribosIntermedios": estribosIntermedios,
            "totalEstribos": totalEstribos,
            "longitudTotalEstribos": longitudTotalEstribos
            }
        )

    result ={
        "piezaEstribo" : piezaEstribo,
        "detalle" : detalle
    }    
    return result

@app.post("/calculo/one")
def oneCalculo(item: OneItem):
    result = {}
    if item.tipo == 'columna':
        columna = CalculoPrimerPiso()
        columna.cant = item.cantidadRepeticiones
        columna.Fe1 = item.acero1Cantidad
        columna.Fe2 = item.acero2Cantidad
        columna.Fe3 = 0
        columna.Long1 = item.m1
        columna.Long2 = item.m2
        columna.Long3 = item.m3
        columna.Long4 = item.m4
        columna.Long5 = item.m5

        preResult = columna_item(columna)
        result = {
            "Fe1Long1" : preResult["LongTotal"],
            "Fe2Long1" : preResult["LongTotal"],
            "Fe3Long1" : preResult["LongTotal"],
            "Fe1Long2" : 0,
            "Fe2Long2" : 0,
            "Fe3Long2" : 0,
            "Fe1Long1Cantidad" : preResult["f1Bar"],
            "Fe2Long1Cantidad" : preResult["f2Bar"],
            "Fe3Long1Cantidad" : preResult["f3Bar"],
            "Fe1Long2Cantidad" : 0,
            "Fe2Long2Cantidad" : 0,
            "Fe3Long2Cantidad" : 0
        }
        insertOneItem(item, preResult)

    if item.tipo == 'zapata':
        zapata = CalculoPrimerPiso()
        zapata.cant = item.cantidadRepeticiones
        zapata.Fe1 = item.acero1Cantidad
        zapata.Fe2 = 0
        zapata.Fe3 = 0
        zapata.Long1 = item.m1
        zapata.Long2 = item.m2
        zapata.Long3 = item.m3
        zapata.Long4 = item.m4
        zapata.Long5 = item.m5

        preResult = zapata_item(zapata)

        result = {
            "Fe1Long1" : preResult["piezasL"],
            "Fe2Long1" : 0,
            "Fe3Long1" : 0,
            "Fe1Long2" : preResult["piezasA"],
            "Fe2Long2" : 0,
            "Fe3Long2" : 0,
            "Fe1Long1Cantidad" : preResult["cantidadPiezasLTotal"],
            "Fe2Long1Cantidad" : 0,
            "Fe3Long1Cantidad" : 0,
            "Fe1Long2Cantidad" : preResult["cantidadPiezasATotal"],
            "Fe2Long2Cantidad" : 0,
            "Fe3Long2Cantidad" : 0
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
            "fierro" : keytabla
        })


    return resultFinal
    
@app.post("/calculo/all")
def allCalculos(allItems: calculoAll):
    resultadoColumna = []
    for columna in allItems.columna:
        resultadoColumna.append( columna_item(columna) )

    resultadoZapata = []
    for zapata in allItems.zapata:
        resultadoZapata.append( zapata_item(zapata) )

    resultadoViga = []
    for viga in allItems.viga:
        resultadoViga.append( viga_item(viga) )    

    resultadoEstribo = []
    for estribo in allItems.estribo:
        resultadoEstribo.append( estribos_item(estribo) )    

    result = {
        "columnas" : resultadoColumna,
        "zapata" : resultadoZapata,
        "viga" : resultadoViga,
        "estribo" : resultadoEstribo
    }   

    return result

def insertOneItem(item: OneItem, preResult):
    sql = "INSERT INTO oneitem (user, cotizacion, ibobjecto, tipo, cantidadRepeticiones, acero1Tipo, acero1Cantidad, acero2Tipo, acero2Cantidad, m1, m2, m3, m4, m5, jsonRequest, jsonResponse) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ( 
        item.user,
        item.cotizacion,
        item.ibobjecto,
        item.tipo,
        item.cantidadRepeticiones,
        item.acero1Tipo,
        item.acero1Cantidad, 
        item.acero2Tipo,
        item.acero2Cantidad,
        item.m1,
        item.m2,
        item.m3,
        item.m4,
        item.m5,
        json.dumps(item.dict()),
        json.dumps(preResult) )

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


