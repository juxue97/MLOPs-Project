from typing import Literal, Optional

from pydantic import BaseModel, Field


class PredictDataRequestForm(BaseModel):
    continent: Optional[Literal["Asia", "Africa", "North America",
                                "Europe", "South America", "Oceania"]] = None
    education_of_employee: Optional[Literal["High School",
                                            "Master's", "Bachelor's", "Doctorate"]] = None
    has_job_experience: Optional[Literal["Y", "N"]] = None
    region_of_employment: Optional[Literal["West",
                                           "Northeast", "South", "Midwest", "Island"]] = None
    unit_of_wage: Optional[Literal["Hour", "Year", "Week", "Month"]] = None
    full_time_position: Optional[Literal["Y", "N"]] = None

    no_of_employees: Optional[int] = Field(
        None, ge=1, description="Must be a positive integer")
    company_age: Optional[int] = Field(
        None, ge=0, description="Must be a non-negative integer")
    prevailing_wage: Optional[float] = Field(
        None, ge=0, description="Must be a non-negative number")


class PredictDataResponseForm(BaseModel):
    message: str = "Success"
    visaStatus: str = None
