"""
Aplicação Streamlit Principal
Boston Housing Dataset - Regressão Neural
UFRN - ELE 604
"""

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Boston Housing - Neural Regression",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏠 Análise de Generalização em Redes Neurais")
st.markdown("### Regressão de Preços - Boston Housing Dataset")
st.markdown("**UFRN - Engenharia Elétrica - ELE 604**")

# Sidebar
st.sidebar.title("📊 Navegação")
st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📋 Sobre o Projeto

Este projeto demonstra técnicas de **MLOps** e **Otimização Bayesiana** 
aplicadas a regressão neural no dataset Boston Housing.

**Tecnologias:**
- PyTorch
- Optuna (Bayesian Optimization)
- K-Fold Cross-Validation
- Streamlit

**Autor:** Cauã Vitor Figueredo Silva  
**Orientador:** Prof. Dr. Allan de Medeiros Martins
""")

st.sidebar.markdown("---")

# Páginas disponíveis
st.sidebar.markdown("### 🎯 Páginas Disponíveis")
st.sidebar.markdown("""
1. 🏠 **Predição Interativa** - Teste o modelo com seus próprios valores
2. 📊 **Métricas e Performance** - Visualize resultados do modelo
3. 🔍 **Análise de Features** - Explore correlações e importância
4. 📈 **Dashboard Visual** - Gráficos e visualizações avançadas
""")

# Conteúdo principal
st.markdown("---")
st.markdown("### 👋 Bem-vindo!")

st.markdown("""
Esta aplicação permite interagir com o modelo de regressão neural treinado 
no **Boston Housing Dataset**. Use a navegação lateral para acessar as diferentes funcionalidades.

#### 🚀 Funcionalidades:

- **Predição em Tempo Real:** Insira características de um imóvel e obtenha uma predição de preço instantânea
- **Análise de Performance:** Visualize métricas como R², MSE e resultados do K-Fold
- **Exploração de Features:** Entenda quais características mais impactam o preço
- **Visualizações Interativas:** Gráficos interativos de learning curves e predições

#### 📊 Modelo Treinado:

- **Arquitetura:** MLP (Multi-Layer Perceptron)
- **R² (Média):** 0.857
- **R² (Melhor Fold):** 0.927
- **MSE:** 13.02
- **Otimização:** Optuna (Bayesian Optimization)
""")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>Desenvolvido para a disciplina ELE 604 - Redes Neurais Artificiais</p>
    <p>UFRN - Novembro 2025</p>
</div>
""", unsafe_allow_html=True)

