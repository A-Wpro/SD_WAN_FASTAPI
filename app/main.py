from fastapi import FastAPI 
from typing import Optional
app = FastAPI() 

@app.get("/")
def Docu():
    docuStr = "Voici la liste des features : GenerateOnosStruc(Param1: int, Param2: int, Param3: int, Param4: int) that generate Onos struc"

    return docuStr

#fonction test principal
@app.get("/GenerateOnosStruc")
def GenerateOnosStruc(Param1: int, Param2: int, Param3: int, Param4: int):
    return {"Hello": "World"}


