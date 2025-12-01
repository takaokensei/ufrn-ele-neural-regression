# Plano de Desenvolvimento: Aplicação Streamlit Interativa

## 🎯 Objetivo

Criar uma aplicação web leve e intuitiva em Streamlit para demonstrar o modelo de regressão neural treinado no Boston Housing Dataset durante a apresentação acadêmica. A aplicação permitirá interação em tempo real com o público/professor, mostrando predições, métricas e visualizações.

---

## 📋 Visão Geral

### Funcionalidades Principais

1. **Predição Interativa:** Input manual de features para obter predição de preço
2. **Comparação de Cenários:** Testar diferentes configurações de imóveis
3. **Visualização de Métricas:** Exibir R², MSE e outras métricas do modelo
4. **Análise de Features:** Mostrar importância e correlação das features
5. **Dashboard de Performance:** Gráficos de learning curves e resultados K-Fold

---

## 🏗️ Arquitetura da Aplicação

### Estrutura de Arquivos

```
ufrn-ele-neural-regression/
├── streamlit_app/
│   ├── __init__.py
│   ├── app.py                    # Arquivo principal Streamlit
│   ├── pages/
│   │   ├── 1_🏠_Predição.py      # Página de predição interativa
│   │   ├── 2_📊_Métricas.py      # Página de métricas e performance
│   │   ├── 3_🔍_Análise.py       # Página de análise de features
│   │   └── 4_📈_Dashboard.py     # Página de visualizações
│   ├── utils/
│   │   ├── model_loader.py       # Carregamento do modelo treinado
│   │   ├── preprocessor.py       # Pré-processamento (StandardScaler)
│   │   └── visualizations.py     # Funções de visualização
│   └── assets/
│       ├── model/
│       │   └── best_model_fold.pth  # Modelo treinado (checkpoint)
│       └── scaler.pkl            # StandardScaler salvo (opcional)
├── requirements_streamlit.txt    # Dependências adicionais
└── .streamlit/
    └── config.toml               # Configurações do Streamlit
```

---

## 🎨 Design e UX

### Tema e Estilo

- **Tema:** Dark mode (profissional, moderno)
- **Cores:** Paleta azul/verde (alinhada com o projeto)
- **Layout:** Sidebar para navegação, conteúdo principal centralizado
- **Responsividade:** Adaptável para diferentes tamanhos de tela

### Navegação

```
Sidebar:
├── 🏠 Predição Interativa
├── 📊 Métricas e Performance
├── 🔍 Análise de Features
└── 📈 Dashboard Visual
```

---

## 📄 Páginas Detalhadas

### Página 1: 🏠 Predição Interativa

**Objetivo:** Permitir que o usuário insira valores de features e obtenha predição de preço em tempo real.

**Componentes:**

1. **Formulário de Input (13 features):**
   - Sliders ou inputs numéricos para cada feature
   - Valores padrão baseados na média do dataset
   - Validação de ranges (min/max do dataset)
   - Botão "Prever Preço"

2. **Resultado da Predição:**
   - Preço predito em destaque (grande, colorido)
   - Intervalo de confiança (opcional, baseado em desvio padrão)
   - Comparação com preço médio do dataset (~$22.500)

3. **Seção de Testes Rápidos:**
   - Botões pré-configurados para cenários:
     - "Imóvel Premium" (RM alto, LSTAT baixo)
     - "Imóvel Econômico" (RM baixo, LSTAT alto)
     - "Imóvel Médio" (valores médios)
   - Mostrar diferença entre predições

4. **Explicação do Modelo:**
   - Breve descrição: "Modelo MLP otimizado com Optuna"
   - R² do modelo: 0.857 (média) / 0.927 (melhor fold)
   - Tempo de predição: < 1ms

**Código Estrutural:**
```python
import streamlit as st
import torch
from utils.model_loader import load_model
from utils.preprocessor import preprocess_input

st.title("🏠 Predição de Preço de Imóveis")
st.markdown("Insira as características do imóvel para obter uma predição de preço")

# Carregar modelo (cache)
@st.cache_resource
def load_trained_model():
    return load_model('assets/model/best_model_fold.pth')

model = load_trained_model()

# Formulário
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        crim = st.slider("CRIM - Taxa de criminalidade", 0.0, 100.0, 3.6)
        zn = st.slider("ZN - Terrenos residenciais", 0.0, 100.0, 11.4)
        # ... outras features
    
    with col2:
        # ... mais features
    
    submitted = st.form_submit_button("🔮 Prever Preço")
    
    if submitted:
        # Pré-processar input
        features = preprocess_input([crim, zn, ...])
        
        # Predição
        with torch.no_grad():
            prediction = model(features)
            price = prediction.item() * 1000  # Converter para dólares
        
        # Exibir resultado
        st.success(f"💰 Preço Predito: ${price:,.2f}")
```

---

### Página 2: 📊 Métricas e Performance

**Objetivo:** Exibir métricas de performance do modelo de forma clara e visual.

**Componentes:**

1. **Cards de Métricas Principais:**
   - R² (Média): 0.857
   - R² (Melhor Fold): 0.927
   - MSE: 13.02
   - MAE: ~$3.600

2. **Tabela Comparativa:**
   - Baseline vs Otimizado
   - Melhoria percentual destacada

3. **Gráfico de Barras:**
   - Resultados por Fold (K-Fold)
   - Destacar Fold 3 como outlier
   - Mostrar média e desvio padrão

4. **Seção de Tempo de Execução:**
   - Tempo de otimização Optuna: ~2 minutos
   - Tempo de predição: < 1ms
   - Comparação com Grid Search (~5h)

**Código Estrutural:**
```python
st.title("📊 Métricas e Performance")

# Cards de métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("R² (Média)", "0.857", "+0.5%")
with col2:
    st.metric("R² (Melhor Fold)", "0.927", "Fold 4")
with col3:
    st.metric("MSE", "13.02", "-3.3%")
with col4:
    st.metric("MAE", "$3.600", "Erro médio")

# Gráfico K-Fold
import plotly.express as px
fig = px.bar(x=folds, y=mses, title="MSE por Fold")
st.plotly_chart(fig)
```

---

### Página 3: 🔍 Análise de Features

**Objetivo:** Mostrar importância e correlação das features com o target.

**Componentes:**

1. **Top 5 Correlações Positivas:**
   - RM (+0.70)
   - ZN (+0.36)
   - B (+0.33)
   - DIS (+0.25)
   - CHAS (+0.18)

2. **Top 5 Correlações Negativas:**
   - LSTAT (-0.74)
   - PTRATIO (-0.51)
   - INDUS (-0.48)
   - TAX (-0.47)
   - NOX (-0.43)

3. **Matriz de Correlação Interativa:**
   - Heatmap clicável
   - Tooltips com valores exatos

4. **Explicação de Features:**
   - Legenda completa com descrições
   - Exemplos de valores típicos

**Código Estrutural:**
```python
st.title("🔍 Análise de Features")

# Carregar matriz de correlação
correlation_matrix = load_correlation_matrix()

# Heatmap interativo
import plotly.graph_objects as go
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='RdBu',
    zmid=0
))
st.plotly_chart(fig)

# Top correlações
st.subheader("Top 5 Correlações com MEDV")
col1, col2 = st.columns(2)

with col1:
    st.write("**Positivas:**")
    for feature, corr in top_positive:
        st.write(f"- {feature}: {corr:+.2f}")

with col2:
    st.write("**Negativas:**")
    for feature, corr in top_negative:
        st.write(f"- {feature}: {corr:+.2f}")
```

---

### Página 4: 📈 Dashboard Visual

**Objetivo:** Visualizações avançadas de learning curves e resultados.

**Componentes:**

1. **Learning Curves:**
   - Baseline vs Otimizado (lado a lado)
   - Interatividade (zoom, hover)
   - Destacar gap de overfitting

2. **Scatter Plot Predições vs Reais:**
   - Dados do melhor fold
   - Linha de identidade (y=x)
   - R² destacado

3. **Histórico de Otimização Optuna:**
   - Gráfico de trials
   - Melhor trial destacado
   - Importância de hiperparâmetros

4. **Seleção de Fold:**
   - Dropdown para escolher fold
   - Atualizar visualizações dinamicamente

**Código Estrutural:**
```python
st.title("📈 Dashboard Visual")

# Seleção de fold
fold_selected = st.selectbox("Selecione o Fold", [1, 2, 3, 4, 5])

# Learning curves
fig_curves = plot_learning_curves(fold_selected)
st.plotly_chart(fig_curves)

# Scatter plot
fig_scatter = plot_predictions_scatter(fold_selected)
st.plotly_chart(fig_scatter)
```

---

## 🔧 Implementação Técnica

### 1. Carregamento do Modelo

**Arquivo:** `streamlit_app/utils/model_loader.py`

```python
import torch
from src.model import MLP

def load_model(checkpoint_path: str) -> MLP:
    """
    Carrega o modelo treinado do checkpoint.
    
    Args:
        checkpoint_path: Caminho para o arquivo .pth
        
    Returns:
        Modelo MLP carregado e em modo eval
    """
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    # Extrair configuração do modelo do checkpoint
    model_config = checkpoint.get('model_config', {
        'input_dim': 13,
        'hidden_dims': [64, 32],
        'output_dim': 1,
        'dropout_rate': 0.3,
        'use_batch_norm': False
    })
    
    # Instanciar modelo
    model = MLP(**model_config)
    
    # Carregar pesos
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    return model
```

### 2. Pré-processamento

**Arquivo:** `streamlit_app/utils/preprocessor.py`

```python
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
import pickle

def load_scaler() -> StandardScaler:
    """Carrega o StandardScaler salvo (se disponível)"""
    try:
        with open('streamlit_app/assets/scaler.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Usar valores padrão do dataset se scaler não estiver disponível
        return None

def preprocess_input(features: list) -> torch.Tensor:
    """
    Pré-processa input do usuário para formato do modelo.
    
    Args:
        features: Lista com 13 valores de features
        
    Returns:
        Tensor PyTorch normalizado
    """
    # Converter para numpy array
    features_array = np.array(features).reshape(1, -1)
    
    # Normalizar (usar scaler ou valores padrão)
    scaler = load_scaler()
    if scaler:
        features_scaled = scaler.transform(features_array)
    else:
        # Normalização manual (valores médios e std do dataset)
        mean = np.array([3.6, 11.4, 11.1, 0.07, 0.55, 6.3, 68.6, 3.8, 9.5, 408.2, 18.5, 356.7, 12.7])
        std = np.array([8.6, 23.3, 6.9, 0.25, 0.12, 0.7, 28.1, 2.1, 8.7, 168.5, 2.2, 91.3, 7.1])
        features_scaled = (features_array - mean) / std
    
    # Converter para tensor
    return torch.FloatTensor(features_scaled)
```

### 3. Configuração do Streamlit

**Arquivo:** `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#4A90E2"
backgroundColor = "#1a1a2e"
secondaryBackgroundColor = "#16213e"
textColor = "#ffffff"
font = "sans serif"

[server]
headless = true
port = 8501
```

---

## 📦 Dependências

**Arquivo:** `requirements_streamlit.txt`

```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
torch>=2.0.0
scikit-learn>=1.3.0
```

---

## 🚀 Deploy no Streamlit Cloud

### Passos para Deploy

1. **Preparar Repositório:**
   - Garantir que `streamlit_app/app.py` existe
   - Adicionar `requirements_streamlit.txt` na raiz
   - Commit e push para GitHub

2. **Configurar Streamlit Cloud:**
   - Acessar https://streamlit.io/cloud
   - Conectar repositório GitHub
   - Configurar:
     - **Main file path:** `streamlit_app/app.py`
     - **Python version:** 3.12
     - **Dependencies file:** `requirements_streamlit.txt`

3. **Assets Necessários:**
   - Modelo treinado (`best_model_fold.pth`) deve estar em `streamlit_app/assets/model/`
   - Opcional: Scaler salvo (`scaler.pkl`)
   - Imagens/gráficos em `streamlit_app/assets/`

4. **Variáveis de Ambiente (se necessário):**
   - Nenhuma necessária para este projeto

---

## 🎯 Funcionalidades de Demonstração

### Durante a Apresentação

1. **Teste ao Vivo (Slide de Demonstração):**
   - QR Code para acessar a aplicação
   - Teste rápido com valores pré-configurados
   - Mostrar predição em tempo real

2. **Cenários de Teste:**
   - **Teste 1 - Velocidade:** Mostrar predição instantânea (< 1ms)
   - **Teste 2 - Precisão:** Comparar predição com valor real conhecido
   - **Teste 3 - Interatividade:** Permitir que público teste diferentes valores

3. **Visualizações Interativas:**
   - Navegar entre páginas durante apresentação
   - Mostrar gráficos interativos (zoom, hover)
   - Destacar métricas principais

---

## 📝 Checklist de Implementação

### Fase 1: Setup Básico
- [ ] Criar estrutura de diretórios
- [ ] Configurar `requirements_streamlit.txt`
- [ ] Criar `.streamlit/config.toml`
- [ ] Criar `streamlit_app/app.py` básico

### Fase 2: Carregamento do Modelo
- [ ] Implementar `model_loader.py`
- [ ] Testar carregamento do checkpoint
- [ ] Validar predições com dados conhecidos

### Fase 3: Página de Predição
- [ ] Criar formulário com 13 features
- [ ] Implementar pré-processamento
- [ ] Exibir resultado da predição
- [ ] Adicionar cenários pré-configurados

### Fase 4: Páginas de Análise
- [ ] Implementar página de métricas
- [ ] Implementar página de análise de features
- [ ] Implementar dashboard visual
- [ ] Adicionar gráficos interativos (Plotly)

### Fase 5: Polimento
- [ ] Adicionar tooltips e explicações
- [ ] Melhorar UX/UI
- [ ] Testar responsividade
- [ ] Adicionar loading states

### Fase 6: Deploy
- [ ] Preparar assets (modelo, scaler)
- [ ] Testar localmente
- [ ] Fazer deploy no Streamlit Cloud
- [ ] Testar aplicação deployada
- [ ] Gerar QR Code para apresentação

---

## 🎨 Exemplo de Slide para Apresentação

**Slide: "Demonstração Interativa"**

```
# Demonstração ao Vivo: Aplicação Streamlit

**Acesse a Plataforma:**
[QR Code]

**Testes Disponíveis:**
1. 🚀 Velocidade: Predição instantânea (< 1ms)
2. 🎯 Precisão: Comparação com valores reais
3. 🔍 Interatividade: Teste seus próprios valores

**Recursos:**
- Predição em tempo real
- Visualizações interativas
- Análise de features
- Dashboard de performance
```

---

## 📊 Métricas de Sucesso

- ✅ Aplicação carrega em < 3 segundos
- ✅ Predição executada em < 1ms
- ✅ Interface responsiva e intuitiva
- ✅ Visualizações interativas funcionando
- ✅ Deploy bem-sucedido no Streamlit Cloud
- ✅ Acessível via QR Code durante apresentação

---

## 🔄 Próximos Passos

1. **Implementar Fase 1-2** (Setup e carregamento do modelo)
2. **Testar localmente** com modelo treinado
3. **Implementar Fase 3** (Página de predição)
4. **Adicionar visualizações** (Fase 4)
5. **Polir e testar** (Fase 5)
6. **Fazer deploy** (Fase 6)

---

**Data de Criação:** Novembro 2025
**Autor:** Cauã Vitor Figueredo Silva
**Status:** 📋 Plano de Desenvolvimento

