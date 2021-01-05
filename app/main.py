import fastapi


from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse,RedirectResponse,ORJSONResponse,JSONResponse
from typing import Optional
import codecs
import os
from TESTS.min_cost import min_cost






app = FastAPI()

#PAGE INDEX 
@app.get("/" , response_class=HTMLResponse)
def Docu():
    
    file = codecs.open("Web/index.html", "r")
    return file.read()

#RENTRE 2 VALEURS SOURCES ET TARGET ET DONNE LE CHEMIN LE PLUS COURS SELON MIN COST
@app.get("/GenerateOnosStruc")
async def GenerateOnosStruc(src: int = 0, trg: int = 10):
     
    return min_cost(0, 10)   

