#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel,EmailStr,Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body,Query,Path,Form,Header,Cookie,UploadFile,File



app = FastAPI()

#-----------------Models------------------------#

class HairColor(Enum): 
    
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class PersonBase(BaseModel):

    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example="Gabriel"
    )

    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Aristizabal Leon"
    )

    age: int = Field(
        gt = 0,
        le = 115,
        example=19
    )

    email: EmailStr = Field(...,example = "myemail@cosasdedevs.com")

    hair_color: Optional[str] = Field(default = None, example="cafe")

    is_married: Optional[bool] = Field(default = None, example = False)


class Person(PersonBase):

    password: str = Field(
        ...,
        min_length=8,
        example = "kdlwodpi"
    )


class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city: str
    state: str
    country: str

class LoginOut(BaseModel):
    #username = str = Field(...,max_length=20)
    username: str = Field(..., max_length=20, example="gabriel2022")
    message:  str = Field(default="Login succesfully!")
#-----------------Fin Models---------------------#

#-----------------Path Operations----------------#
@app.get(
    path = "/",
    status_code = status.HTTP_200_OK
)
def home():
    return {"Hello": "World"}


#Requests and response body


@app.post(

    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons']
)
#Request body
# ... -> obligatorio
def create_person(person: Person = Body(...)):
    #Response body
    return person


#2.Validations: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=['Persons']
)
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
persons = [1,2,3,4,5]

@app.get(

    path="/person/detail/{person_id}",
    status_code = status.HTTP_200_OK,
    tags=['Persons']

)

def show_person(

        person_id: int = Path(
            ...,
            gt=0,
            example=123
        )
):
    if person_id not in persons:

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'This person doesn´t exits!'
        ) 
        
    return {person_id: "it exists!"}


#
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=['Persons']
)
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

#forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Persons']
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username=username)


#cookies and headers
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
)
def contact(

    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),

    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),

    email: EmailStr = Form(...),

    message: str = Form(
        ...,
        min_length=20
    ),

    user_agent: Optional[str] = Header(default=None),

    #cookie
    ads: Optional[str] = Cookie(default=None)

):
    return user_agent


#files
@app.post(
    path = '/post-image/'
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename ,
        "Format": image.content_type,
        "Size(kb)": round( len(image.file.read()) / 1024,ndigits=2)
    }
#-----------------Fin Path Operations----------------#