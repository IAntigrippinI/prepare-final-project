FROM apache/airflow:2.9.3-python3.11

USER root

# Устанавливаем компиляторы и dev-библиотеки
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        python3-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Возвращаемся к airflow
USER airflow

# Копируем requirements
COPY requirements.txt .

# Устанавливаем зависимости как airflow user
RUN pip install --no-cache-dir -r requirements.txt

# Копируем DAG-и и src
COPY dags/ /opt/airflow/dags/
COPY src/ /opt/airflow/src/
COPY alembic.ini /opt/airflow/alembic.ini

WORKDIR /opt/airflow

# Обновляем PYTHONPATH, чтобы включить локальные пакеты
ENV PYTHONPATH=/opt/airflow/src:/home/airflow/.local/lib/python3.11/site-packages:$PYTHONPATH
