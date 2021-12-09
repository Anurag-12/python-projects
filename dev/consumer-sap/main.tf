provider "google" {
  project                     = var.project_id
}

resource "google_service_account" "service_accounts" {
  account_id   = "ingka-${var.ref}"
  display_name = "Resubmission service account"
  description  = "Resubmission service account"
  project      = var.project_id
}

resource "google_project_iam_member" "project_roles" {
  project  = var.project_id
  role     = "roles/pubsub.publisher"
  member   = "serviceAccount:${google_service_account.service_accounts.email}"
}

resource "google_cloud_run_service" "default" {

  name     = "cloudrun-${var.ref}"
  location = "europe-west1"

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "100"
        "autoscaling.knative.dev/minScale" = "0"
        "run.googleapis.com/client-name"   = "terraform"
      }
    }
    spec {
      containers {
        image = "gcr.io/ingka-dpfwcbt-deploy-dev/resub-publish:1.0.5"
        args  = ["--debug=true"]
        env {
          name  = "GCP_PROJECT"
          value = var.project_id
        }
        env {
          name  = "PUB_SUB_TOPIC"
          value = "baseload_int_s2p_004"
        }
      }
      container_concurrency = "12"
      service_account_name  = google_service_account.service_accounts.email
    }
  }

  metadata {
    annotations = {
      generated-by                      = "terraform"
      "run.googleapis.com/launch-stage" = "BETA"
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
  autogenerate_revision_name = true

/*   lifecycle {
    ignore_changes = [
      metadata.0.annotations,
    ]
  } */

  //depends_on = [google_secret_manager_secret_iam_member.api_username_access, google_secret_manager_secret_iam_member.api_password_access]
}

data "google_iam_policy" "auth_users" {
  binding {
    role    = "roles/run.invoker"
    members = ["serviceAccount:${google_service_account.service_accounts.email}"]
  }
}

resource "google_cloud_run_service_iam_policy" "auth_users_policy" {
  location    = google_cloud_run_service.default.location
  project     = google_cloud_run_service.default.project
  service     = google_cloud_run_service.default.name
  policy_data = data.google_iam_policy.auth_users.policy_data
}

resource "google_pubsub_subscription" "subscription" {
  name  = "ingka-${var.ref}"
  topic = "projects/ingka-dp-sap-dev/topics/cr-demo"

  ack_deadline_seconds = 60

  labels = {
    generated-by = "terraform"
  }

  push_config {
    push_endpoint = google_cloud_run_service.default.status[0].url
    oidc_token {
      service_account_email = google_service_account.service_accounts.email
      audience              = google_cloud_run_service.default.status[0].url
    }
  }

}
