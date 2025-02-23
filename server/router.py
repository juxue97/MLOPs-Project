from fastapi import APIRouter, status

from us_visa.pipline.training_pipeline import TrainPipeline
from server.services import train

routerTrain = APIRouter(prefix="/v1", tags=["Training Pipeline"])
# routerPred = APIRouter(prefix="/v1", tags=["Prediction Pipeline"])

routerTrain.add_api_route(
    path="/train",
    endpoint=train,
    methods=["GET"],
    responses={
        200: {"description": "Training started successfully"},
        500: {"description": "Server error while training"},
    },
)

# routerPred.add_api_route(
#     path="/",
#     endpoint=TrainPipeline().run_pipeline,
#     status_code=status.HTTP_200_OK,
#     methods=["GET"],
# )
