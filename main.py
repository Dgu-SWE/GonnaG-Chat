from enum import Enum
from fastapi import FastAPI

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "description": "Deep Learning FTW"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "description": "LeCNN all the images"}

    return {"model_name": model_name, "description": "Have some residuals"}
