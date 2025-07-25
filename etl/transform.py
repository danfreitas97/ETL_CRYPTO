import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Janelas móveis
WINDOWS = [7, 14, 30, 90, 180, 365]


def transform_coin_file(csv_path: Path):
    coin_id = csv_path.stem.split("_")[0]  # bitcoin_365d.csv → bitcoin
    df = pd.read_csv(csv_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Identificação
    df["coin"] = coin_id

    # Variação percentual diária
    df["pct_change"] = df["price"].pct_change()

    # Médias móveis e volatilidades móveis
    for w in WINDOWS:
        df[f"ma_{w}d"] = df["price"].rolling(window=w).mean()
        df[f"volatility_{w}d"] = df["price"].rolling(window=w).std()

    # Retornos
    df["cumulative_return"] = (1 + df["pct_change"]).cumprod() - 1

    df["return_from_start"] = (df["price"] / df["price"].iloc[0]) - 1

    df["daily_return"] = df["price"].pct_change()

    # Drawdown
    df["cummax"] = df["price"].cummax()
    df["drawdown"] = (df["price"] - df["cummax"]) / df["cummax"]

    # Salvar arquivo transformado
    output_path = PROCESSED_DIR / f"{coin_id}_transformed.csv"
    df.to_csv(output_path, index=False)
    print(f"[OK] Transformado: {coin_id} → {output_path.name}")

    return df


def transform_all():
    csv_files = list(RAW_DIR.glob("*_365d.csv"))
    if not csv_files:
        print("[ERRO] Nenhum arquivo encontrado em data/raw/")
        return

    for file in csv_files:
        transform_coin_file(file)


if __name__ == "__main__":
    transform_all()
