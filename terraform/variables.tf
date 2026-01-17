variable "aws_region" {
  description = "AWS region (used by LocalStack)"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "S3 bucket name for ETL pipeline"
  type        = string
}
