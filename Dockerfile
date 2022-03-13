FROM apache/airflow:2.2.0
RUN pip install --no-cache-dir --user matplotlib==3.3.4 scikit-learn==0.24.2