# Job Market Intelligence Pipeline

An end-to-end modern ELT data engineering pipeline that ingests job posting data from public APIs, stores raw data in Google Cloud Storage, transforms data with dbt, orchestrates workflows using Airflow, and builds analytics-ready star schema models in BigQuery.

### Technologies
Python • SQL • BigQuery • dbt • Airflow • Docker • Google Cloud Storage

### Key Features
- Incremental ingestion
- Medallion architecture
- Star schema modeling
- dbt data quality tests
- Airflow DAG orchestration
- Dockerized local environment

---

# Project Goals

This project was designed to simulate a modern analytics engineering workflow while remaining:
- beginner-friendly
- low-cost / free-tier compatible
- production-oriented
- fully containerized
- interview-ready

The pipeline demonstrates:
- ELT architecture
- Medallion data modeling
- incremental ingestion
- orchestration with Airflow
- transformations with dbt
- data quality testing
- dimensional/star schema modeling
- Docker-based reproducibility
- cloud warehousing with BigQuery

---

# Architecture

```text
                ┌─────────────────────┐
                │   Job Posting API   │
                │   RemoteOK / API    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Python Ingestion    │
                │ Incremental Loads   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ GCS Bronze Layer    │
                │ Raw JSON Storage    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ BigQuery Bronze     │
                │ Raw Tables          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ dbt Silver Models   │
                │ Cleaning / Standard │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ dbt Gold Models     │
                │ Star Schema Marts   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Dashboards / SQL    │
                └─────────────────────┘
```

---

# Tech Stack

| Layer | Tool |
|---|---|
| Programming | Python |
| SQL Transformations | dbt Core |
| Orchestration | Apache Airflow |
| Warehouse | Google BigQuery |
| Cloud Storage | Google Cloud Storage |
| Containerization | Docker |
| Dashboarding | Looker Studio |
| Data Source | RemoteOK API |

---

# Medallion Architecture

The project follows a Medallion architecture pattern.

## Bronze Layer
Raw immutable ingestion layer.

Responsibilities:
- ingest raw API responses
- preserve source fidelity
- partition by ingestion date
- maintain append-only history

Example:
```text
bronze.jobs_raw
```

---

## Silver Layer
Cleaned and standardized data layer.

Responsibilities:
- deduplication
- null handling
- type casting
- standardization
- enrichment
- skill extraction

Example:
```text
silver.jobs_cleaned
silver.skills_extracted
```

---

## Gold Layer
Business-ready analytics layer.

Responsibilities:
- dimensional modeling
- star schema construction
- KPI generation
- dashboard optimization

Example:
```text
gold.fact_job_postings
gold.dim_company
gold.dim_skill
gold.dim_date
```

---

# Data Model

## Fact Table

### fact_job_postings

Contains job posting metrics and foreign keys.

Measures:
- salary
- posting_count

Foreign Keys:
- company_id
- skill_id
- date_id
- location_id

---

## Dimension Tables

### dim_company
- company_id
- company_name
- industry

### dim_skill
- skill_id
- skill_name
- category

### dim_date
- date_id
- month
- quarter
- year

### dim_location
- location_id
- city
- country

---

# Incremental Ingestion

The pipeline uses incremental loading to avoid reprocessing historical data daily.

Benefits:
- lower warehouse cost
- faster pipeline execution
- scalable architecture
- realistic production patterns

Example dbt incremental model:

```sql
{{ config(
    materialized='incremental',
    unique_key='job_id'
) }}

SELECT *
FROM {{ source('bronze', 'jobs_raw') }}

{% if is_incremental() %}
WHERE posted_date >
(
    SELECT MAX(posted_date)
    FROM {{ this }}
)
{% endif %}
```

---

# Airflow DAG

The pipeline is orchestrated with Apache Airflow and scheduled to run daily.

## DAG Flow

```text
extract_api_data
    ↓
upload_to_gcs
    ↓
load_bronze_bigquery
    ↓
run_dbt_silver
    ↓
run_dbt_gold
    ↓
run_dbt_tests
```

---

# Data Quality Testing

dbt tests validate data quality automatically.

Implemented tests:
- unique
- not_null
- relationships

Example:

```yaml
models:
  - name: dim_company
    columns:
      - name: company_id
        tests:
          - unique
          - not_null
```

---

# Dockerized Environment

The entire stack is containerized using Docker Compose.

Services:
- airflow-webserver
- airflow-scheduler
- postgres
- dbt

Benefits:
- reproducibility
- environment consistency
- simplified onboarding
- portable local development

---

# Project Structure

```text
job-market-pipeline/
│
├── airflow/
│   ├── dags/
│   └── logs/
│
├── ingestion/
│
├── dbt/
│
├── docker/
│
├── data/
│
├── docs/
│
├── scripts/
│
├── tests/
│
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Example Business Questions

The warehouse supports analytics such as:
- Which skills are most in-demand?
- How has demand for dbt changed over time?
- Which companies hire most frequently?
- What skills correlate with higher salaries?
- Which regions have the highest DE hiring activity?
- Remote vs onsite hiring trends

---

# Cost Optimization Strategy

This project was intentionally designed to remain free or near-zero cost.

## BigQuery Sandbox
Uses the BigQuery free sandbox tier:
- no billing required
- free query allowance
- sufficient for portfolio-scale workloads

## Small Incremental Loads
Only new job postings are processed daily.

## Partitioned Tables
Tables partitioned by ingestion/posted date:
- reduced query scan cost
- improved performance

## Local Orchestration
Airflow and dbt run locally via Docker rather than cloud VMs.

---

# Future Improvements

Potential future enhancements:
- streaming ingestion
- Kafka integration
- Terraform infrastructure provisioning
- CI/CD pipelines
- Great Expectations tests
- sentiment analysis on job descriptions
- Spark transformations
- ML salary prediction models

---

# Setup

## 1. Clone Repository

```bash
git clone <repo-url>
cd job-market-pipeline
```

---

## 2. Configure Environment Variables

Create a `.env` file:

```env
GCP_PROJECT_ID=your-project-id
BIGQUERY_DATASET=job_market
GCS_BUCKET=your-bucket-name
```

---

## 3. Start Docker Environment

```bash
docker compose up
```

---

## 4. Access Airflow

```text
http://localhost:8080
```

---

## 5. Run dbt Models

```bash
dbt run
dbt test
```

---

# Key Engineering Concepts Demonstrated

This project demonstrates:
- ELT pipeline design
- orchestration
- dimensional modeling
- incremental processing
- analytics engineering
- data quality testing
- cloud warehousing
- containerization
- production-style architecture

---

# Learning Outcomes

This project reinforces:
- SQL engineering
- dbt workflows
- orchestration concepts
- cloud fundamentals
- dimensional modeling
- data quality engineering
- production-style development practices

---

# Acknowledgements

Data Source:
- RemoteOK API

Core Technologies:
- Apache Airflow
- dbt Core
- Google BigQuery
- Docker
- Google Cloud Storage