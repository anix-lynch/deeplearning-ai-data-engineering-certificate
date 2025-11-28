# 🎯 C1_W4 Assignment Solution Guide
## Building End-to-End Batch and Streaming Pipelines

---

## 📋 **Overview**

This assignment builds:
1. **Batch Pipeline**: AWS Glue ETL → S3 (for ML training data)
2. **Vector Database**: PostgreSQL with pgvector (for embeddings)
3. **Streaming Pipeline**: Kinesis Data Streams → Lambda → S3 (for real-time recommendations)

---

## 🚀 **PART 1: Implementing the Batch Pipeline**

### **Step 1.1-1.5: Explore the Ratings Table**

**1.1** Get the RDS MySQL endpoint:
```bash
aws rds describe-db-instances --db-instance-identifier de-c1w4-rds --output text --query "DBInstances[].Endpoint.Address"
```

**1.2** Connect to MySQL (replace `<MySQLEndpoint>` with output from 1.1):
```bash
mysql --host=<MySQLEndpoint> --user=admin --password=adminpwrd --port=3306
```

**1.3** Use the classicmodels database:
```sql
use classicmodels;
show tables;
```

**1.4** Check the ratings table:
```sql
SELECT * FROM ratings LIMIT 20;
```

**1.5** Exit MySQL:
```bash
exit
```

---

### **Step 1.6-1.15: Deploy Batch Pipeline with Terraform**

**1.6** Setup environment variables:
```bash
source ./scripts/setup.sh
```

**1.7** Navigate to terraform folder:
```bash
cd terraform
```

**1.8** Edit `terraform/main.tf`:
- **Uncomment lines 1-15** (module "etl" section)
- Select lines 1-15, then delete the `# ` at the beginning
- Save with `Cmd+S`

**1.9** Edit `terraform/outputs.tf`:
- **Uncomment lines 2-8** (ETL section)
- Save with `Cmd+S`

**1.10** Initialize Terraform:
```bash
terraform init || echo "$?"
```

**1.11** Deploy resources:
```bash
terraform plan || echo "$?"
terraform apply || echo "$?"
```
- Type `yes` when prompted

**1.12** Get AWS Console URL:
```bash
cat ~/.aws/aws_console_url
```
- Open the link in a browser

**1.13** Start the Glue job:
```bash
aws glue start-job-run --job-name de-c1w4-etl-job | jq -r '.JobRunId'
```
- Save the JobRunId

**1.14** Check job status (replace `<JobRunID>`):
```bash
aws glue get-job-run --job-name de-c1w4-etl-job --run-id <JobRunID> --output text --query "JobRun.JobRunState"
```
- Wait until status is `SUCCEEDED` (2-3 minutes)

**1.15** Verify data in S3:
- Go to AWS Console → S3
- Find bucket: `de-c1w4-<ACCOUNT_ID>-datalake`
- Check folder: `ratings-ml-training/`

---

## 🗄️ **PART 2: Creating & Setting up the Vector Database**

### **Step 2.1-2.5: Create PostgreSQL Vector DB**

**2.2** Edit `terraform/main.tf`:
- **Uncomment lines 17-27** (module "vector_db" section)
- Save with `Cmd+S`

**2.3** Edit `terraform/outputs.tf`:
- **Uncomment lines 11-27** (Vector DB section)
- Save with `Cmd+S`

**2.4** Deploy Vector DB:
```bash
terraform init || echo "$?"
terraform plan || echo "$?"
terraform apply || echo "$?"
```
- Type `yes` when prompted
- **Wait ~7 minutes** for DB creation

**2.5** Get database credentials:
```bash
terraform output vector_db_master_username
terraform output vector_db_master_password
```
- **Save these values** (remove the quotes)

---

### **Step 2.6-2.12: Load Embeddings into Vector DB**

**2.6** Edit `sql/embeddings.sql`:
- Find all instances of `<BUCKET_NAME>` (there are 2)
- Replace with: `de-c1w4-<AWS-ACCOUNT-ID>-us-east-1-ml-artifacts`
- To get your AWS Account ID:
  ```bash
  aws sts get-caller-identity --query Account --output text
  ```
- Or run:
  ```bash
  aws s3 ls | grep ml-artifacts
  ```
- Save with `Cmd+S`

**2.7** Get Vector DB host:
```bash
terraform output vector_db_host
```
- Save this value

**2.8** Connect to PostgreSQL (replace `<VectorDBHost>`):
```bash
psql --host=<VectorDBHost> --username=postgres --password --port=5432
```
- Enter the password from step 2.5

**2.9** Connect to postgres database:
```bash
\c postgres;
```
- Enter the password again

**2.10** Run the embeddings SQL script:
```bash
\i '../sql/embeddings.sql'
```

**2.11** Verify tables were created:
```bash
\dt *.*
```
- Press `Q` to quit

**2.12** Exit PostgreSQL:
```bash
\q
```

---

## 🔗 **PART 3: Connecting the Model to Vector Database**

### **Step 3.1-3.3: Configure Lambda Environment Variables**

**3.1-3.2** Get Vector DB endpoint:
- Go to AWS Console → RDS → Databases
- Click on `de-c1w4-vector-db`
- Copy the endpoint from "Connectivity & Security" tab
- Format: `de-c1w4-vector-db.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com`

**3.3** Configure Lambda function:
- Go to AWS Console → Lambda
- Find function: `de-c1w4-model-inference`
- Click on it → Configuration tab → Environment variables → Edit
- Set these values:
  - `VECTOR_DB_HOST`: (endpoint from step 3.2)
  - `VECTOR_DB_PASSWORD`: (from step 2.5)
  - `VECTOR_DB_USER`: (from step 2.5)
- Click **Save**

---

## 🌊 **PART 4: Implementing the Streaming Pipeline**

### **Step 4.1-4.4: Deploy Streaming Infrastructure**

**4.1** Edit `terraform/main.tf`:
- **Uncomment lines 29-39** (module "streaming_inference" section)
- Save with `Cmd+S`

**4.2** Edit `terraform/outputs.tf`:
- **Uncomment lines 30-32** (streaming inference section)
- Save with `Cmd+S`

**4.3** Deploy streaming resources:
```bash
terraform init || echo "$?"
terraform plan || echo "$?"
terraform apply || echo "$?"
```
- Type `yes` when prompted

**4.4** Verify streaming pipeline:
- Go to AWS Console → S3
- Find bucket: `de-c1w4-<ACCOUNT_ID>-recommendations`
- **Wait 5 minutes** then refresh
- You should see data appearing in folders: `year/month/day/hour/`

**Monitor Lambda logs:**
- Go to AWS Console → Lambda
- Find: `de-c1w4-transformation-lambda`
- Click Monitor tab → View CloudWatch Logs
- Wait 1-2 minutes if you see "Log group does not exist" error

---

## ✅ **Verification Checklist**

- [ ] Glue job completed successfully
- [ ] Data appears in `de-c1w4-<ACCOUNT_ID>-datalake` bucket
- [ ] Vector DB created and embeddings loaded
- [ ] Lambda environment variables configured
- [ ] Streaming data appears in recommendations bucket
- [ ] CloudWatch logs show Lambda executions

---

## 🎓 **Submit Your Work**

Once all steps are complete:
1. Click **Submit assignment** in the top right corner of Coursera
2. The grader will verify your AWS resources

---

## 🐛 **Common Issues & Solutions**

### Issue 1: Terraform apply fails
**Solution**: Check that you uncommented the correct lines and saved the files

### Issue 2: Can't connect to databases
**Solution**: Verify security groups allow your IP address

### Issue 3: Glue job fails
**Solution**: Check CloudWatch logs for the Glue job

### Issue 4: No data in S3 recommendations bucket
**Solution**: Wait 5-10 minutes, Kinesis streams data every ~10 seconds

### Issue 5: Lambda environment variables not saving
**Solution**: Make sure to click "Save" after editing

---

## 📚 **Key Concepts Learned**

1. **Batch Processing**: AWS Glue ETL for transforming data
2. **Vector Databases**: PostgreSQL with pgvector for similarity search
3. **Streaming**: Kinesis Data Streams + Firehose for real-time data
4. **Infrastructure as Code**: Terraform for AWS resource management
5. **Serverless Computing**: Lambda functions for data transformation

---

## 🎉 **Congratulations!**

You've built an end-to-end data engineering pipeline with:
- Batch processing for ML training data
- Vector database for embeddings
- Real-time streaming for recommendations

This is production-grade architecture used by companies like Netflix, Amazon, and Spotify!
