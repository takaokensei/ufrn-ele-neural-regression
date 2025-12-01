"""
Página de Análise de Features
Mostra correlações e importância das features
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys
from pathlib import Path

st.set_page_config(
    page_title="Análise de Features - Boston Housing",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Análise de Features")
st.markdown("Explore a importância e correlação das features com o preço (MEDV)")

# Top Correlações
st.markdown("### 📊 Top 5 Correlações com MEDV")

col1, col2 = st.columns(2)

# Top 5 Positivas
top_positive = [
    ("RM", 0.70, "Número médio de quartos"),
    ("ZN", 0.36, "Terrenos residenciais zoneados"),
    ("B", 0.33, "Proporção de negros por cidade"),
    ("DIS", 0.25, "Distância aos centros de emprego"),
    ("CHAS", 0.18, "Limita com rio Charles")
]

# Top 5 Negativas
top_negative = [
    ("LSTAT", -0.74, "% de população de baixa renda"),
    ("PTRATIO", -0.51, "Razão aluno-professor"),
    ("INDUS", -0.48, "Acres comerciais não-varejo"),
    ("TAX", -0.47, "Taxa de imposto sobre propriedade"),
    ("NOX", -0.43, "Concentração de óxidos de nitrogênio")
]

with col1:
    st.markdown("#### ✅ Correlações Positivas")
    for feature, corr, desc in top_positive:
        st.markdown(f"""
        **{feature}** ({corr:+.2f})  
        *{desc}*
        """)
        st.progress(corr)

with col2:
    st.markdown("#### ❌ Correlações Negativas")
    for feature, corr, desc in top_negative:
        st.markdown(f"""
        **{feature}** ({corr:+.2f})  
        *{desc}*
        """)
        st.progress(abs(corr))

# Matriz de Correlação
st.markdown("---")
st.markdown("### 🔥 Matriz de Correlação de Pearson")

# Carregar matriz de correlação (valores aproximados do dataset)
feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

# Matriz de correlação simplificada (valores principais)
correlation_matrix = np.array([
    [1.00, -0.20, 0.41, -0.06, 0.42, -0.22, 0.35, -0.38, 0.63, 0.58, 0.29, -0.39, 0.46, -0.39],
    [-0.20, 1.00, -0.53, -0.04, -0.52, 0.31, -0.57, 0.66, -0.31, -0.31, -0.39, 0.18, -0.41, 0.36],
    [0.41, -0.53, 1.00, 0.06, 0.76, -0.39, 0.64, -0.71, 0.60, 0.72, 0.38, -0.36, 0.60, -0.48],
    [-0.06, -0.04, 0.06, 1.00, 0.09, 0.09, 0.09, -0.01, -0.01, -0.04, -0.12, 0.05, -0.05, 0.18],
    [0.42, -0.52, 0.76, 0.09, 1.00, -0.30, 0.73, -0.77, 0.61, 0.67, 0.19, -0.38, 0.59, -0.43],
    [-0.22, 0.31, -0.39, 0.09, -0.30, 1.00, -0.24, 0.21, -0.21, -0.29, -0.36, 0.13, -0.61, 0.70],
    [0.35, -0.57, 0.64, 0.09, 0.73, -0.24, 1.00, -0.75, 0.46, 0.51, 0.26, -0.27, 0.60, -0.38],
    [-0.38, 0.66, -0.71, -0.01, -0.77, 0.21, -0.75, 1.00, -0.49, -0.53, -0.23, 0.25, -0.50, 0.25],
    [0.63, -0.31, 0.60, -0.01, 0.61, -0.21, 0.46, -0.49, 1.00, 0.91, 0.46, -0.44, 0.49, -0.38],
    [0.58, -0.31, 0.72, -0.04, 0.67, -0.29, 0.51, -0.53, 0.91, 1.00, 0.46, -0.44, 0.54, -0.47],
    [0.29, -0.39, 0.38, -0.12, 0.19, -0.36, 0.26, -0.23, 0.46, 0.46, 1.00, -0.18, 0.37, -0.51],
    [-0.39, 0.18, -0.36, 0.05, -0.38, 0.13, -0.27, 0.25, -0.44, -0.44, -0.18, 1.00, -0.37, 0.33],
    [0.46, -0.41, 0.60, -0.05, 0.59, -0.61, 0.60, -0.50, 0.49, 0.54, 0.37, -0.37, 1.00, -0.74],
    [-0.39, 0.36, -0.48, 0.18, -0.43, 0.70, -0.38, 0.25, -0.38, -0.47, -0.51, 0.33, -0.74, 1.00]
])

# Criar heatmap interativo
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix,
    x=feature_names,
    y=feature_names,
    colorscale='RdBu',
    zmid=0,
    text=np.round(correlation_matrix, 2),
    texttemplate='%{text}',
    textfont={"size": 8},
    colorbar=dict(title="Correlação")
))

fig.update_layout(
    title="Matriz de Correlação de Pearson - Boston Housing Dataset",
    width=800,
    height=800,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# Legenda de Features
st.markdown("---")
st.markdown("### 📖 Legenda das Features")

feature_descriptions = {
    "CRIM": "Taxa de criminalidade per capita",
    "ZN": "Proporção de terrenos residenciais zoneados",
    "INDUS": "Proporção de acres comerciais não-varejo",
    "CHAS": "Limita com rio Charles (1=sim, 0=não)",
    "NOX": "Concentração de óxidos de nitrogênio",
    "RM": "Número médio de quartos por habitação",
    "AGE": "Proporção de unidades ocupadas construídas antes de 1940",
    "DIS": "Distância ponderada aos centros de emprego",
    "RAD": "Índice de acessibilidade a rodovias radiais",
    "TAX": "Taxa de imposto sobre propriedade",
    "PTRATIO": "Razão aluno-professor por cidade",
    "B": "Proporção de negros por cidade",
    "LSTAT": "% de população de baixa renda",
    "MEDV": "Preço mediano de casas (target)"
}

# Criar tabela
df_features = pd.DataFrame([
    {"Feature": k, "Descrição": v}
    for k, v in feature_descriptions.items()
])

st.dataframe(df_features, use_container_width=True, hide_index=True)

# Insight
st.markdown("---")
st.markdown("### 💡 Insight")

st.info("""
As correlações mais fortes (RM +0.70 e LSTAT -0.74) explicam a maior parte da 
variância do preço. Features socioeconômicas (LSTAT, PTRATIO, INDUS) têm impacto 
negativo consistente, enquanto características físicas (RM, número de quartos) 
têm impacto positivo.
""")

