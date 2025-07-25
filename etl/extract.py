import requests
import pandas as pd
from pathlib import Path
import time

DAYS = 365
CURRENCY = "brl"
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_top_10_coin_ids():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": CURRENCY,
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise Exception(f"Erro ao buscar top 10: {r.status_code} - {r.text}")
    data = r.json()
    return [coin["id"] for coin in data]


def fetch_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": CURRENCY, "days": str(DAYS)}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise Exception(f"[{coin_id}] Erro na API: {r.status_code} - {r.text}")
    data = r.json()
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def main():
    coins = get_top_10_coin_ids()
    print(f"[INFO] Top 10 moedas: {coins}")

    for coin in coins:
        output_file = OUTPUT_DIR / f"{coin}_{DAYS}d.csv"

        print(f"[INFO] Baixando dados de {coin}...")
        df = fetch_coin_data(coin)
        df.to_csv(output_file, index=False)
        print(f"[OK] {coin} salvo em {output_file.name}")
        # Devido o Rate Limit da Coin Gecko de 100 requisições por minuto
        time.sleep(30)


if __name__ == "__main__":
    main()
