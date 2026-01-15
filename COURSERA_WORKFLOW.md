# Coursera Assignment Workflow

## Core Principle
Test locally → Push to GitHub → Pull in Coursera. Never ask user to run local commands.

## Workflow Steps

### 1. Complete Assignment Locally
```bash
cd /path/to/assignment
# Edit notebook/code files
# Complete all exercises
```

### 2. Test Everything (Critical)
```bash
# Create venv if needed
python3 -m venv .venv
source .venv/bin/activate
pip install jupyter nbconvert python-dotenv requests [other-deps]

# Install kernel
python -m ipykernel install --user --name=venv_assignment

# Execute ALL cells - verify no errors
jupyter nbconvert --to notebook --execute Assignment.ipynb \
  --output Assignment_tested.ipynb \
  --ExecutePreprocessor.kernel_name=venv_assignment \
  --ExecutePreprocessor.timeout=300

# Replace original with tested version
mv Assignment_tested.ipynb Assignment.ipynb
```

### 3. Handle Credentials
```bash
# Create template without real credentials
echo "CLIENT_ID=YOUR_CLIENT_ID
CLIENT_SECRET=YOUR_CLIENT_SECRET" > src/env.template

# Add to .gitignore
echo "src/env" >> .gitignore

# Clear credentials in tracked file
echo "CLIENT_ID=
CLIENT_SECRET=" > src/env

# Commit
git add .gitignore src/env.template src/env
git commit -m "Add env template, protect credentials"
```

### 4. Push to GitHub
```bash
git add Assignment.ipynb [other-files]
git commit -m "Complete assignment - tested all cells"
git push
```

### 5. Provide Coursera Commands
User runs in Coursera terminal:
```bash
cd /home/coder/project

# Download from GitHub
curl -o Assignment.ipynb https://raw.githubusercontent.com/USER/REPO/main/path/Assignment.ipynb

# Add credentials
cat > src/env << 'EOF'
CLIENT_ID=actual_value
CLIENT_SECRET=actual_value
EOF
```

## Key Rules

1. **ALWAYS test notebook execution locally first**
2. **NEVER push real credentials to GitHub**
3. **ALWAYS use required_permissions: ["all"] for terminal commands**
4. **User only runs commands in Coursera terminal**
5. **Verify all cells execute without errors before pushing**

## Common Issues

### Import Errors
- Install all dependencies in venv before testing
- Check notebook kernel matches venv kernel

### Credential Errors
- Use env.template for GitHub
- Provide actual credentials only in Coursera commands

### Cell Execution Fails
- Fix errors locally
- Re-test entire notebook
- Push only after successful execution

## Pre-Submission Checklist

### Local Testing
```bash
cd /path/to/assignment
source .venv/bin/activate

# Test notebook execution (all cells must pass)
jupyter nbconvert --to notebook --execute Assignment.ipynb \
  --output test_output.ipynb \
  --ExecutePreprocessor.kernel_name=venv_assignment \
  --ExecutePreprocessor.timeout=300

# Verify no errors in output
echo "✅ All cells executed successfully"

# Test Python scripts if any
cd src
python main.py
# Verify output files created

# Clean up test files
rm test_output.ipynb
```

### Verification Steps
1. ✅ All notebook cells execute without errors
2. ✅ All exercises completed (check for `### START CODE HERE ###` sections)
3. ✅ Credentials removed from git (check `git diff`)
4. ✅ Python scripts tested (if applicable)
5. ✅ Output files generated correctly
6. ✅ No hardcoded paths (use relative paths)

### Ready to Submit
```bash
# Final push
git add -A
git commit -m "Ready for Coursera submission"
git push

# Provide Coursera commands to user
echo "Run in Coursera terminal:"
echo "curl -o Assignment.ipynb https://raw.githubusercontent.com/USER/REPO/main/path/Assignment.ipynb"
```

## File Structure
```
assignment/
├── Assignment.ipynb          # Tested, working notebook
├── src/
│   ├── env.template         # Tracked in git
│   ├── env                  # Gitignored, empty in repo
│   └── *.py                 # Python modules
└── .venv/                   # Local testing only
```
