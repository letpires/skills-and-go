import sys
from pathlib import Path

# Garante import de kpis mesmo se o MCP subir com outro cwd
# sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastmcp import FastMCP
from kpis import (
    datasets_necessarios as _datasets_necessarios,
    get_estoque_criticos,
    get_taxa_cancelamento,
    get_taxa_comparecimento,
)

_DRIVE_HINT = (
    "Busque as planilhas LIMPAS no Drive: agenda_julho_limpo (ocupação/cancelamento) "
    "e estoque_limpo (estoque crítico). download_file_content com exportMimeType=text/csv."
)

mcp = FastMCP("AestheticsClinique")


@mcp.tool()
def datasets_necessarios() -> dict:
    """Lista planilhas do Drive necessárias para cada KPI."""
    return _datasets_necessarios()


@mcp.tool()
def taxa_comparecimento(agenda_csv: str, fonte_arquivo: str | None = None) -> dict:
    f"""Taxa de comparecimento da última semana (agenda).

    {_DRIVE_HINT}
    """
    result = get_taxa_comparecimento(agenda_csv)

    if fonte_arquivo:
        result["fonte_arquivo"] = fonte_arquivo
    return result


@mcp.tool()
def taxa_cancelamento(agenda_csv: str, fonte_arquivo: str | None = None) -> dict:
    f"""Taxa de cancelamento dos últimos 30 dias (agenda).

    {_DRIVE_HINT}
    """
    result = get_taxa_cancelamento(agenda_csv)
    if fonte_arquivo:
        result["fonte_arquivo"] = fonte_arquivo
    return result


@mcp.tool()
def estoque_criticos(estoque_csv: str, fonte_arquivo: str | None = None) -> dict:
    f"""Itens do estoque abaixo do mínimo.

    {_DRIVE_HINT}
    """
    result = get_estoque_criticos(estoque_csv)
    if fonte_arquivo:
        result["fonte_arquivo"] = fonte_arquivo
    return result


# TODO — evoluir depois da aula:
# faturamento_mes, top_procedimentos, tendencia_faturamento, taxa_cancelamento


if __name__ == "__main__":
    mcp.run()
