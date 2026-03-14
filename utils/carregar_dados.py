from io import BytesIO
import pandas as pd


def carregar_arquivo(arquivo):
    nome = arquivo.name.lower()
    conteudo = arquivo.read()

    if nome.endswith(".csv"):
        try:
            return pd.read_csv(BytesIO(conteudo), sep=None, engine="python")
        except Exception:
            return pd.read_csv(BytesIO(conteudo), sep=";")
    elif nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(BytesIO(conteudo))
    else:
        raise ValueError("Formato de arquivo não suportado.")
