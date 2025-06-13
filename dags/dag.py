from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default DAG arguments
default_args = {
    'owner': 'javier'
}

# Define DAG
dag = DAG(
    dag_id='dag_hello_bash_operator',  # consistent naming style
    description='A simple DAG using BashOperator to print Hello World',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,  # recommended to avoid backfilling old runs
    tags=['bash', 'hello']
)

# Define a single Bash task
hello_task = BashOperator(
    task_id='hello_world_task',
    bash_command='echo Hello World from my first task',
    dag=dag
)

# Set task in the DAG
hello_task
