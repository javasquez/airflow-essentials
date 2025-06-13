# 🚀 Orchestration with Airflow – Essential DAG Examples

This project demonstrates how to orchestrate data pipelines using **Apache Airflow 2.11.0**, focusing on practical and foundational use cases. It runs using the **official Docker Compose setup**, and includes integration with an **external SQL Server database**, plus examples using `pandas`, XComs, Bash scripts, and more.

---

## 📦 Tech Stack

| Component           | Technology                       |
|---------------------|----------------------------------|
| Orchestrator        | Apache Airflow 2.11.0            |
| Executor            | CeleryExecutor                   |
| Deployment          | Docker Compose (official)        |
| Metadata Database   | PostgreSQL (default in Docker)   |
| External Database   | Microsoft SQL Server (via RDS)   |
| Language            | Python 3.12                      |
| Airflow Providers   | `apache-airflow-providers-microsoft-mssql` |

---

## 📁 Project Structure

ORCHESTRATION-WITH-AIRFLOW/
│
├── config/                          # Custom configuration files (optional)
│
├── dags/                            # All DAG definitions
│   ├── bash_scripts/                # Bash scripts used in BashOperator
│   │   └── taskA.sh
│   ├── dag_python_branching_catchup.py      # DAG with catchup and weekday branching
│   ├── dag_python_branching_operator.py     # DAG using BranchPythonOperator + Variable
│   ├── dag_python_branching_taskgroup.py    # DAG using TaskGroup to group related tasks
│   ├── dag_python_database.py               # DAG that interacts with external SQL Server
│   ├── dag_python_operator.py               # Basic PythonOperator example with kwargs
│   ├── dag_python_pipeline.py               # pandas pipeline: read, clean, group
│   ├── dag_xcoms.py                         # DAG demonstrating XCom usage
│   ├── dag.py                               # Generic starter DAG
│   └── modern_dag.py                        # DAG with context manager and Bash script
│
├── data/                           # Local input/output data for the DAGs
│   ├── inputs/
│   │   └── insurance.csv            # Source CSV used in pandas pipeline
│   └── outputs/
│       └── smokers.csv             # Output generated from pipeline
│
├── database/                        # Optional: custom database scripts or metadata
│
├── logs/                            # Airflow logs (auto-generated at runtime)
│
├── plugins/                         # Place for custom operators, hooks, macros
│
├── venv/                            # Python virtual environment (optional if using system Python)
│
├── .env                             # Environment variables (used by docker-compose)
├── docker-compose.yaml              # Official multi-service Docker setup for Airflow
└── README.md                        # Documentation for the project




---

## ✅ DAGs Overview

| DAG File                              | Description                                                               |
|--------------------------------------|---------------------------------------------------------------------------|
| `dag_python_operator.py`             | Basic PythonOperator with parameters                                       |
| `dag_python_database.py`             | Executes SQL commands on SQL Server using `SQLExecuteQueryOperator`       |
| `dag_python_pipeline.py`             | Pandas pipeline: reads, cleans, and transforms CSV                        |
| `dag_python_branching_operator.py`   | Branches logic based on Airflow Variables using `BranchPythonOperator`    |
| `dag_python_branching_catchup.py`    | Demonstrates `catchup=True` with date logic for weekday/weekend branching |
| `dag_python_branching_taskgroup.py`  | Groups related tasks using `TaskGroup`                                    |
| `dag_xcoms.py`                       | Uses XCom to pass data between tasks                                      |
| `modern_dag.py`                      | Uses context manager + BashOperator with external script                  |
| `dag.py`                             | A generic starter DAG                                                     |

---

## 🔌 Airflow Connection Required

Create the following connection in the Airflow UI:

- **Connection ID:** `sql_server_conn`
- **Conn Type:** Microsoft SQL Server
- **Host:** your SQL Server hostname or RDS endpoint
- **Port:** 1433
- **Schema:** dbo
- **Login/Password:** your credentials
- **Extra:**
  ```json
  {
    "encrypt": "no",
    "trustServerCertificate": "yes"
  }
