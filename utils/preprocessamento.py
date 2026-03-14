import pandas as pd


def _validar_colunas(df, colunas_obrigatorias, nome_base):
    faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
    if faltantes:
        raise ValueError(
            f"As seguintes colunas obrigatórias não foram encontradas na base de {nome_base}: {faltantes}"
        )


def preprocessar_vendas(df: pd.DataFrame) -> pd.DataFrame:
    colunas_obrigatorias = [
        "Tipo",
        "calendarioData",
        "Documento",
        "Código",
        "Cliente",
        "CNPJ",
        "SKU",
        "Descrição",
        "Fabricante",
        "Linha",
        "Qtd.",
        "Venda",
        "Venda Líquida",
        "Lucro",
    ]
    _validar_colunas(df, colunas_obrigatorias, "vendas")

    df = df.copy()

    df = df[df["Tipo"].astype(str).str.strip().eq("N")].copy()

    df["calendarioData"] = pd.to_datetime(df["calendarioData"], errors="coerce")

    colunas_numericas = ["Qtd.", "Venda", "Venda Líquida", "Lucro"]
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    colunas_texto = [
        "Documento",
        "Código",
        "Cliente",
        "CNPJ",
        "SKU",
        "Descrição",
        "Fabricante",
        "Linha",
    ]
    for col in colunas_texto:
        df[col] = df[col].astype(str).str.strip()

    df = df.rename(
        columns={
            "calendarioData": "data",
            "Documento": "documento",
            "Código": "codigo_cliente",
            "Cliente": "cliente",
            "CNPJ": "cnpj",
            "SKU": "sku",
            "Descrição": "descricao",
            "Fabricante": "fabricante",
            "Linha": "linha",
            "Qtd.": "quantidade",
            "Venda": "venda_bruta",
            "Venda Líquida": "venda_liquida",
            "Lucro": "lucro",
        }
    )

    df = df.dropna(subset=["data"]).copy()

    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["dia"] = df["data"].dt.day
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)

    return df


def preprocessar_giro(df: pd.DataFrame) -> pd.DataFrame:
    colunas_obrigatorias = [
        "Fabricante",
        "Linha",
        "Grupo",
        "Código",
        "Descrição",
        "ESA Atual",
        "Status",
        "Estoque atual",
        "Clientes",
        "Ul. Venda",
        "Dias Ul. Venda",
        "Q. Vendas Período",
    ]
    _validar_colunas(df, colunas_obrigatorias, "giro")

    df = df.copy()

    colunas_texto = [
        "Fabricante",
        "Linha",
        "Grupo",
        "Código",
        "Descrição",
        "ESA Atual",
        "Status",
        "Ul. Venda",
    ]
    for col in colunas_texto:
        df[col] = df[col].astype(str).str.strip()

    df = df.replace("-", pd.NA)

    colunas_numericas = [
        "Estoque atual",
        "Clientes",
        "Dias Ul. Venda",
        "Q. Vendas Período",
    ]
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.rename(
        columns={
            "Fabricante": "fabricante",
            "Linha": "linha",
            "Grupo": "grupo",
            "Código": "sku",
            "Descrição": "descricao",
            "ESA Atual": "esa_atual",
            "Status": "status",
            "Estoque atual": "estoque_atual",
            "Clientes": "clientes",
            "Ul. Venda": "ultima_venda",
            "Dias Ul. Venda": "dias_ultima_venda",
            "Q. Vendas Período": "qtd_vendas_periodo",
        }
    )

    return df
