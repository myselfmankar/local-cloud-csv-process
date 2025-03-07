📁 Localstack CSV Processing Pipeline

A cloud-based system to process CSV files, extract metadata, and store it using **Localstack** (AWS emulator). Perfect for local development/testing without AWS costs.


## 🎯 Core Deliverables
1. **CSV Processing Pipeline**  
   - Upload CSV → S3 bucket → Trigger Lambda → Extract metadata → Store in DynamoDB → Log notification.
2. **Infrastructure-as-Code**  
   - S3 bucket, Lambda, DynamoDB deployed locally via Docker.

## 🛠️ Tech Stack
- **Localstack** (AWS emulator)
- **Docker** + **Docker Compose**
- **Python** (Lambda runtime)
- **AWS Services**: S3, Lambda, DynamoDB

## 🚀 Features
- Auto-trigger Lambda on CSV upload
- Metadata extraction (row count, column names, file size)
- Persistent storage with DynamoDB
- Error handling for empty/invalid files

## 📦 Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Python 3.9+](https://www.python.org/downloads/)
- [AWS CLI](https://aws.amazon.com/cli/)
- Libraries: `boto3`, `pandas` (auto-installed)



## 🛠️ Setup

### 1. Clone & Prepare
```bash
git clone <your-repo-url>
cd localstack-csv-pipeline

# Install Lambda dependencies
cd lambda
pip install -r requirements.txt -t .  # Installs pandas + boto3
zip -r lambda.zip .  # Package code + dependencies
cd ..
```

## Start Loacalstack
```
docker-compose down -v  # Clean previous state
docker-compose up -d
```

## Verify Resource
```
# Check S3 bucket
aws --endpoint-url=http://localhost:4566 s3 ls

# List DynamoDB tables
aws --endpoint-url=http://localhost:4566 dynamodb list-tables

# Confirm Lambda function exists
aws --endpoint-url=http://localhost:4566 lambda list-functions

```
##  Test the Pipeline
```
# Upload CSV to S3
aws --endpoint-url=http://localhost:4566 s3 cp ./sample.csv s3://csv-bucket/

# Check Metadata in DynamoDB
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name Metadata

# Sample Output
{
  "Items": [{
    "filename": "sample.csv",
    "row_count": 100,
    "column_names": ["id", "name", "age", "city"],
    "upload_timestamp": "2024-01-01 12:00:00"
  }]
}

```
## ⚠️ Known Issues & Workarounds
- **Docker Initialization Timing**:  
  In rare cases, Localstack might not initialize resources automatically due to container readiness timing.  
  **Fix**:  
  ```bash
# Manual setup (if automated init fails)
docker exec localstack awslocal s3 mb s3://csv-bucket
docker exec localstack awslocal dynamodb create-table ...
```
  
## 🛑 Manual Override
```
# Create S3 bucket
docker exec localstack awslocal s3 mb s3://csv-bucket

# Create DynamoDB table
docker exec localstack awslocal dynamodb create-table \
  --table-name Metadata \
  --attribute-definitions AttributeName=filename,AttributeType=S \
  --key-schema AttributeName=filename,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

```
