from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trainFilePath: str
    testFilePath: str


@dataclass
class DataValidationArtifact:
    validationStatus: bool
    message: str
    driftReportFilePath: str


@dataclass
class DataTransformationArtifact:
    transformedObjectFilePath: str
    transformedTrainFilePath: str
    transformedTestFilePath: str


@dataclass
class ModelTrainingArtifact:
    pass


@dataclass
class ModelPusherArtifact:
    pass
