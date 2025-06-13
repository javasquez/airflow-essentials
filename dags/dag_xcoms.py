import pandas as pd
from datetime import timedelta
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.operators.python import PythonOperator

# Default task arguments
default_args = {
    'owner': 'javier'
}

# Task: Reads a CSV file and pushes the content as JSON to XCom
def read_csv_file(path):
    file_df = pd.read_csv(path)
    print(file_df)
    return file_df.to_json()

# Task: Cleans the data by removing rows with missing values
def clean_data(**kwargs):
    print('Printing Airflow context info from clean_data task:')
    print(f"Run ID: {kwargs['run_id']}")
    print(f"Execution Date: {kwargs['execution_date']}")
    print(f"DS: {kwargs['ds']}")
    print(f"Task Instance Key: {kwargs['task_instance_key_str']}")

    ti = kwargs['ti']
    json_data = ti.xcom_pull(task_ids='read_csv_file')
    df = pd.read_json(json_data)
    df = df.dropna()
    print(df)

    return df.to_json()

# Task: Filters smokers, groups them by sex, and saves the result as CSV
def group_by_sex(**kwargs):
    ti = kwargs['ti']
    json_df = ti.xcom_pull(task_ids='clean_data')
    df = pd.read_json(json_df)
    df = df[df['smoker'] == 'yes']
    df = df.groupby('sex').agg({'age': 'count'}).reset_index()
    print('Amount of smokers by sex:')
    print(df)
    
    df.to_csv('/opt/airflow/data/outputs/smokers.csv', index=False)
    return df.to_json()

# DAG definition
with DAG(
    dag_id='dag_first_pandas_pipeline',
    description='A simple ETL pipeline with pandas and PythonOperator',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@once',
    catchup=False,
    tags=['pythonOperator', 'pandas'],
) as dag:

    read_csv_file_task = PythonOperator(
        task_id='read_csv_file',
        python_callable=read_csv_file,
        op_kwargs={'path': '/opt/airflow/data/inputs/insurance.csv'}
    )

    clean_data_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data
    )

    group_by_sex_task = PythonOperator(
        task_id='group_by_sex',
        python_callable=group_by_sex
    )

    read_csv_file_task >> clean_data_task >> group_by_sex_task
