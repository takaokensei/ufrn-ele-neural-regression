#!/bin/bash
# Script para executar Streamlit com venv ativado (Linux/Mac)
echo "Ativando ambiente virtual..."
source venv/bin/activate
echo "Iniciando Streamlit..."
streamlit run streamlit_app/app.py

