output "cloud_run" {
  description = "The instance of the Cloud Run resources."
  value       = google_cloud_run_service.default
}

output "subscription" {
  description = "The instance of the Subscription resources."
  value       = google_pubsub_subscription.subscription
}