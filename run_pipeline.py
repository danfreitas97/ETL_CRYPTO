import subprocess
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ETL_DIR = os.path.join(BASE_DIR, "etl")
DASHBOARD_PATH = os.path.join(BASE_DIR, "dashboard", "app.py")


def run_step(description, script_path, wait_after=0):
    print(f"\n📦 Iniciando: {description}")
    try:
        process = subprocess.Popen(
            ["python", script_path],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, script_path)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script_path}: {e}")
        exit(1)

    if wait_after > 0:
        print(f"⏳ Aguardando {wait_after} segundos...")
        time.sleep(wait_after)


if __name__ == "__main__":
    print("\n🚀 Iniciando pipeline ETL")
    print("\n⏱️ Download iniciando. Levará 5 minutos devido Rate Limit da API. Aguarde.")

    run_step("Extração de dados da API CoinGecko",
             os.path.join(ETL_DIR, "extract.py"))
    run_step("Transformação dos dados", os.path.join(
        ETL_DIR, "transform.py"), wait_after=3)
    run_step("Carga dos dados em Parquet", os.path.join(
        ETL_DIR, "load.py"), wait_after=3)

    print("\n✅ Pipeline concluído com sucesso!")
