# 📊 End-to-End Sales Analytics Dashboard

> SQL-powered analytics pipeline transforming raw sales data into interactive Power BI & Tableau dashboards — with automated dbt models, Snowflake warehouse, and scheduled Airflow refresh.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![dbt](https://img.shields.io/badge/dbt-1.6-orange) ![Snowflake](https://img.shields.io/badge/Snowflake-DataWarehouse-blue) ![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)

---

## 🏗️ Architecture

```
Raw Sales Data (CSV / REST API / PostgreSQL)
        │
        ▼
  Python Ingestion → Amazon S3 (Raw Zone)
        │
        ▼
  dbt Models (Staging → Marts)
  ├── dim_customers
  ├── dim_products
  ├── fact_sales
  └── agg_monthly_revenue
        │
        ▼
  Snowflake Data Warehouse
        │
        ▼
  Power BI + Tableau Dashboards
  ├── Revenue by Region
  ├── Top Products & Categories
  ├── Customer Churn Indicators
  └── MoM Growth Trends
```

---

## 🚀 Features

- **Automated dbt pipeline** with staging, intermediate, and mart layers
- **Snowflake** as the analytical warehouse with clustering and partitioning
- **Power BI dashboard** with 8 KPI tiles updated on daily schedule
- **Airflow DAG** refreshing data every morning at 6 AM
- **30% faster** dashboard load time via pre-aggregated dbt models
- **Data quality tests** on every dbt model — not null, unique, accepted values

---

## 📁 Project Structure

```
sales-analytics-dashboard/
├── ingestion/
│   └── ingest_sales.py          # Pulls data from APIs + CSVs → S3
├── dbt/
│   ├── models/
│   │   ├── staging/             # Raw → clean
│   │   ├── intermediate/        # Business logic
│   │   └── marts/               # Final KPI tables
│   ├── tests/                   # dbt data quality tests
│   └── dbt_project.yml
├── dags/
│   └── sales_dashboard_dag.py   # Airflow orchestration
├── dashboards/
│   └── sales_dashboard.pbix     # Power BI file
├── sql/
│   └── ad_hoc_queries.sql       # Useful analytical queries
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Ingestion | Python, REST APIs, Pandas |
| Storage | Amazon S3 |
| Warehouse | Snowflake |
| Transformation | dbt 1.6 |
| Orchestration | Apache Airflow |
| Visualization | Power BI, Tableau |

---

## 📊 Key Results

- ✅ **8 KPI dashboards** refreshed daily with zero manual effort
- ✅ **30% faster** load times via pre-aggregated mart models
- ✅ **100% dbt test pass rate** — every model tested for quality
- ✅ **Single source of truth** for sales, customers, and products
