# Week 1: Troubleshooting Database Connectivity on AWS

**Module**: 2 - Source Systems, Data Ingestion, and Pipelines  
**Status**: 🚧 In Progress

---

## 📋 Assignment Overview

This lab focuses on troubleshooting and resolving common issues when connecting to databases on AWS. You'll work with:
- EC2 instances connecting to RDS databases
- Security group configurations
- Network connectivity issues
- Database access and data insertion

---

## 🎯 Learning Objectives

1. Diagnose and fix database connectivity issues from EC2 to RDS
2. Configure security groups for proper network access
3. Enhance RDS security configurations
4. Connect to MySQL and PostgreSQL databases
5. Insert and query data in relational databases

---

## 📁 Files in This Directory

| File/Folder | Description |
|-------------|-------------|
| `C1_W4_Assignment.md` | Official assignment instructions from Coursera |
| `SOLUTION_GUIDE.md` | **⭐ Complete step-by-step solution guide** |
| `QUICK_COMMANDS.md` | **⚡ Quick reference for all commands** |
| `terraform/` | Infrastructure as Code (Terraform modules) |
| `scripts/` | Setup and utility scripts |
| `sql/` | SQL scripts for database operations |
| `data/` | Sample data files |
| `images/` | Architecture diagrams and screenshots |

---

## 🚀 Quick Start

### Option 1: Follow the Solution Guide (Recommended)
```bash
# Open the comprehensive solution guide
open SOLUTION_GUIDE.md
```

The solution guide includes:
- ✅ All commands with explanations
- ✅ Expected outputs
- ✅ Troubleshooting tips
- ✅ Verification steps
- ✅ Common issues and solutions

### Option 2: Use Quick Commands
```bash
# Open the quick reference
open QUICK_COMMANDS.md
```

Perfect for when you just need the commands!

---

## 🏗️ Architecture

This assignment implements:

### Batch Pipeline
```
MySQL (RDS) → AWS Glue ETL → S3 Data Lake → Training Data
```

### Vector Database
```
PostgreSQL (RDS) + pgvector → Store Embeddings → Vector Search
```

### Streaming Pipeline
```
Kinesis Data Streams → Lambda (Model Inference) → Kinesis Firehose → S3 Recommendations
```

---

## 🛠️ Technologies Used

- **AWS Services**:
  - Amazon EC2 (Compute)
  - Amazon RDS (MySQL & PostgreSQL)
  - AWS Glue (ETL)
  - AWS Lambda (Serverless)
  - Amazon Kinesis (Streaming)
  - Amazon S3 (Storage)
  - CloudWatch (Monitoring)

- **Infrastructure**:
  - Terraform (IaC)
  - VPC & Security Groups

- **Databases**:
  - MySQL
  - PostgreSQL with pgvector extension

---

## 📝 Assignment Steps

### Part 1: Batch Pipeline (Steps 1.1 - 1.15)
1. Explore the ratings table in MySQL
2. Deploy AWS Glue ETL job with Terraform
3. Transform data and store in S3

### Part 2: Vector Database (Steps 2.1 - 2.12)
1. Create PostgreSQL database with pgvector
2. Load embeddings from S3
3. Verify vector database setup

### Part 3: Lambda Configuration (Steps 3.1 - 3.3)
1. Configure Lambda environment variables
2. Connect model inference to vector database

### Part 4: Streaming Pipeline (Steps 4.1 - 4.4)
1. Deploy Kinesis infrastructure
2. Verify real-time data flow
3. Monitor Lambda transformations

---

## ⏱️ Time Estimates

- **Part 1**: ~15 minutes (includes 2-3 min Glue job wait)
- **Part 2**: ~20 minutes (includes 7 min DB creation wait)
- **Part 3**: ~5 minutes
- **Part 4**: ~15 minutes (includes 5-10 min streaming wait)

**Total**: ~55 minutes

---

## ✅ Success Criteria

- [ ] Glue job completes successfully
- [ ] Data appears in S3 datalake bucket
- [ ] Vector database created with embeddings loaded
- [ ] Lambda environment variables configured
- [ ] Streaming data flows to recommendations bucket
- [ ] CloudWatch logs show Lambda activity

---

## 🐛 Common Issues

### Issue: Terraform apply fails
**Solution**: Ensure you uncommented the correct lines and saved files

### Issue: Database connection refused
**Solution**: Check security groups allow your IP address

### Issue: Glue job fails
**Solution**: Check CloudWatch logs for detailed error messages

### Issue: No streaming data
**Solution**: Wait 5-10 minutes, Kinesis streams data every ~10 seconds

---

## 📚 Additional Resources

- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Amazon RDS User Guide](https://docs.aws.amazon.com/rds/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [pgvector Extension](https://github.com/pgvector/pgvector)

---

## 🎓 What You'll Learn

By completing this assignment, you'll gain hands-on experience with:
- Building production-grade data pipelines
- Managing AWS infrastructure with Terraform
- Working with vector databases for ML applications
- Implementing real-time streaming architectures
- Troubleshooting cloud connectivity issues

---

## 📊 Grading

This assignment is auto-graded by Coursera. The grader verifies:
- AWS resources are properly created
- Data flows through the pipelines correctly
- Configurations are set up as specified

**Submit** your work via the Coursera platform when complete.

---

**Good luck! 🚀**

For detailed instructions, see `SOLUTION_GUIDE.md`
