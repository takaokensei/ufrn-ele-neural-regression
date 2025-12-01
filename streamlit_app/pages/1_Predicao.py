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

# Carregar modelo (com cache, mas verificando se checkpoint existe)
@st.cache_resource
def load_trained_model():
    """Carrega o modelo treinado (cacheado para performance)"""
    try:
        from pathlib import Path
        import os
        
        # Verificar caminho do checkpoint
        base_path = Path(__file__).parent.parent.parent
        checkpoint_path = base_path / "models" / "best_model_fold.pth"
        
        if not os.path.exists(checkpoint_path):
            st.error(f"❌ Checkpoint não encontrado em: {checkpoint_path}")
            st.info("💡 Certifique-se de que o modelo foi treinado e salvo executando o notebook.")
            st.stop()
        
        return load_model()
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar modelo: {e}")
        st.info("💡 Certifique-se de que o modelo foi treinado e salvo executando o notebook.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro inesperado ao carregar modelo: {e}")
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

# Inicializar session_state para features
if 'feature_values' not in st.session_state:
    st.session_state.feature_values = defaults.copy()
if 'scenario_selected' not in st.session_state:
    st.session_state.scenario_selected = None

# Cenários pré-configurados (valores alinhados com os steps dos sliders)
scenarios = {
    "Premium": {
        "CRIM": round(0.1, 1), "ZN": round(25.0, 1), "INDUS": round(2.0, 1), 
        "CHAS": 1.0, "NOX": round(0.4, 3), "RM": round(7.5, 1), 
        "AGE": round(10.0, 1), "DIS": round(5.0, 1), "RAD": 3.0, 
        "TAX": 250.0, "PTRATIO": round(15.0, 1), "B": round(395.0, 1), 
        "LSTAT": round(2.0, 1)
    },
    "Econômico": {
        "CRIM": round(10.0, 1), "ZN": 0.0, "INDUS": round(20.0, 1), 
        "CHAS": 0.0, "NOX": round(0.7, 3), "RM": round(5.5, 1), 
        "AGE": round(90.0, 1), "DIS": round(2.0, 1), "RAD": 20.0, 
        "TAX": 600.0, "PTRATIO": round(20.0, 1), "B": round(200.0, 1), 
        "LSTAT": round(30.0, 1)
    },
    "Médio": defaults
}

# Seção de Testes Rápidos (ANTES dos sliders)
st.markdown("### 🚀 Testes Rápidos")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏆 Imóvel Premium", use_container_width=True, key="btn_premium_page"):
        st.session_state.feature_values = scenarios["Premium"].copy()
        st.session_state.scenario_selected = "Premium"
        st.rerun()

with col2:
    if st.button("💼 Imóvel Econômico", use_container_width=True, key="btn_economico_page"):
        st.session_state.feature_values = scenarios["Econômico"].copy()
        st.session_state.scenario_selected = "Econômico"
        st.rerun()

with col3:
    if st.button("📊 Imóvel Médio", use_container_width=True, key="btn_medio_page"):
        st.session_state.feature_values = scenarios["Médio"].copy()
        st.session_state.scenario_selected = "Médio"
        st.rerun()

# Mostrar qual cenário está ativo
if st.session_state.scenario_selected:
    scenario_name = st.session_state.scenario_selected
    st.success(f"✅ Cenário **{scenario_name}** aplicado! Os valores dos sliders foram atualizados abaixo.")
    # Limpar flag após mostrar
    st.session_state.scenario_selected = None

# Formulário de input (SEM form para permitir atualização dinâmica)
st.markdown("---")
st.markdown("### 📝 Características do Imóvel")

# Usar valores do session_state se um cenário foi selecionado, senão usar defaults
scenario_key = st.session_state.scenario_selected if st.session_state.scenario_selected else "default"
current_values = st.session_state.feature_values

col1, col2 = st.columns(2)

features = {}

with col1:
    st.markdown("#### Características Demográficas e Sociais")
    features['CRIM'] = st.slider(
        f"**CRIM** - {feature_descriptions['CRIM']}",
        min_value=float(ranges['CRIM'][0]),
        max_value=float(ranges['CRIM'][1]),
        value=float(current_values.get('CRIM', defaults['CRIM'])),
        step=0.1,
        help="Taxa de criminalidade per capita",
        key=f"slider_CRIM_page_{scenario_key}"
    )
        
    features['ZN'] = st.slider(
        f"**ZN** - {feature_descriptions['ZN']}",
        min_value=float(ranges['ZN'][0]),
        max_value=float(ranges['ZN'][1]),
        value=float(current_values.get('ZN', defaults['ZN'])),
        step=0.1,
        key=f"slider_ZN_page_{scenario_key}"
    )
    
    features['INDUS'] = st.slider(
        f"**INDUS** - {feature_descriptions['INDUS']}",
        min_value=float(ranges['INDUS'][0]),
        max_value=float(ranges['INDUS'][1]),
        value=float(current_values.get('INDUS', defaults['INDUS'])),
        step=0.1,
        key=f"slider_INDUS_page_{scenario_key}"
    )
    
    chas_value = current_values.get('CHAS', defaults['CHAS'])
    chas_index = 1 if chas_value == 1.0 else 0
    features['CHAS'] = st.selectbox(
        f"**CHAS** - {feature_descriptions['CHAS']}",
        options=[0.0, 1.0],
        index=chas_index,
        format_func=lambda x: "Sim" if x == 1.0 else "Não",
        key=f"select_CHAS_page_{scenario_key}"
    )
    
    features['NOX'] = st.slider(
        f"**NOX** - {feature_descriptions['NOX']}",
        min_value=float(ranges['NOX'][0]),
        max_value=float(ranges['NOX'][1]),
        value=float(current_values.get('NOX', defaults['NOX'])),
        step=0.001,
        format="%.3f",
        key=f"slider_NOX_page_{scenario_key}"
    )
    
    features['RM'] = st.slider(
        f"**RM** - {feature_descriptions['RM']}",
        min_value=float(ranges['RM'][0]),
        max_value=float(ranges['RM'][1]),
        value=float(current_values.get('RM', defaults['RM'])),
        step=0.1,
        help="Número médio de quartos (correlação positiva forte com preço)",
        key=f"slider_RM_page_{scenario_key}"
    )
    
    features['AGE'] = st.slider(
        f"**AGE** - {feature_descriptions['AGE']}",
        min_value=float(ranges['AGE'][0]),
        max_value=float(ranges['AGE'][1]),
        value=float(current_values.get('AGE', defaults['AGE'])),
        step=0.1,
        key=f"slider_AGE_page_{scenario_key}"
    )

with col2:
    st.markdown("#### Características de Localização e Infraestrutura")
    features['DIS'] = st.slider(
        f"**DIS** - {feature_descriptions['DIS']}",
        min_value=float(ranges['DIS'][0]),
        max_value=float(ranges['DIS'][1]),
        value=float(current_values.get('DIS', defaults['DIS'])),
        step=0.1,
        key=f"slider_DIS_page_{scenario_key}"
    )
    
    features['RAD'] = st.slider(
        f"**RAD** - {feature_descriptions['RAD']}",
        min_value=float(ranges['RAD'][0]),
        max_value=float(ranges['RAD'][1]),
        value=float(current_values.get('RAD', defaults['RAD'])),
        step=1.0,
        key=f"slider_RAD_page_{scenario_key}"
    )
    
    features['TAX'] = st.slider(
        f"**TAX** - {feature_descriptions['TAX']}",
        min_value=float(ranges['TAX'][0]),
        max_value=float(ranges['TAX'][1]),
        value=float(current_values.get('TAX', defaults['TAX'])),
        step=1.0,
        key=f"slider_TAX_page_{scenario_key}"
    )
    
    features['PTRATIO'] = st.slider(
        f"**PTRATIO** - {feature_descriptions['PTRATIO']}",
        min_value=float(ranges['PTRATIO'][0]),
        max_value=float(ranges['PTRATIO'][1]),
        value=float(current_values.get('PTRATIO', defaults['PTRATIO'])),
        step=0.1,
        help="Razão aluno-professor (correlação negativa com preço)",
        key=f"slider_PTRATIO_page_{scenario_key}"
    )
    
    features['B'] = st.slider(
        f"**B** - {feature_descriptions['B']}",
        min_value=float(ranges['B'][0]),
        max_value=float(ranges['B'][1]),
        value=float(current_values.get('B', defaults['B'])),
        step=0.1,
        key=f"slider_B_page_{scenario_key}"
    )
    
    features['LSTAT'] = st.slider(
        f"**LSTAT** - {feature_descriptions['LSTAT']}",
        min_value=float(ranges['LSTAT'][0]),
        max_value=float(ranges['LSTAT'][1]),
        value=float(current_values.get('LSTAT', defaults['LSTAT'])),
        step=0.1,
        help="% de população de baixa renda (correlação negativa mais forte)",
        key=f"slider_LSTAT_page_{scenario_key}"
    )

# Botão de predição (fora do form)
st.markdown("---")
submitted = st.button("🔮 Prever Preço", use_container_width=True, type="primary")
    
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
                price = prediction.item()  # Já está em milhares de dólares (k$)
            
            elapsed_time = (time.time() - start_time) * 1000  # em ms
        
        # Exibir resultado
        st.markdown("---")
        st.markdown("### 💰 Resultado da Predição")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.metric(
                "Preço Predito",
                f"${price:.2f}k",
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
                f"{diff:+.2f}k",
                help="Diferença em relação ao preço médio do dataset"
            )
        
        # Comparação visual
        st.progress(min(max(price / 50.0, 0.0), 1.0))
        st.caption("Preço médio do dataset: ~$22.5k | Range típico: $5k - $50k")

# Atualizar session_state com valores dos sliders
for key, value in features.items():
    st.session_state.feature_values[key] = value

