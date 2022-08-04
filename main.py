#Python
from doctest import Example
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel,EmailStr,Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path


app = FastAPI()

#Models

class HairColor(Enum): 
    
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):

    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )

    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )

    age: int = Field(
        gt = 0,
        le = 115
    )

    email: EmailStr = Field(...)

    hair_color: Optional[str] = Field(default = None)

    is_married: Optional[bool] = Field(default = None, example = False)

    class Config:

        schema_extra = {

            "example": {

                "first_name" : "Gabriel",
                "last_name" : "Aristizabal León",
                "age" : 19,
                "email" : "myemail@cosasdedevs.com",
                "hair_color" : "cafe"

            }

        }


class Location(BaseModel):
    city: str
    state: str
    country: str

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

        person_id: int = Path(
            ...,
            gt=0,
            example=123
        )
):
    return {person_id: "it exists!"}


#
@app.put("/person/{person_id}")
def update_person(

    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person id",
        gt=0,
        example=123
    ),

    person: Person = Body(...),
    location: Location = Body(...)
):

    results = person.dict()
    results.update(location.dict())

    return results