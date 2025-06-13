from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.models import Variable

default_args = {
    'owner': 'javier',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# This function retrieves a Variable from Airflow
# The return value is pushed to XCom because do_xcom_push=True
def define_branch():
    value = Variable.get('choicer', default_var='False')
    print(f"VariableSelector = {value}")
    return value

# This function pulls the XCom value from the previous task
# and returns the task_id to execute next based on the value
def select_branch(**kwargs):
    ti = kwargs['ti']
    raw_value = ti.xcom_pull(task_ids='define_branch_task')
    print(f"Read value was: {raw_value}")

    if str(raw_value).strip().lower() == 'true':
        return 'true_choice_task'
    else:
        return 'false_choice_task'

# Sample Python tasks
def print_true():
    print("This is the TRUE path.")

def print_false():
    print("This is the FALSE path.")

# DAG definition
with DAG(
    dag_id="dag_branching_operator",
    description="Branching logic based on Variable and XCom",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['xcom', 'branching'],
) as dag:

    define_branch_task = PythonOperator(
        task_id='define_branch_task',
        python_callable=define_branch,
        do_xcom_push=True
    )

    select_branch_task = BranchPythonOperator(
        task_id='select_branch_task',
        python_callable=select_branch,
        provide_context=True
    )

    true_choice_task = PythonOperator(
        task_id='true_choice_task',
        python_callable=print_true
    )

    false_choice_task = PythonOperator(
        task_id='false_choice_task',
        python_callable=print_false
    )

    define_branch_task >> select_branch_task >> [true_choice_task, false_choice_task]
