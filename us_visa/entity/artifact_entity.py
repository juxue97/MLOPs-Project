from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trainFilePath: str
    testFilePath: str


@dataclass
class DataValidationArtifact:
    pass


@dataclass
class DataTransformationArtifact:
    pass


@dataclass
class ModelTrainingArtifact:
    pass


@dataclass
class ModelPusherArtifact:
    pass
