from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default arguments applied to all tasks
default_args = {
    'owner': 'javier',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Simple Python functions used in PythonOperator
def print_function():
    print("This is the simplest possible PythonOperator.")

def print_word(word):
    print(f"Hi, you are printing: {word}")

# DAG definition
with DAG(
    dag_id="dag_hello_python_operator",
    description='A basic DAG using PythonOperator',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['simple', 'python'],
) as dag:

    task_hello = PythonOperator(
        task_id='another_task_with_script_1',
        python_callable=print_function
    )

    task_hello_2 = PythonOperator(
        task_id='another_task_with_script_2',
        python_callable=print_word,
        op_kwargs={'word': 'Javier'}
    )

    task_hello_3 = PythonOperator(
        task_id='another_task_with_script_3',
        python_callable=print_word,
        op_kwargs={'word': 'Javier'}
    )

    [task_hello, task_hello_2] >> task_hello_3
