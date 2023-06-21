terraform {
    backend "s3" {
        encrypt = true
        bucket = "kookkie-terraform-state"
        region = "eu-central-1"
        key = "terraform/kookkie-terraform-state"
    }
}
