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
    pass


@dataclass
class ModelTrainingArtifact:
    pass


@dataclass
class ModelPusherArtifact:
    pass
