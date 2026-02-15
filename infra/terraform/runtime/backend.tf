terraform {
  backend "s3" {
    bucket         = "pomodoro-quest-tfstate-andresantos"
    key            = "runtime/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "pomodoro-quest-tf-lock"
    encrypt        = true
    }
}