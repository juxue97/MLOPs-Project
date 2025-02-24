from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

from server.models import PredictDataRequestForm, PredictDataResponseForm
from us_visa.entity.config_entity import PredictConfig
from us_visa.pipline.prediction_pipeline import USVisaClassifier
from us_visa.pipline.training_pipeline import TrainPipeline
from us_visa.utils.main_utils import result_mapping


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


async def predict(form: PredictDataRequestForm, request: Request) -> JSONResponse:
    try:
        payload = form.dict()

        # Convert dictionary to PredictConfig object
        payload = PredictConfig(**payload)

        pipeline = USVisaClassifier()
        df = pipeline.get_payload_data_as_df(payload=payload)

        result = pipeline.predict(dataFrame=df)[0].astype(int)
        visaStatus = result_mapping(value=result)

        response = PredictDataResponseForm(
            visaStatus=visaStatus,
        )

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while making prediction: {str(e)}",
        )

# {
#     "continent": "Asia",
#     "education_of_employee": "Bachelor's",
#     "has_job_experience": "Y",
#     "region_of_employment": "West",
#     "unit_of_wage": "Year",
#     "full_time_position": "Y",
#     "no_of_employees": 150,
#     "company_age": 10,
#     "prevailing_wage": 60000.50
# }
