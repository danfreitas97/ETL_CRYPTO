import subprocess
import time
import sys


def run_step(description, script, wait_after=0):
    print(f"\n📦 Iniciando: {description}")
    try:
        process = subprocess.Popen(
            ["python", script],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, script)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script}: {e}")
        exit(1)

    if wait_after > 0:
        print(f"⏳ Aguardando {wait_after} segundos...")
        time.sleep(wait_after)


if __name__ == "__main__":
    print("\n🚀 Iniciando pipeline ETL")

    print("\n⏱️ Download iniciando. Levará 5 minutos devido Rate Limit da API. Aguarde.")

    run_step("Extração de dados da API CoinGecko", "etl/extract.py")
    run_step("Transformação dos dados", "etl/transform.py", wait_after=3)
    run_step("Carga dos dados em Parquet", "etl/load.py", wait_after=3)

    print("\n✅ Pipeline concluído com sucesso!")
