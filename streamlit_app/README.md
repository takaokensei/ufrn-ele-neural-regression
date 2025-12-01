# 🏠 Streamlit App - Boston Housing Neural Regression

Aplicação web interativa para demonstração do modelo de regressão neural treinado no Boston Housing Dataset.

## 🚀 Como Executar

### Localmente

1. **Instalar dependências:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Executar a aplicação:**
   ```bash
   streamlit run streamlit_app/app.py
   ```

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
├── app.py              # Arquivo principal
├── pages/              # Páginas da aplicação
│   ├── 1_🏠_Predição.py
│   ├── 2_📊_Métricas.py
│   ├── 3_🔍_Análise.py
│   └── 4_📈_Dashboard.py
├── utils/              # Módulos utilitários
│   ├── model_loader.py
│   └── preprocessor.py
└── assets/
    └── model/
        └── best_model_fold.pth
```

## 🎯 Funcionalidades

- ✅ Predição interativa de preços
- ✅ Visualização de métricas de performance
- ✅ Análise de correlação de features
- ✅ Dashboard com learning curves e gráficos

## 📝 Notas

- O modelo deve estar em `models/best_model_fold.pth` ou `streamlit_app/assets/model/best_model_fold.pth`
- A aplicação usa cache para melhor performance
- Todas as visualizações são interativas (Plotly)

