# Cursor Agent Handover Guide - Coursera Data Engineering Cert

## Context: What You're Helping With

User is completing **DeepLearning.AI Data Engineering Professional Certificate** on Coursera.

**Current Status:**
- ✅ Completed Week 4 Assignment (got 0% due to AWS session expiry, but work was correct)
- 🔄 Need help with remaining modules/assignments
- ⚠️ **Critical**: AWS sessions expire after 2 hours - must work fast!

---

## Environment Setup

### Coursera Lab Environment
- **Platform**: Browser-based VS Code (code-server)
- **Terminal**: Linux shell (`/bin/bash`)
- **User**: `coder@<container-id>:~/project$`
- **Working Directory**: `/home/coder/project` or `~/project`
- **AWS**: Temporary account created per lab session (expires in 2 hours)

### Local Mac Environment
- **User**: `anixlynch`
- **Home**: `/Users/anixlynch`
- **Downloads**: `~/Downloads`
- **GitHub**: `anix-lynch` (username)
- **GitHub Token**: Available via `gh auth token` (if `gh` CLI is installed)

---

## Key Workflow Patterns

### 1. File Backup Strategy (CRITICAL)

**Problem**: Can't download files directly from Coursera browser terminal.

**Solution**: Git bridge workflow (push from Coursera → pull on Mac)

#### Step-by-Step Backup Process:

**A. In Coursera Terminal:**
```bash
# 1. Create zip backup
cd ~/project
zip -r project_backup_$(date +%Y%m%d_%H%M%S).zip .

# 2. If zip > 100MB, split it (GitHub limit)
split -b 90M project_backup_*.zip project_backup_part_

# 3. Initialize git (if not already)
git init
git config --global user.email "anix-lynch@users.noreply.github.com"
git config --global user.name "anix-lynch"
git config --global --add safe.directory /home/coder/project

# 4. Add and commit
git add project_backup_part_*  # or project_backup_*.zip if < 100MB
git commit -m "Backup: $(date +%Y%m%d_%H%M%S)"

# 5. Create repo and push (from Mac side - see below)
# OR push to existing repo:
git remote add origin https://github.com/anix-lynch/<repo-name>.git
git branch -M main
git push -u origin main
```

**B. On Mac (Agent Side):**
```bash
# 1. Create GitHub repo
gh repo create <repo-name> --private --description "Coursera assignment backup"

# 2. Get token for user
gh auth token
# Returns: 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 (may change)

# 3. User will enter credentials in Coursera popup:
#    Username: anix-lynch
#    Password: <token from step 2>
```

**C. Download on Mac:**
```bash
cd ~/Downloads
git clone https://github.com/anix-lynch/<repo-name>.git
cd <repo-name>

# If split into chunks, rejoin:
cat project_backup_part_* > project_backup_restored.zip

# Extract:
unzip project_backup_restored.zip -d ../coursera_backup_extracted/
```

---

### 2. GitHub File Size Limits

- **Hard limit**: 100MB per file
- **Warning threshold**: 50MB
- **Solution for large files**:
  - Split: `split -b 90M file.zip file_part_`
  - Rejoin: `cat file_part_* > file.zip`

**Note**: Git LFS is NOT available in Coursera environment.

---

### 3. AWS Session Management

**Critical Constraints:**
- AWS sessions expire after **2 hours**
- After expiry: Can access files, but **cannot use AWS resources**
- Autograder needs **active AWS resources** to verify work
- Must submit **while AWS is still active**

**Reboot Process:**
1. Click **?** icon (top right in Coursera VS Code)
2. Click **"Reboot"** in Lab Help dialog
3. Wait **~10 minutes** for lab to restart
4. Get fresh 2-hour AWS session
5. Files are preserved, but AWS resources are **new** (need to redeploy)

---

### 4. Terraform Workflow Pattern

**Common Pattern:**
```bash
# 1. Setup environment
cd ~/project
source ./scripts/setup.sh

# 2. Navigate to terraform
cd terraform

# 3. Initialize (if first time or backend changed)
terraform init -reconfigure

# 4. Apply
terraform apply -auto-approve
# Takes ~10 minutes (Vector DB creation is slow)

# 5. Get outputs
terraform output <output_name>
```

**Common Issues:**
- Backend changed → need `-reconfigure` flag
- Safe directory error → `git config --global --add safe.directory /home/coder/project`
- Files need uncommenting → check assignment instructions

---

### 5. Manual AWS Console Steps

**Cannot be automated** - must be done in browser:
- Lambda environment variable configuration
- Some resource verification steps

**Get Console URL:**
```bash
cat ~/.aws/aws_console_url
```
⚠️ URL expires in 15 minutes - work fast!

---

## Assignment-Specific Patterns

### Week 4 Assignment (Completed)
- **Files to modify**: `terraform/main.tf`, `terraform/outputs.tf`, `sql/embeddings.sql`
- **Key steps**: Uncomment modules, update bucket names, deploy, configure Lambda
- **Backup location**: `~/Downloads/coursera_backup_extracted/`

### Future Assignments
- Check assignment markdown file for specific requirements
- Usually involves Terraform, AWS services, SQL scripts
- Pattern: Uncomment code → Deploy → Configure → Verify → Submit

---

## Communication Style

**User Preferences:**
- ✅ Execute, don't explain (unless critical)
- ✅ Minimal CTAs (only tell user what they MUST do)
- ✅ Don't create .md files unless explicitly asked
- ✅ Work directly in local directories (not sandbox)
- ✅ Keep it concise

**Terminal Commands:**
- Always specify if command is for **Coursera terminal** or **Mac terminal**
- Use `cd ~/project` for Coursera
- Use `cd ~/Downloads` for Mac downloads

---

## Backup Locations Reference

### Current Backups:
- **Extracted**: `~/Downloads/coursera_backup_extracted/`
- **GitHub**: `https://github.com/anix-lynch/coursera-take-2`
- **Local zip**: `~/Downloads/coursera-take-2/project_backup_20251127_230048.zip`

### Backup Naming Convention:
- Format: `project_backup_YYYYMMDD_HHMMSS.zip`
- Example: `project_backup_20251127_230048.zip`

---

## Common Commands Reference

### Coursera Terminal:
```bash
# Get AWS account ID
aws sts get-caller-identity --query Account --output text

# Get AWS console URL
cat ~/.aws/aws_console_url

# Check file sizes
ls -lh

# Split large files
split -b 90M file.zip file_part_

# Git setup
git config --global user.email "anix-lynch@users.noreply.github.com"
git config --global user.name "anix-lynch"
```

### Mac Terminal:
```bash
# Create GitHub repo
gh repo create <name> --private

# Get GitHub token
gh auth token

# Clone and rejoin chunks
git clone https://github.com/anix-lynch/<repo>.git
cat file_part_* > file.zip
```

---

## Troubleshooting

### Git Issues:
- **"dubious ownership"** → `git config --global --add safe.directory /home/coder/project`
- **"not a git repository"** → `git init` first
- **Authentication failed** → Use GitHub token, not password

### File Size Issues:
- **> 100MB** → Split into chunks
- **Git LFS not available** → Use split method

### AWS Issues:
- **Session expired** → Reboot lab
- **Resources gone** → Redeploy with Terraform
- **Console URL expired** → Run `cat ~/.aws/aws_console_url` again

---

## Success Criteria

**Assignment is complete when:**
1. ✅ All code files modified correctly
2. ✅ Terraform deployed successfully
3. ✅ All manual AWS Console steps done
4. ✅ Verification steps pass
5. ✅ **Submitted while AWS session is active**

**Critical**: Submit **before** AWS expires, or autograder can't verify!

---

## Quick Start Checklist for New Assignment

1. ✅ Read assignment markdown file
2. ✅ Identify files to modify
3. ✅ Make changes
4. ✅ Create backup (zip + GitHub)
5. ✅ Deploy with Terraform
6. ✅ Complete manual AWS steps
7. ✅ Verify everything works
8. ✅ **Submit immediately** (while AWS active!)

---

## Notes

- User has migraine issues - keep instructions clear and concise
- User is close to completing cert - be encouraging
- Previous work was correct, just timing issue with AWS expiry
- All code patterns are established - mostly redeploying same patterns

**You've got this! The user is 95% done, just needs help with remaining modules.** 🚀

