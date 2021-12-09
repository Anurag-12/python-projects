terraform {
  backend "gcs" {
    bucket  = "PIPELINE_NAME-DIR-ENVIRONMENT-tfstate"
    prefix  = "state"
  }
}