from fastapi import APIRouter

from server.services import train, predict

routerTrain = APIRouter(prefix="/v1", tags=["Training Pipeline"])
routerPred = APIRouter(prefix="/v1", tags=["Prediction Pipeline"])

routerTrain.add_api_route(
    path="/train",
    endpoint=train,
    methods=["GET"],
    responses={
        200: {"description": "Training process completed"},
        500: {"description": "Server error while training"},
    },
)

routerPred.add_api_route(
    path="/predict",
    endpoint=predict,
    methods=["POST"],
    responses={
        200: {"description": "Prediction process completed"},
        500: {"description": "Server error while making prediction"},
    },
)
