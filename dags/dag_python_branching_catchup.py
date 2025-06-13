from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

def decide_branch(**kwargs):
    execution_date = kwargs['execution_date']
    print(f"Simulated execution date: {execution_date}")
    
    # 0 = Monday, 6 = Sunday
    weekday = execution_date.weekday()
    if weekday < 5:
        return 'weekday_task'
    else:
        return 'weekend_task'

def run_weekday_task():
    print("This is a weekday. Running weekday task.")

def run_weekend_task():
    print("This is a weekend. Running weekend task.")

default_args = {
    'owner': 'javier',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='branching_based_on_weekday',
    default_args=default_args,
    start_date=days_ago(20),              # Simulates 3 days ago
    schedule_interval='@daily',          # One run per day
    catchup=True,                        # ✅ Enables backfilling of past days
    
    tags=['branching', 'examples']
) as dag:

    branch = BranchPythonOperator(
        task_id='decide_day_type',
        python_callable=decide_branch,
        provide_context=True
    )

    weekday_task = PythonOperator(
        task_id='weekday_task',
        python_callable=run_weekday_task
    )

    weekend_task = PythonOperator(
        task_id='weekend_task',
        python_callable=run_weekend_task
    )

    branch >> [weekday_task, weekend_task]
