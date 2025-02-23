import sys
from fastapi import status
from fastapi.responses import Response

from us_visa.pipline.training_pipeline import TrainPipeline


async def train():
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()

        return Response("Training process completed", status_code=status.HTTP_200_OK)

    except Exception as e:
        raise Response(
            f"Error occur while training: {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
