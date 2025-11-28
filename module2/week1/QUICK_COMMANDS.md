# ⚡ Quick Command Reference - C1_W4 Assignment

## 🔧 **Setup Commands**
```bash
# Setup environment
source ./scripts/setup.sh

# Navigate to terraform
cd terraform

# Get AWS Account ID
aws sts get-caller-identity --query Account --output text

# Get AWS Console URL
cat ~/.aws/aws_console_url
```

---

## 📊 **Part 1: Batch Pipeline**

### MySQL Commands
```bash
# Get RDS endpoint
aws rds describe-db-instances --db-instance-identifier de-c1w4-rds --output text --query "DBInstances[].Endpoint.Address"

# Connect to MySQL
mysql --host=<MySQLEndpoint> --user=admin --password=adminpwrd --port=3306

# Inside MySQL:
use classicmodels;
show tables;
SELECT * FROM ratings LIMIT 20;
exit
```

### Terraform - Batch Pipeline
```bash
# Edit files:
# - terraform/main.tf (uncomment lines 1-15)
# - terraform/outputs.tf (uncomment lines 2-8)

terraform init || echo "$?"
terraform plan || echo "$?"
terraform apply || echo "$?"  # Type 'yes'
```

### Glue Job
```bash
# Start job
aws glue start-job-run --job-name de-c1w4-etl-job | jq -r '.JobRunId'

# Check status (replace <JobRunID>)
aws glue get-job-run --job-name de-c1w4-etl-job --run-id <JobRunID> --output text --query "JobRun.JobRunState"
```

---

## 🗄️ **Part 2: Vector Database**

### Terraform - Vector DB
```bash
# Edit files:
# - terraform/main.tf (uncomment lines 17-27)
# - terraform/outputs.tf (uncomment lines 11-27)

terraform init || echo "$?"
terraform plan || echo "$?"
terraform apply || echo "$?"  # Type 'yes', wait ~7 min
```

### Get Credentials
```bash
terraform output vector_db_master_username
terraform output vector_db_master_password
terraform output vector_db_host
```

### PostgreSQL Commands
```bash
# Edit sql/embeddings.sql first!
# Replace <BUCKET_NAME> with: de-c1w4-<ACCOUNT_ID>-us-east-1-ml-artifacts

# Find bucket name
aws s3 ls | grep ml-artifacts

# Connect to PostgreSQL
psql --host=<VectorDBHost> --username=postgres --password --port=5432

# Inside PostgreSQL:
\c postgres;
\i '../sql/embeddings.sql'
\dt *.*
\q
```

---

## 🔗 **Part 3: Lambda Configuration**

**Manual Steps in AWS Console:**
1. Go to RDS → Databases → `de-c1w4-vector-db` → Copy endpoint
2. Go to Lambda → `de-c1w4-model-inference` → Configuration → Environment variables → Edit
3. Set:
   - `VECTOR_DB_HOST`: <endpoint>
   - `VECTOR_DB_PASSWORD`: <password from terraform output>
   - `VECTOR_DB_USER`: <username from terraform output>
4. Click Save

---

## 🌊 **Part 4: Streaming Pipeline**

### Terraform - Streaming
```bash
# Edit files:
# - terraform/main.tf (uncomment lines 29-39)
# - terraform/outputs.tf (uncomment lines 30-32)

terraform init || echo "$?"
terraform plan || echo "$?"
terraform apply || echo "$?"  # Type 'yes'
```

### Verify
```bash
# Check S3 bucket in AWS Console:
# de-c1w4-<ACCOUNT_ID>-recommendations

# Check Lambda logs:
# Lambda → de-c1w4-transformation-lambda → Monitor → View CloudWatch Logs
```

---

## 🎯 **Files to Edit**

| File | Lines to Uncomment | Section |
|------|-------------------|---------|
| `terraform/main.tf` | 1-15 | module "etl" |
| `terraform/outputs.tf` | 2-8 | ETL outputs |
| `terraform/main.tf` | 17-27 | module "vector_db" |
| `terraform/outputs.tf` | 11-27 | Vector DB outputs |
| `sql/embeddings.sql` | Replace `<BUCKET_NAME>` (2 places) | S3 bucket name |
| `terraform/main.tf` | 29-39 | module "streaming_inference" |
| `terraform/outputs.tf` | 30-32 | Streaming outputs |

---

## ⏱️ **Expected Wait Times**

- Glue Job: **2-3 minutes**
- Vector DB Creation: **~7 minutes**
- Streaming Data to Appear: **5-10 minutes**

---

## 🚨 **Important Notes**

1. **Always save files** after editing (`Cmd+S`)
2. **Type 'yes'** when terraform prompts
3. **Remove quotes** from terraform outputs when using credentials
4. **AWS Console URL expires** every 15 minutes (re-run command)
5. **Wait for resources** to be created before proceeding

---

## ✅ **Success Indicators**

- ✅ Glue job status: `SUCCEEDED`
- ✅ Data in S3 datalake bucket
- ✅ Tables created in Vector DB
- ✅ Lambda env vars configured
- ✅ Data flowing to recommendations bucket
- ✅ CloudWatch logs showing activity
