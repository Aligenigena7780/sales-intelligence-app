import pandas as pd


MESES_PT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


def nome_mes(numero_mes: int) -> str:
    return MESES_PT.get(numero_mes, str(numero_mes))


def calcular_kpis(df: pd.DataFrame) -> dict:
    faturamento = float(df["venda_bruta"].sum())
    lucro = float(df["lucro"].sum())
    venda_liquida = float(df["venda_liquida"].sum())

    margem = 0.0
    if venda_liquida != 0:
        margem = lucro / venda_liquida

    pedidos = int(df["documento"].nunique())
    clientes = int(df["codigo_cliente"].nunique())
    skus = int(df["sku"].nunique())

    return {
        "faturamento": faturamento,
        "lucro": lucro,
        "margem": margem,
        "pedidos": pedidos,
        "clientes": clientes,
        "skus": skus,
    }


def calcular_variacao(valor_atual: float, valor_anterior: float):
    delta_absoluto = valor_atual - valor_anterior

    if valor_anterior == 0:
        delta_percentual = 0.0 if valor_atual == 0 else 1.0
    else:
        delta_percentual = delta_absoluto / valor_anterior

    return delta_absoluto, delta_percentual


def filtrar_mes_unico(df: pd.DataFrame, ano: int, mes: int) -> pd.DataFrame:
    return df[(df["ano"] == ano) & (df["mes"] == mes)].copy()


def filtrar_intervalo_meses(
    df: pd.DataFrame,
    ano_inicio: int,
    mes_inicio: int,
    ano_fim: int,
    mes_fim: int,
) -> pd.DataFrame:
    inicio = pd.Timestamp(year=ano_inicio, month=mes_inicio, day=1)
    fim = pd.Timestamp(year=ano_fim, month=mes_fim, day=1) + pd.offsets.MonthEnd(1)
    return df[(df["data"] >= inicio) & (df["data"] <= fim)].copy()


def periodo_anterior_mes_unico(ano: int, mes: int):
    if mes == 1:
        return ano - 1, 12
    return ano, mes - 1


def periodo_anterior_intervalo(
    ano_inicio: int,
    mes_inicio: int,
    ano_fim: int,
    mes_fim: int,
):
    inicio = pd.Timestamp(year=ano_inicio, month=mes_inicio, day=1)
    fim = pd.Timestamp(year=ano_fim, month=mes_fim, day=1)

    quantidade_meses = (fim.year - inicio.year) * 12 + (fim.month - inicio.month) + 1

    fim_anterior = inicio - pd.offsets.MonthBegin(1)
    inicio_anterior = fim_anterior - pd.DateOffset(months=quantidade_meses - 1)

    return (
        inicio_anterior.year,
        inicio_anterior.month,
        fim_anterior.year,
        fim_anterior.month,
    )
