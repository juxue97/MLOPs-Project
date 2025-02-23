# MLOPs-Project

This repository is dedicated to revising and optimizing a data science project by integrating MLOps (Machine Learning Operations) practices and utilizing standard production tools. The goal is to enhance the project’s workflow, deployment, and scalability to align with industry best practices in machine learning lifecycle management.

## Project Overview

This project covers the end-to-end process of building, training, and deploying machine learning models while ensuring that every step adheres to MLOps principles, such as reproducibility, version control, automation, and monitoring. We leverage modern tools and frameworks for experiment tracking, model versioning, and automated deployments.

## Key Features:

- Data Preparation: ETL pipeline for cleaning, transforming, and loading data for training.
- Experiment Tracking: Use of MLflow for tracking models, parameters, metrics, and artifacts.
- Model Versioning: Automated model versioning and registry management via MLflow.
- Deployment: Model deployment and serving using MLflow's REST API or Docker.
- CI/CD Pipeline: Fully integrated CI/CD pipeline using GitHub Actions for continuous testing, building, and deployment.
- Monitoring: Monitoring model performance and health using MLflow and logging systems.

## Workflow

- ETL: Extract raw data, apply necessary transformations, and load it into structured formats for training.
- Model Training: Train models using best practices and log all experiments with MLflow.
- Model Versioning: Manage model versions, track experiment metadata, and maintain reproducibility through MLflow Model Registry.
- Deployment: Deploy models using MLflow’s REST API or through Docker containers.
- CI/CD: Automate the building, testing, and deployment process via a CI/CD pipeline integrated with GitHub Actions.
- Monitoring and Maintenance: Continuously monitor models in production, ensuring they are performing as expected.

## Tools and Technologies

- MLOPs' tool (MLflow/Evidently): Experiment tracking, model management, and deployment. (https://www.evidentlyai.com)
- Flowchart: Project planning, tracking progression (https://whimsical.com)
- Docker: Containerization for model deployment.
- GitHub Actions: CI/CD pipeline for automated testing and deployment.
- pandas, scikit-learn: Data manipulation and machine learning libraries.
- Flask/FastAPI: Model-serving API for inference.

## Setup the python environment

- create environment: python -m venv venv
- activate environment: venv/Scrips/activate
- download packages/libraries: pip install -r requirements.txt

## Current task:

- setup the training pipeline

  - data ingestion -> data ingestion artifact
  - data validation (data ingestion artifact) -> data validation artifact & status
  - data transformation (data ingestion artifact, data validation artifact & status) -> data transformation artifact
  - model training (data transformation artifact) -> model training artifact
  - model evaluation (data ingestion artifact, model training artifact) -> model acceptanace status
  - model push2cloud (mode acceptance status) - > s3

  ## How to run the server?

  1. Create/Activate your python environment (python -m venv venv && venv/Scripts/activate)
  2. Pip install all the necessary libraries (pip install -r requirements.txt)
  3. Refer to the .env.example for neccessary credentials for running the program
  4. Run the http server using command : python -m server.main
