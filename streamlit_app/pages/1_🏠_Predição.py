"""
Página de Predição Interativa
Permite que o usuário insira features e obtenha predição de preço
"""

import streamlit as st
import torch
import time
import sys
from pathlib import Path

# Adicionar utils ao path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.model_loader import load_model, get_model_info
from utils.preprocessor import (
    preprocess_input, 
    validate_features, 
    get_feature_defaults,
    get_feature_ranges
)

# Configuração da página
st.set_page_config(
    page_title="Predição Interativa - Boston Housing",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predição de Preço de Imóveis")
st.markdown("Insira as características do imóvel para obter uma predição de preço em tempo real")

# Carregar modelo (com cache)
@st.cache_resource
def load_trained_model():
    """Carrega o modelo treinado (cacheado para performance)"""
    try:
        return load_model()
    except Exception as e:
        st.error(f"❌ Erro ao carregar modelo: {e}")
        st.stop()

# Carregar modelo
with st.spinner("🔄 Carregando modelo..."):
    model = load_trained_model()

# Obter informações do modelo
model_info = get_model_info()

# Exibir informações do modelo
with st.expander("ℹ️ Informações do Modelo", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("R²", f"{model_info.get('r2', 'N/A'):.3f}" if isinstance(model_info.get('r2'), (int, float)) else "N/A")
    with col2:
        st.metric("MSE", f"{model_info.get('mse', 'N/A'):.2f}" if isinstance(model_info.get('mse'), (int, float)) else "N/A")
    with col3:
        st.metric("Fold", f"{model_info.get('fold', 'N/A')}")

# Obter defaults e ranges
defaults = get_feature_defaults()
ranges = get_feature_ranges()

# Feature descriptions
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
    "LSTAT": "% de população de baixa renda"
}

# Formulário de input
st.markdown("### 📝 Características do Imóvel")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    features = {}
    
    with col1:
        st.markdown("#### Características Demográficas e Sociais")
        features['CRIM'] = st.slider(
            f"**CRIM** - {feature_descriptions['CRIM']}",
            min_value=float(ranges['CRIM'][0]),
            max_value=float(ranges['CRIM'][1]),
            value=float(defaults['CRIM']),
            step=0.1,
            help="Taxa de criminalidade per capita"
        )
        
        features['ZN'] = st.slider(
            f"**ZN** - {feature_descriptions['ZN']}",
            min_value=float(ranges['ZN'][0]),
            max_value=float(ranges['ZN'][1]),
            value=float(defaults['ZN']),
            step=0.1
        )
        
        features['INDUS'] = st.slider(
            f"**INDUS** - {feature_descriptions['INDUS']}",
            min_value=float(ranges['INDUS'][0]),
            max_value=float(ranges['INDUS'][1]),
            value=float(defaults['INDUS']),
            step=0.1
        )
        
        features['CHAS'] = st.selectbox(
            f"**CHAS** - {feature_descriptions['CHAS']}",
            options=[0.0, 1.0],
            index=0,
            format_func=lambda x: "Sim" if x == 1.0 else "Não"
        )
        
        features['NOX'] = st.slider(
            f"**NOX** - {feature_descriptions['NOX']}",
            min_value=float(ranges['NOX'][0]),
            max_value=float(ranges['NOX'][1]),
            value=float(defaults['NOX']),
            step=0.001,
            format="%.3f"
        )
        
        features['RM'] = st.slider(
            f"**RM** - {feature_descriptions['RM']}",
            min_value=float(ranges['RM'][0]),
            max_value=float(ranges['RM'][1]),
            value=float(defaults['RM']),
            step=0.1,
            help="Número médio de quartos (correlação positiva forte com preço)"
        )
        
        features['AGE'] = st.slider(
            f"**AGE** - {feature_descriptions['AGE']}",
            min_value=float(ranges['AGE'][0]),
            max_value=float(ranges['AGE'][1]),
            value=float(defaults['AGE']),
            step=0.1
        )
    
    with col2:
        st.markdown("#### Características de Localização e Infraestrutura")
        features['DIS'] = st.slider(
            f"**DIS** - {feature_descriptions['DIS']}",
            min_value=float(ranges['DIS'][0]),
            max_value=float(ranges['DIS'][1]),
            value=float(defaults['DIS']),
            step=0.1
        )
        
        features['RAD'] = st.slider(
            f"**RAD** - {feature_descriptions['RAD']}",
            min_value=float(ranges['RAD'][0]),
            max_value=float(ranges['RAD'][1]),
            value=float(defaults['RAD']),
            step=1.0
        )
        
        features['TAX'] = st.slider(
            f"**TAX** - {feature_descriptions['TAX']}",
            min_value=float(ranges['TAX'][0]),
            max_value=float(ranges['TAX'][1]),
            value=float(defaults['TAX']),
            step=1.0
        )
        
        features['PTRATIO'] = st.slider(
            f"**PTRATIO** - {feature_descriptions['PTRATIO']}",
            min_value=float(ranges['PTRATIO'][0]),
            max_value=float(ranges['PTRATIO'][1]),
            value=float(defaults['PTRATIO']),
            step=0.1,
            help="Razão aluno-professor (correlação negativa com preço)"
        )
        
        features['B'] = st.slider(
            f"**B** - {feature_descriptions['B']}",
            min_value=float(ranges['B'][0]),
            max_value=float(ranges['B'][1]),
            value=float(defaults['B']),
            step=0.1
        )
        
        features['LSTAT'] = st.slider(
            f"**LSTAT** - {feature_descriptions['LSTAT']}",
            min_value=float(ranges['LSTAT'][0]),
            max_value=float(ranges['LSTAT'][1]),
            value=float(defaults['LSTAT']),
            step=0.1,
            help="% de população de baixa renda (correlação negativa mais forte)"
        )
    
    submitted = st.form_submit_button("🔮 Prever Preço", use_container_width=True)
    
    if submitted:
        # Converter features para lista na ordem correta
        feature_order = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                        'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
        features_list = [features[f] for f in feature_order]
        
        # Validar features
        is_valid, error_msg = validate_features(features_list)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
        else:
            # Pré-processar input
            with st.spinner("🔄 Processando..."):
                start_time = time.time()
                features_tensor = preprocess_input(features_list)
                
                # Predição
                with torch.no_grad():
                    prediction = model(features_tensor)
                    price = prediction.item() * 1000  # Converter para milhares de dólares
                
                elapsed_time = (time.time() - start_time) * 1000  # em ms
            
            # Exibir resultado
            st.markdown("---")
            st.markdown("### 💰 Resultado da Predição")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.metric(
                    "Preço Predito",
                    f"${price:,.2f}",
                    help="Preço em milhares de dólares (k$)"
                )
            
            with col2:
                st.metric(
                    "Tempo de Predição",
                    f"{elapsed_time:.2f} ms",
                    help="Tempo de execução da predição"
                )
            
            with col3:
                avg_price = 22.5  # Preço médio do dataset em k$
                diff = price - avg_price
                st.metric(
                    "vs. Média",
                    f"{diff:+.2f} k$",
                    help="Diferença em relação ao preço médio do dataset"
                )
            
            # Comparação visual
            st.progress(min(max(price / 50.0, 0.0), 1.0))  # Normalizar para 0-1 (assumindo max ~50k)
            st.caption(f"Preço médio do dataset: ~$22.5k | Range típico: $5k - $50k")

# Seção de Testes Rápidos
st.markdown("---")
st.markdown("### 🚀 Testes Rápidos")

col1, col2, col3 = st.columns(3)

# Cenários pré-configurados
scenarios = {
    "Premium": {
        "CRIM": 0.1, "ZN": 25.0, "INDUS": 2.0, "CHAS": 1.0, "NOX": 0.4,
        "RM": 7.5, "AGE": 10.0, "DIS": 5.0, "RAD": 3.0, "TAX": 250.0,
        "PTRATIO": 15.0, "B": 395.0, "LSTAT": 2.0
    },
    "Econômico": {
        "CRIM": 10.0, "ZN": 0.0, "INDUS": 20.0, "CHAS": 0.0, "NOX": 0.7,
        "RM": 5.5, "AGE": 90.0, "DIS": 2.0, "RAD": 20.0, "TAX": 600.0,
        "PTRATIO": 20.0, "B": 200.0, "LSTAT": 30.0
    },
    "Médio": defaults
}

with col1:
    if st.button("🏆 Imóvel Premium", use_container_width=True):
        st.session_state.scenario = "Premium"
        st.rerun()

with col2:
    if st.button("💼 Imóvel Econômico", use_container_width=True):
        st.session_state.scenario = "Econômico"
        st.rerun()

with col3:
    if st.button("📊 Imóvel Médio", use_container_width=True):
        st.session_state.scenario = "Médio"
        st.rerun()

# Aplicar cenário se selecionado
if 'scenario' in st.session_state:
    scenario_name = st.session_state.scenario
    scenario_features = scenarios[scenario_name]
    st.info(f"✅ Cenário '{scenario_name}' aplicado. Ajuste os valores acima e clique em 'Prever Preço'.")

