# SemDesLC
Semantically Describing Predictive Models for Interpretable Insights into Lung Cancer Relapse

SemDesLC predicts lung cancer relapse likelihood, providing oncologists with `patient-centric` and `population-centric` analysis. Our approach bridge the gap and fulfill the needs of three different type of users: `KG builders, analysts and consumers`. 
This repository contains all the necessary scripts and instructions to reproduce the experiments.

## Getting Started

Install the pre-requisites for `SemDesLC` framework, in order to facilitate the reproducibility, we run all our experiments in Docker container on a Ubuntu 16.04.6 LTS or newer.
If you don't have Docker (and docker-compose) installed. Please, follow the instructions according to configuration of your machine. 

### Software
* Docker - v19.03.6 or newer 
* docker-compose - v1.26.0 or newer
* Docker Installation
  * Linux: [https://docs.docker.com/desktop/install/linux-install/](https://docs.docker.com/desktop/install/linux-install/)
  * Windows: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)
  * Mac: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)

### Results for KG builder
Navigate to the directory and follow the README inside the directory to execute necessary scripts
```bash
 cd experiments_kg_builder/
```
### Results for KG analysts
To get started, you need to start the containers:
```bash 
docker-compose up -d
```
Then navigate to [`http://localhost:8501/`](http://localhost:8501/). This will start the interface, for the predictive task of relapse likelihood. Login credentials to access the interface are: `Username`: `user123` and `Password`: `roger` (`Note: click twice on login button`).
Interface includes three components Train, Deduce and Explain. 
* Train component: 
  * data quality check
  * predictive modeling of lung cancer relapse
* Deduce component:
  * visualization: Feature Importance Plot, Decision Trees and Decision Tree with SHACL Valdiation
  * SemDesLC KG: Statistical Queries on top of KG
* Explain component: 
  * symbolic learning: mining horn rules, statistical analysis, natural language explanations 
  * patient-centric analysis: This includes the characteristics of individual patients, and explanations
  * population-centric analysis: This includes the influence of sub-population on a predictive model decisions and explanations
