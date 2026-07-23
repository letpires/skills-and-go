# Aula 2 — MCP de KPIs no Claude + Google Drive

Nesta aula você sobe um **servidor MCP local** (`AestheticsClinique`) com tools de KPI e conecta o **Claude Desktop** a ele e ao **Google Drive**, para o agente buscar as planilhas limpas da aula 1 e calcular indicadores.

Arquivos principais:

- `mcp_server.py` — servidor FastMCP (`taxa_comparecimento`, `taxa_cancelamento`, `estoque_criticos`, `datasets_necessarios`)
- `kpis.py` — lógica dos KPIs (pandas + CSV)
- `requirements.txt` — dependências desta aula

Fluxo esperado:

1. Drive MCP busca `agenda_limpa` / `estoque_limpo`
2. Baixa o conteúdo como CSV (`download_file_content` com `exportMimeType=text/csv`)
3. Passa o texto CSV para as tools do servidor local

## Arquitetura / workflow do agente

![Workflow do agente](workflow%20agente.png)

---

## Pré-requisitos

- Python 3.10+ (3.12 recomendado)
- [Claude Desktop](https://claude.ai/download) instalado
- Planilhas **limpas** da aula 1 no Drive (`agenda_limpa`, `estoque_limpo`)
- Conta Google + projeto no GCP (para o Drive MCP)
- Plano Claude **Pro / Max / Team / Enterprise** para o conector remoto do Google Drive

---

## 1. Dependências (requirements)

Hoje o curso tem **um `requirements.txt` por aula** (`aula1/`, `aula2/`). Você pode seguir assim ou consolidar tudo num requirements na raiz do repo.

### Opção A — Por aula (como está agora)

Na pasta `aula2`:

```bash
cd aula2
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

Pacotes desta aula: `fastmcp` e `pandas`.

### Opção B — Instalar as libs na mão e depois registrar no requirements

Com o venv ativo:

```bash
pip install fastmcp pandas
```

Confira o que entrou:

```bash
pip freeze | grep -E 'fastmcp|pandas'
```

Se o projeto tiver (ou passar a ter) um **requirements principal na raiz**:

```bash
# na raiz do repo
pip freeze | grep -E '^(fastmcp|pandas)==' >> requirements.txt
# ou edite requirements.txt e adicione:
# fastmcp
# pandas
```

Se mantiver separado por aula, atualize só `aula2/requirements.txt`:

```text
fastmcp
pandas
```

### Dica

No Claude Desktop o MCP roda com o **Python do venv**. Por isso o caminho no config deve apontar para `.venv/bin/python` (macOS/Linux) ou `.venv\Scripts\python.exe` (Windows), não para o Python global.

---

## 2. Onde fica o config do Claude Desktop

O arquivo se chama `claude_desktop_config.json`. A pasta fica **escondida** no sistema.

### Forma mais segura (qualquer SO)

No Claude Desktop:

**Settings → Developer → Edit Config**

Isso cria o arquivo se ainda não existir e abre a pasta correta da sua instalação.

### macOS (Library)

A pasta `Library` fica oculta. Caminho:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Abrir no Finder / Terminal:

```bash
# abrir a pasta no Finder
open ~/Library/Application\ Support/Claude/

# editar o config
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json

# ou no VS Code / Cursor
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Se o Finder não mostrar Library: **Finder → Ir → Ir para a pasta…** (`Cmd + Shift + G`) e cole:

```text
~/Library/Application Support/Claude/
```

### Windows (AppData — pasta oculta)

Caminho padrão:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

Abrir:

```powershell
# Explorer na pasta
explorer %APPDATA%\Claude

# Notepad
notepad %APPDATA%\Claude\claude_desktop_config.json
```

Ou: `Win + R` → digite `%APPDATA%\Claude` → Enter.

Se AppData não aparece no Explorer: **Exibir → Mostrar → Itens ocultos**.

> Em algumas instalações (Microsoft Store / MSIX), o arquivo real pode estar em:
>
> `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\`
>
> Se editar o config e o MCP não aparecer, use **Edit Config** no app ou confira esse caminho alternativo.

---

## 3. Conectar o MCP da clínica no Claude

### Passo a passo

1. Crie o venv e instale as deps (seção 1)
2. Descubra o caminho **absoluto** do Python do venv e do `mcp_server.py`
3. Abra `claude_desktop_config.json`
4. Adicione (ou mescle) o bloco abaixo em `mcpServers`
5. Salve o arquivo
6. **Feche o Claude Desktop por completo** e abra de novo (quit, não só fechar a janela)
7. Em um chat novo, confira se as tools `aesthetics-clinique` / `AestheticsClinique` aparecem

### Exemplo de config (macOS)

Substitua pelo caminho absoluto da sua máquina:

```json
{
  "mcpServers": {
    "aesthetics-clinique": {
      "command": "/Users/SEU_USUARIO/Desktop/dev/skills-and-go/aula2/.venv/bin/python",
      "args": [
        "/Users/SEU_USUARIO/Desktop/dev/skills-and-go/aula2/mcp_server.py"
      ]
    }
  }
}
```

### Exemplo de config (Windows)

```json
{
  "mcpServers": {
    "aesthetics-clinique": {
      "command": "C:\\Users\\SEU_USUARIO\\Desktop\\dev\\skills-and-go\\aula2\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\SEU_USUARIO\\Desktop\\dev\\skills-and-go\\aula2\\mcp_server.py"
      ]
    }
  }
}
```

### Se já existirem outros MCPs

Não apague o JSON inteiro — só acrescente a chave `aesthetics-clinique` dentro de `mcpServers`, mantendo vírgulas válidas.

### Testar o servidor fora do Claude (opcional)

```bash
cd aula2
source .venv/bin/activate
python mcp_server.py
```

Se subir sem erro de import (`fastmcp`, `kpis`, `pandas`), o caminho do Python está ok.

### Tools expostas

| Tool | O que faz |
|------|-----------|
| `datasets_necessarios` | Lista planilhas e o workflow Drive → CSV → KPI |
| `taxa_comparecimento` | Comparecimento da última semana (`agenda_limpa`) |
| `taxa_cancelamento` | Cancelamento dos últimos 30 dias (`agenda_limpa`) |
| `estoque_criticos` | Itens abaixo do mínimo (`estoque_limpo`) |

---

## 4. Conectar o Google Drive no Claude

As tools do Drive usadas nesta aula batem com o **MCP remoto oficial** do Google (`search_files`, `download_file_content`).

### 4.1 No Google Cloud

1. Crie/selecione um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Ative:
   - **Google Drive API** (`drive.googleapis.com`)
   - **Google Drive MCP API** (`drivemcp.googleapis.com`)
3. Configure o **OAuth consent screen** (Branding / Audience / Data Access)
4. Em Data Access, adicione scopes (conforme a [doc do Google](https://developers.google.com/workspace/drive/api/guides/configure-mcp-server)):
   - `https://www.googleapis.com/auth/drive.readonly`
   - `https://www.googleapis.com/auth/drive.file`
5. Se o app for **External**, adicione seu e-mail em **Test users**
6. Crie um **OAuth Client ID**:
   - Tipo: **Web application**
   - Authorized redirect URI: `https://claude.ai/api/mcp/auth_callback`
7. Copie o **Client ID** e o **Client Secret**

### 4.2 No Claude (connector)

1. Abra Claude Desktop (ou claude.ai)
2. Vá em **Settings → Connectors** (ou Admin settings → Connectors)
3. **Add custom connector**
4. Preencha:
   - **Server name:** `Google Drive`
   - **Remote MCP server URL:** `https://drivemcp.googleapis.com/mcp/v1`
   - Em **Advanced settings:** Client ID e Client Secret do passo anterior
5. Salve e complete o login OAuth com a conta Google que tem as planilhas
6. Confirme que o conector ficou autenticado

> Precisa de plano Claude **Pro / Max / Team / Enterprise** para esse conector remoto.

### 4.3 Planilhas no Drive

Garanta que existem (da aula 1) arquivos como:

- `agenda_limpa`
- `estoque_limpo`

A Service Account da aula 1 **não** é a mesma autenticação do Drive MCP no Claude: aqui o Claude acessa o Drive **como o usuário** que autenticou no OAuth.

---

## 5. Usar os dois juntos

Com **aesthetics-clinique** + **Google Drive** ativos, peça por exemplo:

> Use o Drive para achar `agenda_limpa`, baixe como CSV e calcule a taxa de comparecimento com as tools da clínica.

O agente deve:

1. Chamar `datasets_necessarios` (opcional, para lembrar o workflow)
2. `search_files` no Drive (`title contains 'agenda_limpa'` / `estoque_limpo`)
3. `download_file_content` com `exportMimeType=text/csv`
4. Passar o CSV para `taxa_comparecimento`, `taxa_cancelamento` ou `estoque_criticos`

---

## 6. Troubleshooting rápido

| Problema | O que checar |
|----------|----------------|
| MCP não aparece no Claude | Quit completo do app; caminhos absolutos; JSON válido |
| Erro de import no server | venv ativo na instalação; `pip install -r requirements.txt`; `command` aponta para o Python do `.venv` |
| Drive não autentica | Redirect URI correta; APIs `drive` + `drivemcp` ativas; test user no OAuth |
| CSV vazio / KPI falha | Planilha limpa existe? Nome certo? Export CSV ok? |
| Config “não salva” no Windows | Confira o caminho MSIX em `%LOCALAPPDATA%\Packages\Claude_...` |

Logs MCP (macOS):

```bash
open ~/Library/Logs/Claude/
```

Windows: `%APPDATA%\Claude\logs\`

---

## Estrutura

```
aula2/
├── mcp_server.py           # FastMCP — tools expostas ao Claude
├── kpis.py                 # cálculo dos KPIs
├── workflow agente.png     # diagrama do fluxo do agente
├── requirements.txt        # fastmcp, pandas
├── .venv/                  # ambiente local (não versionar)
└── README.md
```
