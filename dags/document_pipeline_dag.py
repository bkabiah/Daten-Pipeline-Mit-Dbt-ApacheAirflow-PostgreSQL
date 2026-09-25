from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from extract_docs import extract_and_load_to_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'document_analysis_pipeline',
    default_args=default_args,
    description='Extrahiert PDFs und transformiert sie mit dbt',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Task 1: PDFs extrahieren und in Raw Layer laden
    extract_docs = PythonOperator(
        task_id='extract_and_load_docs',
        python_callable=extract_and_load_to_postgres,
    )

    # Task 2: dbt Seed/Run (Wir nutzen dbt run, da die Daten schon in der DB sind)
    # Zuerst müssen wir das Schema 'raw' und 'analytics' in dbt bekannt machen oder einfach dbt run ausführen.
    # Wir erstellen ein pre-hook in dbt oder nutzen bash, um die Schemas zu erstellen.
    create_schemas = BashOperator(
        task_id='create_db_schemas',
        bash_command='PGPASSWORD=airflow psql -h postgres -U airflow -d airflow -c "CREATE SCHEMA IF NOT EXISTS raw; CREATE SCHEMA IF NOT EXISTS analytics; CREATE SCHEMA IF NOT EXISTS staging;"'
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir /opt/airflow/.dbt',
    )

    extract_docs >> create_schemas >> run_dbt
