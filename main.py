#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query
app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str 
    last_name: str 
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}


#Requests and response body


@app.post("/person/new")
#Request body
# ... -> obligatorio
def create_person(person: Person = Body(...)):
    #Response body
    return person


#2.Validations: Query Parameters
@app.get("/person/detail")
def show_person(

    #Opcionalmente recibiremos un str
    #Por defecto será None
    #Si la persona escribe algo,debe ser menor a 50 caracteres y mayor a 1
    name: Optional[str] = Query(None,min_length=1,max_length=50),
    age: str = Query(...)
):
    return {name:age}