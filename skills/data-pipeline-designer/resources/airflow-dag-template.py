"""
Production-ready Airflow DAG template for batch ELT pipelines.
Includes: TaskGroups, SLAs, data quality checks, error handling.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.task_group import TaskGroup
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

# Default args with SLA and retries
default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "email": ["alerts@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "sla": timedelta(hours=4),  # Pipeline must complete within 4 hours
}

with DAG(
    "production_elt_pipeline",
    default_args=default_args,
    description="Production ELT with quality gates",
    schedule_interval="0 2 * * *",  # Daily at 2 AM
    start_date=datetime(2025, 10, 1),
    catchup=False,
    tags=["production", "elt", "daily"],
) as dag:

    # TaskGroup: Ingestion from multiple sources (parallel)
    with TaskGroup("ingestion") as ingestion:
        ingest_orders = SnowflakeOperator(
            task_id="ingest_orders",
            sql="COPY INTO staging.orders FROM @s3_stage/orders",
        )
        ingest_customers = SnowflakeOperator(
            task_id="ingest_customers",
            sql="COPY INTO staging.customers FROM @s3_stage/customers",
        )

    # Data quality: Pre-transformation checks
    validate_source = GreatExpectationsOperator(
        task_id="validate_source_data",
        checkpoint_name="staging_checkpoint",
        fail_task_on_validation_failure=True,  # Block pipeline if critical checks fail
    )

    # TaskGroup: dbt transformations (sequential layers)
    with TaskGroup("transformations") as transformations:
        dbt_staging = PythonOperator(
            task_id="dbt_staging",
            python_callable=lambda: run_dbt_models(["staging"]),
        )
        dbt_intermediate = PythonOperator(
            task_id="dbt_intermediate",
            python_callable=lambda: run_dbt_models(["intermediate"]),
        )
        dbt_marts = PythonOperator(
            task_id="dbt_marts",
            python_callable=lambda: run_dbt_models(["marts"]),
        )
        dbt_staging >> dbt_intermediate >> dbt_marts

    # Data quality: Post-transformation checks
    validate_marts = GreatExpectationsOperator(
        task_id="validate_marts",
        checkpoint_name="marts_checkpoint",
        fail_task_on_validation_failure=True,
    )

    # Success notification
    notify_success = PythonOperator(
        task_id="notify_success",
        python_callable=lambda: send_slack_alert("Pipeline completed successfully"),
    )

    # Define task dependencies
    ingestion >> validate_source >> transformations >> validate_marts >> notify_success


def run_dbt_models(models):
    """Execute dbt models with logging."""
    import subprocess

    result = subprocess.run(["dbt", "run", "--models"] + models, capture_output=True, check=False)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    return result.stdout


def send_slack_alert(message):
    """Send Slack notification (implement with actual webhook)."""
    print(f"ALERT: {message}")
