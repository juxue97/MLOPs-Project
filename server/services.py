from fastapi import status, HTTPException
from fastapi.responses import JSONResponse

from us_visa.pipline.training_pipeline import TrainPipeline


async def train() -> JSONResponse:
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()

        return JSONResponse(
            content={"message": "Training process completed"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while training: {str(e)}",
        )
