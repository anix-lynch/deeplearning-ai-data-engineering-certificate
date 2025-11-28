# Realistic Redeploy Guide After Reboot

## What CAN Be Automated (Terminal Commands) ✅

### 1. Setup & Terraform Deploy
```bash
cd ~/project
source ./scripts/setup.sh
cd terraform
terraform init -reconfigure
terraform apply -auto-approve
```
⏱️ Takes ~10 minutes (Vector DB creation is slow)

### 2. Get Credentials
```bash
terraform output vector_db_master_username
terraform output vector_db_master_password
terraform output vector_db_host
```
📋 **Save these somewhere** - you'll need them!

### 3. Update SQL File (New AWS Account ID)
```bash
# Get new account ID
NEW_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

# Update SQL file
sed -i "s/555833365064/${NEW_ACCOUNT}/g" sql/embeddings.sql
```

### 4. Start Glue Job
```bash
JOB_RUN_ID=$(aws glue start-job-run --job-name de-c1w4-etl-job | jq -r '.JobRunId')
echo "Job Run ID: $JOB_RUN_ID"

# Wait and check status
aws glue get-job-run --job-name de-c1w4-etl-job --run-id $JOB_RUN_ID --output text --query "JobRun.JobRunState"
# Wait until it says "SUCCEEDED" (~2-3 minutes)
```

### 5. Load Embeddings into Vector DB
```bash
# Connect (use password from step 2)
psql --host=<VECTOR_DB_HOST> --username=postgres --password --port=5432

# In psql prompt:
\c postgres;
\i 'sql/embeddings.sql'
\q
```

### 6. Verify Streaming Pipeline
```bash
# Check S3 bucket for files
aws s3 ls s3://de-c1w4-<NEW_ACCOUNT>-us-east-1-recommendations/ --recursive
```

---

## What CANNOT Be Automated (Must Do in AWS Console) ❌

### Step 3.3: Configure Lambda Environment Variables

**This MUST be done manually in AWS Console:**

1. Get AWS Console URL:
   ```bash
   cat ~/.aws/aws_console_url
   ```
   ⚠️ URL expires in 15 minutes - work fast!

2. In AWS Console:
   - Search for **Lambda**
   - Find `de-c1w4-model-inference`
   - Click on it
   - Go to **Configuration** tab → **Environment variables** → **Edit**
   - Add these 3 variables:
     - `VECTOR_DB_HOST` = `<from terraform output>`
     - `VECTOR_DB_USER` = `postgres`
     - `VECTOR_DB_PASSWORD` = `<from terraform output>`
   - Click **Save**

⏱️ Takes ~2 minutes

---

## Complete Workflow After Reboot

### Phase 1: Automated (Terminal)
1. ✅ Setup & Deploy Terraform (~10 min)
2. ✅ Get credentials
3. ✅ Update SQL file with new account ID
4. ✅ Start Glue job (~3 min wait)
5. ✅ Load embeddings (~2 min)

### Phase 2: Manual (AWS Console)
6. ❌ Configure Lambda env vars (~2 min)

### Phase 3: Verify & Submit
7. ✅ Check streaming pipeline works
8. ✅ **Submit assignment** (while AWS is still active!)

---

## Time Estimate

- **Automated steps**: ~15 minutes
- **Manual steps**: ~2 minutes  
- **Total**: ~17 minutes

**Then submit immediately!** You have ~1h 43min left in your 2-hour window.

---

## Pro Tips

1. **Do Lambda config FIRST** after getting credentials (before it expires)
2. **Work fast** - AWS console URL expires in 15 min
3. **Submit as soon as verification works** - don't wait!
4. **Your code files are already correct** - just redeploy

---

## If Something Goes Wrong

Your backup is at:
- `~/Downloads/coursera_backup_extracted/`
- GitHub: `https://github.com/anix-lynch/coursera-take-2`

All your code is correct - you just need to redeploy! 🎯

