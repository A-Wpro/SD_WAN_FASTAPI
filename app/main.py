import fastapi


from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse,RedirectResponse,ORJSONResponse,JSONResponse
from typing import Optional
import codecs
import os


def actions_RL():
    return "hello"


test = actions_RL()
app = FastAPI()


@app.get("/" , response_class=HTMLResponse)
def Docu():
    docuStr = "Voici la liste des features : GenerateOnosStruc(Param1: int, Param2: int, Param3: int, Param4: int) that generate Onos struc"
    file = codecs.open("Web/index.php", "r")

    return file.read()




#TODO : first enter redirected page into which we will first check the last id of graphs
#  to then create graph to then insert the id of the graph to the use

@app.get("/GenerateOnosStruc")
def GenerateOnosStruc():

    response = RedirectResponse(url='/?id=9')
    return response
@app.get("/{id}", response_class=HTMLResponse)
def Docu():
    file = codecs.open("Web/index.php", "r")

    return file.read()

