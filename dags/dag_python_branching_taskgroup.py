from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.utils.edgemodifier import Label
from datetime import timedelta

# Function that prints a message, used by tasks in the TaskGroups
def print_msg(msg):
    print(f"Message: {msg}")

default_args = {
    'owner': 'javier',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_taskgroup',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['taskgroup'],
) as dag:

    # Initial task
    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print("Start of the DAG")
    )

    # TaskGroup representing the first phase of processing
    with TaskGroup('phase_A', tooltip='First processing phase') as phase_a:
        t1 = PythonOperator(
            task_id='task_1',
            python_callable=print_msg,
            op_args=['Task 1 of Phase A']
        )
        t2 = PythonOperator(
            task_id='task_2',
            python_callable=print_msg,
            op_args=['Task 2 of Phase A']
        )
        # Task 2 runs after Task 1
        t1 >> t2

    # TaskGroup representing the second phase of processing
    with TaskGroup('phase_B', tooltip='Second processing phase') as phase_b:
        t3 = PythonOperator(
            task_id='task_3',
            python_callable=print_msg,
            op_args=['Task 3 of Phase B']
        )
        t4 = PythonOperator(
            task_id='task_4',
            python_callable=print_msg,
            op_args=['Task 4 of Phase B']
        )
        t3 >> t4

    # Final task
    end = PythonOperator(
        task_id='end',
        python_callable=lambda: print("End of the DAG")
    )

    # Defining the full flow with labels for better visualization in the UI
    start >> Label("Run Phase A") >> phase_a
    phase_a >> Label("Then Phase B") >> phase_b
    phase_b >> Label("Complete the flow") >> end
