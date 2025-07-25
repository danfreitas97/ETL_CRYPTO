# 📈 Projeto ETL de Criptomoedas com Análise Técnica

Este projeto realiza o processo completo de **ETL (Extração, Transformação e Carga)** de dados históricos de criptomoedas e apresenta os resultados em um **dashboard interativo** via Streamlit.

Os dados são coletados automaticamente da API pública da [CoinGecko](https://www.coingecko.com/), processados com indicadores técnicos como **médias móveis** e **volatilidade**, e apresentados com gráficos claros e informativos.

---

## 💡 Objetivo

Criar um pipeline 100% automatizado que:

1. **Baixa os dados** das 10 maiores criptomoedas (últimos 365 dias)
2. **Transforma** os dados com cálculo de indicadores técnicos
3. **Armazena** os dados processados em formato otimizado (Parquet)
4. **Exibe** os dados em um **dashboard web interativo** com:
   - Gráfico de preços com médias móveis
   - Volatilidade por janela de tempo
   - Retorno diário acumulado
   - Heatmap de correlação entre moedas
   - Explicações contextualizadas para cada gráfico

---

## ▶️ Como rodar o projeto

### 🔹 Pré-requisitos

- Docker e Docker Compose instalados

### 🔹 Passos

1. Clone o repositório:

2. Rode o projeto com:

   ```
   docker-compose up --build
   ```

3. Aguarde cerca de 5 minutos enquanto os dados são baixados (API Rate Limit), e 10 seg enquanto transformados e carregados.

4. Acesse o dashboard no navegador:
   [http://localhost:8501](http://localhost:8501)

---

## 📊 O que você verá no dashboard

- **Preço e Médias Móveis:** evolução dos preços com tendência suavizada
- **Volatilidade:** análise de risco por janelas móveis
- **Retorno Diário:** variação percentual acumulada
- **Correlação entre moedas:** heatmap para entender relação entre os criptoativos
- **Legendas explicativas abaixo dos títulos dos gráficos**

---

## ℹ️ Observações

- A CoinGecko limita a API gratuita a **100 requisições por minuto**
- O projeto já respeita esse limite com `sleep` inteligente
- Os dados são atualizados automaticamente ao iniciar o container
