import requests
import pandas as pd
from google.cloud import storage
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env ###
load_dotenv()
gcp_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials

# Faz a requisição para a API da Câmara dos Deputados
resp = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados")
data = resp.json()
df_data = pd.DataFrame(data["dados"])

# Filtra as colunas desejadas
df_data_filtered = df_data[["nome","email","siglaUf","siglaPartido"]]
json_data = df_data_filtered.to_json(orient="records", force_ascii=False)

# Nome do bucket e arquivo
bucket_name = "gcs_python_test"
destination_blob_name = "df_data_filtered.json"  # Nome no GCS

# Função para fazer o upload do JSON para o bucket do GCS
def upload_json_to_bucket(bucket_name, destination_blob_name, json_content):
    # Cria cliente de storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Envia o arquivo
    blob.upload_from_string(json_content, content_type="application/json")

    print(f"Arquivo {destination_blob_name} enviado para gs://{bucket_name}/{destination_blob_name}")


# Faz o upload
upload_json_to_bucket(bucket_name, destination_blob_name, json_data)