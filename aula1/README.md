# Aula 1 — Clínica de estética: análise de dados

Análise completa dos dados de uma clínica de estética com Python: carregamento via Google Sheets, inspeção, limpeza, EDA, KPIs e tendência de faturamento.

O notebook principal é `analise-completa.ipynb`.

## Pré-requisitos

- Python 3.12 recomendado
- Conta Google / acesso ao Google Cloud Platform (GCP)
- Planilhas no Google Drive compartilhadas com a Service Account

## 1. Ambiente virtual (venv)

Na pasta `aula1`:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Pacotes usados: `pandas`, `numpy`, `plotly`, `gspread`, `google-auth`.

Para Jupyter / VS Code / Cursor, selecione o interpretador do `.venv`.

## 2. Chave GCP (Service Account)

A autenticação com Google Sheets/Drive usa uma **chave JSON de Service Account** gerada no GCP.

### Criar a chave

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie (ou selecione) um projeto
3. Ative as APIs **Google Sheets API** e **Google Drive API**
4. Vá em **IAM e administrador → Contas de serviço**
5. Crie uma Service Account e gere uma chave JSON
6. Baixe o arquivo `.json` e coloque-o na pasta `aula1` (ou em `credentials/`)

### Configurar no notebook

No setup do `analise-completa.ipynb`, ajuste o caminho da chave:

```python
JSON_KEY = Path("seu-arquivo-da-service-account.json")
FOLDER_ID = "id-da-pasta-no-google-drive"
```

O cliente é criado assim:

```python
gc = gspread.service_account(filename=JSON_KEY)
```

### Compartilhar as planilhas

A Service Account só acessa o que for compartilhado com o e-mail dela (algo como `nome@projeto.iam.gserviceaccount.com`):

- Compartilhe a **pasta** do Drive (ou cada planilha) com esse e-mail, com permissão de **Editor** se for gravar dados
- Crie as planilhas de destino **antes** de subir dados limpos — Service Accounts não devem ser proprietárias de arquivos novos (risco de `storageQuotaExceeded`)

### Segurança

- **Não** versionar a chave JSON no Git
- O `.gitignore` já ignora `.venv/`, `credentials/` e arquivos `*-*-*.json`
- Se a chave vazar, revogue-a no Console do GCP e gere outra

## 3. Rodar a aula

Com o `.venv` ativo e a chave no lugar:

```bash
jupyter notebook analise-completa.ipynb
# ou abra o notebook no Cursor / VS Code e execute as células
```

Fluxo do notebook:

1. Carregamento e inspeção  
2. Diagnóstico de qualidade  
3. Limpeza  
4. EDA  
5. KPIs  
6. Tendência de faturamento  

## Estrutura

```
aula1/
├── analise-completa.ipynb   # notebook da aula
├── requirements.txt
├── .gitignore
├── README.md
└── *.json                   # chave GCP (local, não commitada)
```
