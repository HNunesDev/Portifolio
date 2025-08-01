import os
import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# ============== Funções ==============

def extrair_precos(moedas, moeda_base="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": moedas, "vs_currencies": moeda_base}

    r = requests.get(url, params=params)
    df = pd.DataFrame(r.json()).T
    df.reset_index(inplace=True)
    df.columns = ["moeda", "preco_usd"]
    df["data"] = dt.date.today()
    return df


def transformar_dados(df):
    return df.sort_values(by="preco_usd", ascending=False).reset_index(drop=True)


def salvar_csv(df, arquivo):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    if os.path.exists(arquivo):
        df.to_csv(arquivo, mode='a', header=False, index=False)
    else:
        df.to_csv(arquivo, index=False)


def plotar_precos(df):
    plt.figure(figsize=(8, 4))
    plt.bar(df["moeda"], df["preco_usd"], color="skyblue")
    plt.xlabel("Criptomoeda")
    plt.ylabel("Preço em USD")
    plt.title(f"Preços em {dt.date.today()}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ============== ETL ==============
moedas = "bitcoin,ethereum,solana,ripple,0chain"
arquivo = "Portifolio\ETL_cripto/precos_cripto.csv"

# Extracao
df = extrair_precos(moedas)

# Transformacao
df = transformar_dados(df)

# Salvando
salvar_csv(df, arquivo)

# Visualização basica
print("Criptos e preços extraídos:")
print(df)
plotar_precos(df)
