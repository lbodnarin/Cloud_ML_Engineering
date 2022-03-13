from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('FL_DELAY', default_args={'depends_on_past': True}, start_date=datetime(2009,1,1), end_date=datetime(2018,12,31), schedule_interval='0 0 1 1 *') as dag:

    from tasks.t1_create_database import t1_create_database
    from tasks.t2_create_table import t2_create_table
    from tasks.t3_copy_from import t3_copy_from
    from tasks.t4_outlier_detection import t4_outlier_detection
    from tasks.t5_matplotlib import t5_matplotlib
    import boto3
    import json

    dbname = 'FL_DELAY'
    OWNER = 'airflow'
    secret_name = 'RDS/Postgres'
    region_name = 'us-east-1'
    bucket_name = 'mybucket'
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(get_secret_value_response['SecretString'])
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name=bucket_name)

    t1 = PythonOperator(task_id='t1_create_database', python_callable=t1_create_database, op_args=[secret, dbname, OWNER])
    t2 = PythonOperator(task_id='t2_create_table', python_callable=t2_create_table, op_args=[secret, dbname])
    t3 = PythonOperator(task_id='t3_copy_from', python_callable=t3_copy_from, op_args=[bucket, secret, dbname])
    t4 = PythonOperator(task_id='t4_outlier_detection', python_callable=t4_outlier_detection, op_args=[secret, dbname])
    t5 = PythonOperator(task_id='t5_matplotlib', python_callable=t5_matplotlib, op_args=[bucket, secret, dbname])

    t1 >> t2 >> t3 >> t4 >> t5