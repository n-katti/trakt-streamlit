# Trakt-Streamlit
An in-progress project split into the following phases:

### Phase 1: - current
Automate entire end-to-end pipeline of ingesting my Trakt (movies/tv) data via API, storing in a SQLite database, and displaying in a Streamlit dashboard. 

### Phase 2:
Push Docker container to AWS -> ECR and ECS and EC2 will be used to run ingestion script daily and to maintain live version of Streamlit dashboard

### Phase 3: 
Create terraform infrastructure for AWS resources

### Phase 4: 
Implement CI/CD workflow using GitHub Actions for all of the above
