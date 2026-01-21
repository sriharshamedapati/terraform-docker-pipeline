# Automated Data Pipeline Infrastructure with Terraform, Docker, and LocalStack

A fully automated DataOps CI pipeline that provisions cloud infrastructure using Terraform, simulates AWS services with LocalStack, runs a containerized ETL process using Docker, and validates data processing inside GitHub Actions.

This project demonstrates how modern data teams can build, test, and validate cloud-based data pipelines without using real AWS resources.

---

## What This Project Does

On every push to the `main` branch, the pipeline automatically:

1. Starts a GitHub Actions runner (Linux VM)
2. Launches LocalStack (AWS cloud emulator) using Docker
3. Uses Terraform to provision an S3 bucket inside LocalStack
4. Uploads a raw CSV file to the bucket
5. Builds a Docker-based ETL application
6. Runs the ETL container to:

   * Read raw data from S3
   * Transform the data
   * Save the processed output back to S3
7. Verifies that the processed file exists

If any step fails, the pipeline stops. If all steps pass, the pipeline completes successfully.

---

## Architecture Overview

```text
GitHub Push
    ↓
GitHub Actions (CI Runner)
    ↓
LocalStack (AWS Emulator - Docker)
    ↓
Terraform → Creates S3 Bucket
    ↓
Raw CSV Uploaded to S3
    ↓
Docker ETL Container Runs
    ↓
Processed CSV Saved to S3
    ↓
Validation Step
```

---

## Technology Stack

| Tool                   | Purpose                     |
| ---------------------- | --------------------------- |
| Terraform              | Infrastructure as Code      |
| Docker                 | Containerized ETL execution |
| LocalStack             | AWS cloud emulation         |
| GitHub Actions         | CI/CD automation            |
| Python (Pandas, Boto3) | ETL logic                   |
| AWS CLI                | S3 interaction              |

---

## Project Structure

```text
terraform-docker-pipeline/
│
├── .github/workflows/
│   └── pipeline.yml
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── etl/
│   ├── Dockerfile
│   ├── etl.py
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

## ETL Flow

### Extract

Reads a CSV file from:

```
s3://<bucket-name>/raw/input.csv
```

### Transform

* Filters invalid or empty rows
* Adds a `row_length` column for validation

### Load

Saves the processed file to:

```
s3://<bucket-name>/processed/output.csv
```

---

## Running Locally

### Start LocalStack

```bash
docker-compose up -d
```

### Initialize Infrastructure

```bash
cd terraform
terraform init
terraform apply -var="bucket_name=ci-test-bucket" -auto-approve
```

### Upload Test Data

```bash
echo "id,name" > test.csv
echo "1,Alice" >> test.csv
echo "2,Bob" >> test.csv

aws --endpoint-url=http://localhost:4566 s3 cp test.csv s3://ci-test-bucket/raw/input.csv
```

### Build and Run ETL

```bash
docker build -t etl-app ./etl

docker run --rm \
  -e AWS_ENDPOINT_URL=http://localhost:4566 \
  -e S3_BUCKET_NAME=ci-test-bucket \
  -e AWS_ACCESS_KEY_ID=test \
  -e AWS_SECRET_ACCESS_KEY=test \
  etl-app
```

### Verify Output

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://ci-test-bucket/processed/
```

---

## CI Pipeline

The pipeline runs automatically on:

```
Push to main branch
```

Workflow definition:

```
.github/workflows/pipeline.yml
```

---

## Why This Project Matters

This project demonstrates how to:

* Automate cloud infrastructure provisioning
* Test AWS-based pipelines locally without cloud costs
* Run containerized ETL workloads in CI
* Integrate DevOps and Data Engineering practices

---

## Future Improvements

* Multi-environment support (dev, test, prod)
* Schema validation for incoming data
* Automated ETL unit testing
* Container registry integration
* Monitoring and logging integration
