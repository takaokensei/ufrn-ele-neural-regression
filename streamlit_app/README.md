# 🏠 Streamlit App - Boston Housing Neural Regression

Aplicação web interativa para demonstração do modelo de regressão neural treinado no Boston Housing Dataset.

## 🚀 Como Executar

### Localmente

1. **Instalar dependências:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Ativar ambiente virtual (Windows):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Ou (Linux/Mac):**
   ```bash
   source venv/bin/activate
   ```

3. **Executar a aplicação:**
   ```bash
   streamlit run streamlit_app/app.py
   ```
   
   **Importante:** Certifique-se de que o ambiente virtual está ativado para que o PyTorch e outras dependências estejam disponíveis.

3. **Acessar no navegador:**
   - URL padrão: http://localhost:8501

### Deploy no Streamlit Cloud

1. Fazer push do código para GitHub
2. Acessar https://streamlit.io/cloud
3. Conectar repositório
4. Configurar:
   - **Main file path:** `streamlit_app/app.py`
   - **Python version:** 3.12
   - **Dependencies file:** `requirements_streamlit.txt`

## 📁 Estrutura

```
streamlit_app/
├── app.py              # Arquivo principal (aplicação centralizada)
├── pages/              # Páginas da aplicação (não mais usadas - integradas no app.py)
│   ├── 1_Predicao.py
│   ├── 2_Metricas.py
│   ├── 3_Analise.py
│   └── 4_Dashboard.py
├── utils/              # Módulos utilitários
│   ├── model_loader.py
│   └── preprocessor.py
└── assets/
    └── model/
        └── best_model_fold.pth
```

**Nota:** A aplicação agora usa `app.py` centralizado com todas as páginas integradas via navegação na sidebar.

## 🎯 Funcionalidades

- ✅ Predição interativa de preços
- ✅ Visualização de métricas de performance
- ✅ Análise de correlação de features
- ✅ Dashboard com learning curves e gráficos

## 📝 Notas

- O modelo deve estar em `models/best_model_fold.pth` ou `streamlit_app/assets/model/best_model_fold.pth`
- A aplicação usa cache para melhor performance
- Todas as visualizações são interativas (Plotly)

