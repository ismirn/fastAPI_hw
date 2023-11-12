from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import List
from datetime import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/root')
def root__get():
    return RedirectResponse('https://http.cat/404')

@app.post("/post", response_model=List[Timestamp], summary="Get Post")
def get_post_post_post():
    current_timestamp = int(datetime.now().timestamp())
    new_post = Timestamp(id=len(post_db), timestamp=current_timestamp)
    post_db.append(new_post)
    return post_db

@app.get("/dog", response_model=List[Dog], summary="Get Dogs",
         operation_id="get_dogs_dog_get")
def get_dogs_dog(kind: DogType = Query(None, description="Kind of dog")):
    if kind:
        filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return filtered_dogs
    else:
        return list(dogs_db.values())

@app.post("/dog", response_model=Dog, summary="Create Dog",
          operation_id="create_dog_dog_post")
def create_dog_dog_post(dog: Dog):
    new_pk = max(dogs_db.keys()) + 1
    dog.pk = new_pk
    dogs_db[new_pk] = dog
    return dog

@app.get("/dog/{pk}", response_model=Dog, summary="Get Dog By Pk",
         operation_id="get_dog_by_pk_dog__pk__get", tags=["Dog"])
def get_dog_by_pk_dog_pk(pk: int):
    if pk in dogs_db:
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=404, detail="Dog not found")

@app.patch("/dog/{pk}", response_model=Dog, summary="Update Dog",
           operation_id="update_dog_dog__pk__patch", tags=["Dog"])
def update_dog_dog_pk(pk: int, dog: Dog):
    if pk in dogs_db:
        dogs_db[pk] = dog
        return dog
    else:
        raise HTTPException(status_code=404, detail="Dog not found")