# Quick Commands Reference

## 🚀 In Coursera Terminal

### Clone Repository
```bash
cd ~
git clone https://github.com/anix-lynch/dlai-c2w4-airflow-pipeline.git
cd dlai-c2w4-airflow-pipeline
```

### Upload Data to S3
```bash
cd data
aws s3 sync work_zone s3://<RAW-DATA-BUCKET>/work_zone/
cd ..
```

### Verify Data Upload
```bash
aws s3 ls s3://<RAW-DATA-BUCKET>/work_zone/ --recursive
```

### Upload DAGs to S3
```bash
cd src/dags
aws s3 cp model_trip_duration_easy_destiny.py s3://<DAGS-BUCKET>/dags/
aws s3 cp model_trip_duration_alitran.py s3://<DAGS-BUCKET>/dags/
aws s3 cp model_trip_duration_to_my_place_ai.py s3://<DAGS-BUCKET>/dags/
```

### Upload All DAGs at Once
```bash
cd src/dags
aws s3 sync . s3://<DAGS-BUCKET>/dags/
```

### Get AWS Console URL
```bash
cat ../.aws/aws_console_url
```

---

## 🔧 If You Need to Modify Code

### Pull Latest Changes
```bash
cd ~/dlai-c2w4-airflow-pipeline
git pull origin main
```

### Re-generate Dynamic DAGs (if template changed)
```bash
cd src/templates
python3 generate_dags.py
cd ../..
```

### Test DAG Syntax Locally
```bash
python3 src/dags/model_trip_duration_easy_destiny.py
```

---

## 🔄 AWS CloudShell (If Airflow Breaks)

### Restart Airflow
```bash
# Copy restart script content from scripts/restart_airflow.sh
nano -c restart_airflow.sh
# Paste content, save (Ctrl+O, Ctrl+X)
bash ./restart_airflow.sh
```

---

## 🖥️ On Your Local Machine

### Push Code Changes to GitHub
```bash
cd /Users/anixlynch/dev/deeplearning-ai-data-engineering-certificate/c2w4_extracted
git add .
git commit -m "Update DAG implementation"
git push origin main
```

### Generate DAGs Locally
```bash
cd src/templates
python3 generate_dags.py
```

---

## 📍 Important Paths

### In Coursera
- Project directory: `~/project` or `/home/coder/project`
- Cloned repo: `~/dlai-c2w4-airflow-pipeline`

### S3 Paths
- Raw data: `s3://<RAW-BUCKET>/work_zone/data_science_project/datasets/<VENDOR>/`
- DAGs: `s3://<DAGS-BUCKET>/dags/`
- GX config: `s3://<DAGS-BUCKET>/dags/gx/`

---

## ⚙️ Airflow UI Steps

1. **Add Variable**
   - Admin → Variables → + → Key: `bucket_name`, Val: `<RAW-BUCKET>` → Save

2. **View DAG**
   - DAGs → Click DAG name → Graph view

3. **Run DAG**
   - Toggle ON → Trigger DAG (▶️ button)

4. **View Logs**
   - Click task in graph → Logs tab

5. **Check XCom**
   - Admin → XComs → Filter by DAG/task

---

## 🎯 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| DAGs not showing | Wait 2 min, refresh, check S3 upload |
| Import error | Check execution_engine parameter |
| Data not found | Verify bucket_name variable in Airflow |
| Permission denied | Check IAM role attached to Airflow |
| Syntax error | Run `python3 <dag>.py` to test |

---

## 📦 Bucket Name Placeholders

**Replace these in all commands:**
- `<RAW-DATA-BUCKET>` → Get from CloudFormation Outputs (RawDataBucket)
- `<DAGS-BUCKET>` → Get from CloudFormation Outputs (DAGsBucket)

**Example:**
```bash
# If RawDataBucket = de-c2w4a1-123456-us-east-1-raw-data
# If DAGsBucket = de-c2w4a1-123456-us-east-1-dags

aws s3 sync work_zone s3://de-c2w4a1-123456-us-east-1-raw-data/work_zone/
aws s3 cp model_trip_duration_easy_destiny.py s3://de-c2w4a1-123456-us-east-1-dags/dags/
```

