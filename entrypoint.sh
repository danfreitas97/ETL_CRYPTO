#!/bin/bash

echo "Iniciando..."
python run_pipeline.py

echo "📊 Iniciando dashboard Streamlit..."
streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0
