#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path


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
    
    name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title = "Person name",
            description = "This is the person name. It´s between 1 and 50 characters"
        ),
    
    age: int = Query(
        ...,
        title = "Person age",
        description = "This is the person age. It´s required"
    )

):
    return {name:age}


#3.Validaciones: Path parameters
@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(...,gt=0)
):
    return {person_id: "it exists!"}