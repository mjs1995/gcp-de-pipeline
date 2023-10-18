# Terraform Deployment for Apache Airflow on GKE
This repository contains Terraform configurations to deploy Apache Airflow on Google Kubernetes Engine (GKE).

## Structure
- main.tf: Contains the main Terraform configuration, defining the GKE cluster and necessary Google Cloud resources.
- airflow.tf: Specifies Kubernetes and Helm resources required for Airflow, including the Kubernetes namespace for Airflow and the Helm chart for its deployment.

## Prerequisites
- Install Google Cloud SDK and Terraform.
- Set up a GCP project and activate necessary APIs.

## Deployment Steps
Initialization:
- Initialize your Terraform configurations.
- ```shell 
  terraform init
  ```
Planning:
- Review the resources that will be created or modified.
- ```shell
  terraform plan
  ```
Apply:
- Apply the Terraform configurations to create the defined resources on GCP.
- ```shell
  terraform apply
  ```
Access Airflow:
- After successfully applying the configurations, Airflow will be deployed on GKE.
- To access the Airflow web UI, forward the port from the web service pod.
- ```shell
  kubectl port-forward <AIRFLOW-WEB-POD-NAME> 8080:8080 -n airflow
  ```
- Open a browser and navigate to http://localhost:8080 to access the Airflow web interface.

Tear Down:
- If you wish to remove the resources, use the following command.
- ```shell
  terraform destroy
  ```
Manual GKE Cluster Deletion (if needed):
- If the terraform destroy command doesn't remove the GKE cluster as expected, you can delete the cluster manually using the following gcloud command:
- ```shell
  gcloud container clusters delete [CLUSTER_NAME] --region [REGION]
  ```
