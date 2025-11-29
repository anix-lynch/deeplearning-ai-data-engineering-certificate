#!/bin/bash

# 1. Initialize dbt project (skipping prompts)
dbt init classicmodels_modeling --adapter postgres

# 2. Copy configuration and models
cp ./module4/week1/scripts/packages.yml ./classicmodels_modeling/
cp ./module4/week1/scripts/profiles.yml ./classicmodels_modeling/
cp ./module4/week1/scripts/schema.yml ./classicmodels_modeling/models/
cp -r ./module4/week1/models/star_schema ./classicmodels_modeling/models/
cp -r ./module4/week1/models/obt ./classicmodels_modeling/models/

# 3. Install dependencies
cd classicmodels_modeling
dbt deps

echo "✅ Setup complete!"
echo "⚠️  ACTION REQUIRED: Edit profiles.yml with your RDS endpoint."
