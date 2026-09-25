FROM apache/airflow:2.8.1-python3.10

# Python Packages für PDF-Analyse und DB-Verbindung
RUN pip install --no-cache-dir pypdf fpdf psycopg2-binary sqlalchemy

# dbt-core und dbt-postgres mit kompatiblen Versionen installieren
# Wir nutzen dbt 1.5.x, das garantiert mit dem Airflow-Image kompatibel ist
RUN pip install --no-cache-dir 'dbt-core==1.5.6' 'dbt-postgres==1.5.6' 'Jinja2==3.1.2'

# dbt Projekt in den Container kopieren
COPY dbt/ /opt/airflow/dbt/
WORKDIR /opt/airflow/dbt

# dbt Profile erstellen (für den Container)
RUN mkdir -p /opt/airflow/.dbt
COPY dbt_profiles.yml /opt/airflow/.dbt/profiles.yml

ENV DBT_PROFILES_DIR=/opt/airflow/.dbt
