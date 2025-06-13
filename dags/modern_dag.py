from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments applied to all tasks
default_args = {
    'owner': 'javier',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG using context manager style (modern approach)
with DAG(
    dag_id="dag_hello_world_modern_style",
    description='Hello World DAG using modern DAG definition style',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,  # prevents backfilling past runs
    tags=['example', 'modern_style'],
    template_searchpath='/opt/airflow/dags/bash_scripts'  # path for external bash scripts
) as dag:

    # Task using an external bash script
    task_hello = BashOperator(
        task_id='task_with_script',
        bash_command='taskA.sh'
    )

    # Simple echo task
    task_hello_2 = BashOperator(
        task_id='second_task',
        bash_command='echo hello from the second modern task'
    )

    # Another simple echo task
    task_hello_3 = BashOperator(
        task_id='third_task',
        bash_command='echo hello from the third modern task'
    )

    # Task dependencies: task_hello and task_hello_2 must run before task_hello_3
    [task_hello, task_hello_2] >> task_hello_3
