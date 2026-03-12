# **RetailForecastML – End-to-End Retail Demand Forecasting Pipeline**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-lightgrey)
![DVC](https://img.shields.io/badge/DVC-Data%20Versioning-purple)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-orange)
![Grafana](https://img.shields.io/badge/Dashboard-Grafana-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)

---

# Overview

**RetailForecastML** is a production-style machine learning project designed to forecast daily retail item demand using an automated MLOps pipeline.

Accurate demand prediction is critical for retail businesses to manage inventory, reduce stock shortages, and improve supply chain efficiency. This project demonstrates how machine learning models can be integrated into a modern MLOps workflow that includes automated retraining, monitoring, version control, and scalable deployment.

The pipeline covers the complete lifecycle of a machine learning system — from data preparation and feature engineering to model deployment and operational monitoring.

Key goals of the project include:

* Forecasting daily sales for retail store items using regression models
* Detecting data and concept drift to maintain model reliability
* Automating retraining and model updates through CI/CD pipelines
* Deploying the model as a REST API using FastAPI
* Monitoring system performance using Prometheus and Grafana dashboards

---

# Project Workflow

Below is a high-level overview of the forecasting pipeline.

<img width="4328" height="2894" alt="image" src="https://github.com/user-attachments/assets/0fa8cb53-b633-4505-90d9-11d00649e6bf" />

---

# 1. Data Processing and Model Development

The project begins by preparing the dataset and building a baseline forecasting model.

Key steps include:

* Loading the retail sales dataset (`train.csv`) and performing data cleaning.
* Handling missing values and removing outliers to ensure data quality.
* Engineering time-based features such as:

  * `year`
  * `month`
  * `day`
  * `day_of_week`
  * `is_weekend`
* Creating lag features to capture temporal dependencies:

  * `lag_1`
  * `lag_7`
  * `lag_30`
* Generating rolling statistical features:

  * `rolling_mean_7`
  * `rolling_mean_30`
* Splitting the dataset into chronological training and testing sets.
* Training machine learning models including:

  * **XGBoost Regressor**
  * **Random Forest Regressor**
* Evaluating model performance using:

  * **MAE (Mean Absolute Error)**
  * **RMSE (Root Mean Squared Error)**
  * **MAPE (Mean Absolute Percentage Error)**

The trained model is saved to `models/model.pkl`, while evaluation metrics are stored in `models/metrics.json`.

This stage establishes the baseline forecasting model for the entire pipeline.

---

# 2. Drift Detection and Model Reliability

To maintain long-term model performance, the system incorporates mechanisms to detect both **data drift** and **concept drift**.

### Data Drift Detection

Data drift occurs when the distribution of incoming data changes compared to the original training data.

This project uses the **Evidently AI** library to:

* Compare feature distributions between reference and incoming data
* Generate automated drift reports in HTML format
* Identify significant deviations in feature behavior

### Concept Drift Detection

Concept drift occurs when the relationship between input features and the target variable changes over time.

This is monitored by:

* Comparing current model performance with baseline metrics
* Triggering alerts if performance drops beyond predefined thresholds (for example, MAPE increase >20%)
* Logging drift events in `logs/drift_logs.log`
* Storing summarized results in `reports/drift_summary.json`

These monitoring steps ensure the system can automatically determine when model retraining is required.

---

# 3. Automated Retraining Pipeline

To ensure the forecasting model stays accurate over time, retraining is fully automated.

### Data and Model Versioning

The project uses **DVC (Data Version Control)** for managing datasets and trained models.

Key advantages include:

* Version tracking for datasets and model artifacts
* Efficient storage of large files outside the Git repository
* Reproducible data pipelines

The remote storage backend is integrated with **DagsHub**.

<img width="1897" height="736" alt="image" src="https://github.com/user-attachments/assets/fdd03e86-9b26-434a-a0e2-680fa3a8b1d7" />


### Retraining Workflow

The retraining script located in:

```
src/retraining/retrain_pipeline.py
```

performs the following tasks:

* Retrieves the latest dataset using DVC
* Executes feature engineering steps
* Retrains the forecasting model
* Evaluates the updated model
* Stores the new model and metrics with version identifiers
* Logs retraining activities for traceability

Retraining can be triggered automatically when drift detection flags indicate that model performance has degraded.

### GitHub Actions Automation

A scheduled **GitHub Actions workflow** orchestrates the retraining process by:

* Checking for drift indicators
* Running retraining scripts
* Updating model artifacts
* Synchronizing new versions with DVC and DagsHub

This ensures that the system can update itself automatically when necessary.

---

# 4. Model Deployment with FastAPI and Docker

The trained forecasting model is deployed as a REST API using **FastAPI**.

### API Endpoints

The API provides two main endpoints:

```
/           → Health check endpoint
/predict    → Returns demand forecasts
```

The FastAPI service loads the most recent model version through DVC integration.

### Containerization

The application is packaged using **Docker**, allowing consistent execution across environments.

Containerization enables:

* Easy deployment
* Dependency isolation
* Scalability across cloud platforms

The project is deployed on **Hugging Face Spaces**, allowing public access to the forecasting API.

---

# 5. Monitoring and Observability

To ensure reliable production operation, the system integrates a monitoring stack.

<img width="1919" height="905" alt="image" src="https://github.com/user-attachments/assets/3c30b1e3-9f5f-498a-86e1-639d6a95911f" />


### Monitoring Components

**Prometheus**

* Collects runtime metrics such as:

  * API request count
  * response latency
  * error rates

**Grafana**

* Visualizes collected metrics through interactive dashboards.

**Prometheus Python Client**

* Instruments the FastAPI application to expose metrics through the `/metrics` endpoint.

**Docker Compose**

* Orchestrates FastAPI, Prometheus, and Grafana services together.

<img width="1911" height="908" alt="image" src="https://github.com/user-attachments/assets/2300ab95-daf9-466d-9be6-8f478fbb33e0" />


Through this setup users can monitor:

* API performance
* forecasting request volume
* system uptime
* retraining frequency
* drift detection activity

---

# 6. Continuous Integration and Deployment (CI/CD)

The project implements a fully automated **CI/CD pipeline** using **GitHub Actions**.

### CI/CD Workflow

1. **Environment Setup**

   * Install project dependencies
   * Sync datasets and models using DVC

2. **Drift Evaluation**

   * Analyze drift reports
   * Determine if retraining is required

3. **Model Retraining**

   * Execute retraining scripts
   * Generate updated model artifacts

4. **Artifact Versioning**

   * Save models and metrics
   * Push updates to DVC remote storage

5. **Container Build and Deployment**

   * Rebuild Docker image
   * Redeploy FastAPI service

6. **Validation**

   * Test the `/predict` endpoint
   * Verify system metrics
   * Log retraining activity

This automated workflow keeps the forecasting system continuously updated and production-ready.

---

# System Architecture

The RetailForecastML system integrates multiple technologies across the machine learning lifecycle:

| Layer           | Technology                           | Purpose                                  |
| --------------- | ------------------------------------ | ---------------------------------------- |
| Data Processing | Pandas, NumPy, Scikit-learn          | Data preparation and feature engineering |
| Modeling        | XGBoost, RandomForest                | Demand forecasting                       |
| Version Control | DVC, DagsHub                         | Dataset and model versioning             |
| Monitoring      | Prometheus, Grafana                  | System performance tracking              |
| Deployment      | FastAPI, Docker, Hugging Face Spaces | Model serving                            |
| Automation      | GitHub Actions                       | CI/CD pipeline                           |

---

# Conclusion

RetailForecastML demonstrates how modern machine learning systems can be built with **end-to-end MLOps practices**.

By integrating tools such as **Evidently AI, DVC, FastAPI, Prometheus, Grafana, and GitHub Actions**, the project showcases:

* Automated model lifecycle management
* scalable API-based model deployment
* continuous monitoring and drift detection
* reproducible data and model versioning

This architecture provides a practical blueprint for deploying and maintaining reliable demand forecasting systems in real-world retail environments.

---

# License

MIT License

Copyright (c) 2026 Ved Bhatt

