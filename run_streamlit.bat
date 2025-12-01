@echo off
REM Script para executar Streamlit com venv ativado (Windows)
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo Iniciando Streamlit...
streamlit run streamlit_app/app.py
pause

