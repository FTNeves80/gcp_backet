import requests
import pandas as pd
from google.cloud import storage
from google.cloud import storage, bigquery
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env ###
load_dotenv()
gcp_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials

# Nome do bucket e arquivo
bucket_name = "gcs_python_test"
destination_blob_name = "df_data_filtered.json"  # Nome no GCS
dataset_id = "ds_raw"
table_id = "tb_raw_deputados"

def extract_data():
    # Faz a requisição para a API da Câmara dos Deputados
    resp = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados")
    data = resp.json()
    df_data = pd.DataFrame(data["dados"])

    # Filtra as colunas desejadas
    df_data_filtered = df_data[["nome","email","siglaUf","siglaPartido"]]
    #json_data = df_data_filtered.to_json(orient="records", force_ascii=False)
    json_data = "\n".join(df_data_filtered.to_json(orient="records", lines=True).splitlines())

    return json_data


# Função para fazer o upload do JSON para o bucket do GCS
def upload_json_to_bucket(bucket_name, destination_blob_name, json_content):
    # Cria cliente de storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Envia o arquivo
    blob.upload_from_string(json_content, content_type="application/json")

    print(f"Arquivo {destination_blob_name} enviado para gs://{bucket_name}/{destination_blob_name}")


def insert_to_bigquery(bucket_name, blob_name, dataset_id, table_id):
    client = bigquery.Client()

    # Cria o dataset se não existir
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} já existe.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Dataset {dataset_id} criado.")

    # Define o schema da tabela
    schema = [
        bigquery.SchemaField("nome", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("siglaUf", "STRING"),
        bigquery.SchemaField("siglaPartido", "STRING"),
    ]

    table_ref = dataset_ref.table(table_id)

    # Cria a tabela se não existir
    try:
        client.get_table(table_ref)
        print(f"Tabela {table_id} já existe.")
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Tabela {table_id} criada.")

    # Caminho do arquivo no GCS
    gcs_uri = f"gs://{bucket_name}/{blob_name}"

    # Configuração da carga
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    # Executa o job de carga
    load_job = client.load_table_from_uri(
        gcs_uri, table_ref, job_config=job_config
    )


# executa
upload_json_to_bucket(bucket_name, destination_blob_name, extract_data())
insert_to_bigquery(bucket_name, destination_blob_name, dataset_id, table_id)