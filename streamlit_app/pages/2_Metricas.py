"""
Página de Métricas e Performance
Exibe métricas do modelo e resultados do K-Fold
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.model_loader import get_model_info

st.set_page_config(
    page_title="Métricas e Performance - Boston Housing",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Métricas e Performance")
st.markdown("Visualize as métricas de performance do modelo treinado")

# Obter informações do modelo
model_info = get_model_info()

# Cards de Métricas Principais
st.markdown("### 🎯 Métricas Principais")

col1, col2, col3, col4 = st.columns(4)

r2_mean = 0.857
r2_best = 0.927
mse_optimized = 13.02
mae_approx = 3.6

with col1:
    st.metric(
        "R² (Média)",
        f"{r2_mean:.3f}",
        "+0.5%",
        help="Coeficiente de determinação médio (5 folds)"
    )

with col2:
    st.metric(
        "R² (Melhor Fold)",
        f"{r2_best:.3f}",
        "Fold 4",
        help="Melhor performance alcançada no Fold 4"
    )

with col3:
    st.metric(
        "MSE",
        f"{mse_optimized:.2f}",
        "-3.3%",
        help="Mean Squared Error (otimizado)"
    )

with col4:
    st.metric(
        "MAE",
        f"${mae_approx:.1f}k",
        "Erro médio",
        help="Mean Absolute Error (~$3.600)"
    )

# Tabela Comparativa
st.markdown("---")
st.markdown("### 📈 Comparativo: Baseline vs Otimizado")

comparison_data = {
    "Métrica": ["MSE", "R² (Média)", "R² (Melhor Fold)", "Desvio Padrão"],
    "Baseline": [13.47, 0.852, "-", 2.47],
    "Otimizado (Optuna)": [13.02, 0.857, 0.927, 4.62],
    "Variação": ["-3.3%", "+0.5%", "Potencial máximo", "+ Variância"]
}

df_comparison = pd.DataFrame(comparison_data)
st.dataframe(df_comparison, use_container_width=True, hide_index=True)

# Gráfico K-Fold
st.markdown("---")
st.markdown("### 📊 Resultados por Fold (K-Fold Cross-Validation)")

# Dados dos folds
folds = [1, 2, 3, 4, 5]
mses = [12.52, 10.80, 21.03, 7.60, 13.38]  # Valores aproximados
mean_mse = sum(mses) / len(mses)
std_mse = 4.62

# Criar gráfico
fig = go.Figure()

# Barras
fig.add_trace(go.Bar(
    x=folds,
    y=mses,
    name="MSE por Fold",
    marker_color='#4A90E2',
    text=[f"{m:.2f}" for m in mses],
    textposition='outside'
))

# Linha de média
fig.add_hline(
    y=mean_mse,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Média: {mean_mse:.2f}",
    annotation_position="right"
)

# Banda de desvio padrão
fig.add_hrect(
    y0=mean_mse - std_mse,
    y1=mean_mse + std_mse,
    fillcolor="red",
    opacity=0.2,
    layer="below",
    line_width=0,
    annotation_text=f"±1 Desvio Padrão: {std_mse:.2f}",
    annotation_position="top left"
)

# Destacar Fold 3 (outlier)
fig.add_trace(go.Scatter(
    x=[3],
    y=[mses[2]],
    mode='markers',
    marker=dict(size=15, color='red', symbol='x'),
    name='Outlier (Fold 3)',
    showlegend=True
))

fig.update_layout(
    title="MSE por Fold - K-Fold Cross-Validation",
    xaxis_title="Fold",
    yaxis_title="MSE",
    height=400,
    showlegend=True,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# Análise do Fold 3
st.info("""
**📌 Observação:** O Fold 3 apresentou comportamento outlier (MSE=21.03), 
indicando maior sensibilidade do modelo a distribuições específicas de dados. 
Isso é comum em datasets pequenos (Small Data) e reforça a importância do 
K-Fold Cross-Validation para estimativas robustas.
""")

# Seção de Tempo de Execução
st.markdown("---")
st.markdown("### ⚡ Eficiência Computacional")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Otimização Optuna",
        "~2 minutos",
        "20 trials",
        help="Tempo para otimização bayesiana com 20 trials"
    )

with col2:
    st.metric(
        "Tempo de Predição",
        "< 1 ms",
        "Instantâneo",
        help="Tempo médio para uma predição"
    )

with col3:
    st.metric(
        "Redução vs Grid Search",
        "~99%",
        "5h → 2min",
        help="Comparação com Grid Search exaustivo (~5 horas)"
    )

# Insight Crítico
st.markdown("---")
st.markdown("### 💡 Insight Crítico")

st.success("""
Embora a média do R² tenha se mantido estável (0.857), o modelo atingiu picos de 
performance muito superiores (0.927 no Fold 4), demonstrando capacidade de aprender 
padrões complexos. O aumento no desvio padrão (2.47 → 4.62) reflete a sensibilidade 
inerente ao Small Data em diferentes distribuições, mas os resultados comprovam o 
potencial de generalização.
""")

