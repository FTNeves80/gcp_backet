# 📊 Deputados Data Extractor

Este projeto tem como objetivo coletar dados públicos da API da Câmara dos Deputados, filtrar informações relevantes e enviá-las diretamente para um bucket no **Google Cloud Storage (GCS)**, sem necessidade de salvar arquivos localmente.

## 🚀 Funcionalidades

- Coleta dados dos deputados em exercício diretamente da [API da Câmara](https://dadosabertos.camara.leg.br/swagger/api.html).
- Filtra informações como:
  - `nome`
  - `email`
  - `siglaUf`
  - `siglaPartido`
- Converte os dados em formato JSON (com suporte a UTF-8).
- Faz upload diretamente para o bucket no Google Cloud Storage (GCS).

## 🧰 Requisitos

- Python 3.7+
- Conta com acesso ao **Google Cloud Platform**
- Bucket criado no GCS
- Credencial do GCP com permissão de escrita no bucket (arquivo `.json`)

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/deputados-gcs-upload.git
   cd deputados-gcs-upload

📦 deputados-gcs-upload
├── main.py
├── requirements.txt
└── README.md
