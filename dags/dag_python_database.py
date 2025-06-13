from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    'owner': 'javier',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id="dag_python_database",
    description='Basic DAG executing SQL Server commands',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['sql', 'python', 'database'],
) as dag:

    # Task to create the table only if it does not already exist
    create_table = SQLExecuteQueryOperator(
        task_id='create_table',
        conn_id='sql_server_conn',
        sql=r"""
            IF NOT EXISTS (
                SELECT * FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'users'
            )
            BEGIN
                CREATE TABLE dbo.users (
                    id INT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INT NOT NULL,
                    is_active BIT DEFAULT 1,
                    created_at DATETIME DEFAULT GETDATE()
                );
            END
        """
    )

    # Task to insert dummy data into the table
    insert_data = SQLExecuteQueryOperator(
        task_id='insert_data',
        conn_id='sql_server_conn',
        sql=r"""
            INSERT INTO users (id, name, age, is_active)
            VALUES 
                (1, 'Alice Johnson', 28, 1),
                (2, 'Bob Smith', 35, 0),
                (3, 'Carlos Rivera', 22, 1),
                (4, 'Diana Torres', 41, 1),
                (5, 'Edward Brown', 30, 0);
        """
    )

    # Task to query and return the data using XCom
    show_data = SQLExecuteQueryOperator(
        task_id='show_data',
        conn_id='sql_server_conn',
        sql="SELECT * FROM dbo.users",
        do_xcom_push=True
    )

    create_table >> insert_data >> show_data
