terraform {
  backend "s3" {
    bucket         = "pomodoro-quest-tfstate-andresantos"
    key            = "core/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "pomodoro-quest-tf-lock"
    encrypt        = true
  }
}
