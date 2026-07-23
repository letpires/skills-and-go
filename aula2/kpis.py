"""KPIs da clínica — dados já limpos na aula 1, aqui só calcula.

Fluxo (Claude + Drive MCP):
  1. Drive MCP busca agenda_julho_limpo / estoque_limpo
  2. Agente passa o CSV para a tool
  3. pd.read_csv → KPI
"""

import io
from datetime import datetime, timedelta

import pandas as pd


def carregar_csv(csv_texto: str) -> pd.DataFrame:
    """Lê CSV do Drive MCP."""
    if not csv_texto or not csv_texto.strip():
        raise ValueError("CSV vazio. Confira se o Drive MCP retornou o conteúdo.")
    return pd.read_csv(io.StringIO(csv_texto))


# ---------------------------------------------------------------------------
# 1. Taxa de comparecimento — última semana
# ---------------------------------------------------------------------------

def get_taxa_comparecimento(agenda_csv: str) -> dict:
    df = carregar_csv(agenda_csv)
    df["data"] = pd.to_datetime(df["data"])

    hoje = datetime.today().date()
    inicio = hoje - timedelta(days=7)
    semana = df[df["data"].dt.date.between(inicio, hoje)]

    total = len(semana)
    realizados = (semana["status"] == "realizado").sum()
    cancelados = (semana["status"] == "cancelado").sum()
    taxa = round(realizados / total * 100, 1) if total > 0 else 0.0

    return {
        "periodo": f"{inicio} a {hoje}",
        "total_agendamentos": int(total),
        "realizados": int(realizados),
        "cancelados": int(cancelados),
        "taxa_comparecimento_pct": float(taxa),
    }



# ---------------------------------------------------------------------------
# 3. Estoque crítico
# ---------------------------------------------------------------------------

def get_estoque_criticos(estoque_csv: str) -> dict:
    df = carregar_csv(estoque_csv)

    criticos = df[df["quantidade_atual"] < df["quantidade_minima"]].copy()
    criticos["deficit"] = criticos["quantidade_minima"] - criticos["quantidade_atual"]
    criticos = criticos.sort_values("deficit", ascending=False)

    return {
        "total_itens_criticos": len(criticos),
        "itens": criticos[["produto", "quantidade_atual", "quantidade_minima", "deficit"]].to_dict(
            orient="records"
        ),
    }

def datasets_necessarios() -> dict:
    return {
        "workflow": [
            "1. Buscar planilhas LIMPAS no google-drive MCP (search_files)",
            "2. Baixar CSV (download_file_content, exportMimeType=text/csv)",
            "3. Passar o texto CSV para a tool",
        ],
        "planilhas": {
            "agenda_julho_limpo": {
                "busca": "title contains 'agenda_julho_limpo'",
                "tools": ["taxa_comparecimento", "taxa_cancelamento"],
            },
            "estoque_limpo": {
                "busca": "title contains 'estoque_limpo'",
                "tools": ["estoque_criticos"],
            },
        },
    }


# # ---------------------------------------------------------------------------
# # 2. Taxa de cancelamento — últimos 30 dias
# # ---------------------------------------------------------------------------

# def get_taxa_cancelamento(agenda_csv: str) -> dict:
#     df = carregar_csv(agenda_csv)
#     df["data"] = pd.to_datetime(df["data"])

#     hoje = datetime.today().date()
#     inicio = hoje - timedelta(days=30)
#     periodo = df[df["data"].dt.date.between(inicio, hoje)]

#     total = len(periodo)
#     cancelados = (periodo["status"] == "cancelado").sum()
#     taxa = round(cancelados / total * 100, 1) if total > 0 else 0.0

#     return {
#         "periodo": f"{inicio} a {hoje}",
#         "total_agendamentos": int(total),
#         "cancelados": int(cancelados),
#         "taxa_cancelamento_pct": float(taxa),
#     }


# ---------------------------------------------------------------------------
# TODO — evoluir depois da aula
# ---------------------------------------------------------------------------
# def get_faturamento_mes(financeiro_limpo): ...
# def get_top_procedimentos(agenda_limpa): ...
# def get_taxa_cancelamento()



