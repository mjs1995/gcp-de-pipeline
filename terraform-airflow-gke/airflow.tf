provider "kubernetes" {
  host             = "https://${google_container_cluster.primary.endpoint}"
  token            = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(
    google_container_cluster.primary.master_auth[0].cluster_ca_certificate
  )
}

resource "kubernetes_namespace" "airflow" {
  metadata {
    name = "airflow"
  }
  depends_on = [google_container_cluster.primary]
}

resource "random_string" "webserver_secret_key" {
  length  = 32
  special = false
  upper   = false
  numeric = false
}

resource "kubernetes_secret" "webserver_secret" {
  metadata {
    name      = "my-webserver-secret"
    namespace = kubernetes_namespace.airflow.metadata[0].name
  }

  data = {
    "webserver-secret-key" = "${random_string.webserver_secret_key.result}"
  }

  depends_on = [
    kubernetes_namespace.airflow
  ]
}

provider "helm" {
  kubernetes {
    host                   = "https://${google_container_cluster.primary.endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(
      google_container_cluster.primary.master_auth[0].cluster_ca_certificate
    )
  }
}

resource "helm_release" "airflow" {
  name       = "airflow"
  repository = "https://airflow-helm.github.io/charts"
  chart      = "airflow"
  namespace  = kubernetes_namespace.airflow.metadata[0].name
  timeout    = 600

  set {
    name  = "webserverSecretKeySecretName"
    value = "my-webserver-secret"
  }

  set {
    name  = "dags.folder"
    value = "gs://gke_gcs_bucket/airflow/"
  }

  depends_on = [
    kubernetes_secret.webserver_secret
  ]
}