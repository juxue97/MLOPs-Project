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
class ClassificationMetricArtifact:
    accuracy: float
    f1_score: float
    precision_score: float
    recall_score: float


@dataclass
class ModelTrainerArtifact:
    trainedModelFilePath: str
    metricArtifact: ClassificationMetricArtifact


@dataclass
class ModelEvaluationArtifact:
    isModelAccepted: bool
    changedAccuracy: float
    s3ModelPath: str
    trainedModelPath: str


@dataclass
class ModelPusherArtifact:
    pass
