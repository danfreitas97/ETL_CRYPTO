import pandas as pd
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_CSV = PROCESSED_DIR / "all_coins.csv"
OUTPUT_PARQUET = PROCESSED_DIR / "all_coins.parquet"


def load_all_transformed():
    files = list(PROCESSED_DIR.glob("*_transformed.csv"))
    if not files:
        print("[ERRO] Nenhum arquivo transformado encontrado.")
        return

    dfs = []
    for file in files:
        df = pd.read_csv(file)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)
    print(f"[INFO] Total de registros combinados: {len(full_df)}")

    # Salvar CSV
    full_df.to_csv(OUTPUT_CSV, index=False)
    print(f"[OK] all_coins.csv salvo em: {OUTPUT_CSV}")

    # Salvar como Parquet
    full_df.to_parquet(OUTPUT_PARQUET, index=False)
    print(f"[OK] all_coins.parquet salvo em: {OUTPUT_PARQUET}")


if __name__ == "__main__":
    load_all_transformed()
