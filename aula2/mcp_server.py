import sys
from pathlib import Path

# Garante import de kpis mesmo se o MCP subir com outro cwd
# sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastmcp import FastMCP
from kpis import (
    datasets_necessarios as _datasets_necessarios,
    get_estoque_criticos,
    get_taxa_comparecimento,
)

mcp = FastMCP("AestheticsClinique")


@mcp.tool()
def datasets_necessarios() -> dict:
    """Lista planilhas do Drive necessárias para cada KPI."""
    return _datasets_necessarios()


@mcp.tool()
def taxa_comparecimento(agenda_csv: str, fonte_arquivo: str | None = None) -> dict:
    """Taxa de comparecimento da última semana (agenda)."""
    result = get_taxa_comparecimento(agenda_csv)

    if fonte_arquivo:
        result["fonte_arquivo"] = fonte_arquivo
    return result



@mcp.tool()
def estoque_criticos(estoque_csv: str, fonte_arquivo: str | None = None) -> dict:
    """Itens do estoque abaixo do mínimo."""
    result = get_estoque_criticos(estoque_csv)
    if fonte_arquivo:
        result["fonte_arquivo"] = fonte_arquivo
    return result


# TODO — evoluir depois da aula:
# faturamento_mes, top_procedimentos, tendencia_faturamento, taxa_cancelamento


# Execute este trecho apenas quando este arquivo for executado diretamente.
if __name__ == "__main__":
    mcp.run()
