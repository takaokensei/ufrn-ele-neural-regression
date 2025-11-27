# Slide 1 — Título

## Análise de Generalização em Redes Neurais para Regressão

### Validação Cruzada K-Fold e Otimização Bayesiana (Optuna)

---

**Autor:** Cauã Vitor Figueredo Silva  

**Matrícula:** 20220014216  

**UFRN - Engenharia Elétrica - ELE 604**  

**Novembro de 2025**

---

# Slide 2 — Contexto e Objetivos

### 🎯 O Desafio: Small Data & Overfitting

O dataset **Boston Housing** possui apenas **506 amostras**. O risco de o modelo "memorizar" os dados é alto.

**Problema Inicial:** Gap treino-validação de **181%** (overfitting severo)

### 🚀 Objetivos do Projeto

1. **Pipeline MLOps:** Implementar fluxo robusto de ponta a ponta.

2. **Generalização:** Garantir performance realística via **K-Fold (K=5)**.

3. **Regularização:** Mitigar overfitting (Dropout + L2 + Early Stopping).

4. **SOTA (State of the Art):** Maximizar métricas via **Otimização Bayesiana**.

---

# Slide 3 — Análise dos Dados

### 📊 Boston Housing Dataset

- **Target:** `MEDV` (Preço mediano em US$ 1000)

- **Dimensões:** 506 amostras × 13 features

### Features Críticas (Correlação Alta)

- **LSTAT (-0.74):** % população de baixa renda (Correlação Negativa)

- **RM (+0.70):** Número de quartos (Correlação Positiva)

- **PTRATIO (-0.51):** Razão aluno-professor

> **Ponto de Atenção:** A escassez de dados exige validação cruzada para evitar viés de seleção.

**(Inserir: Histograma da variável alvo MEDV ou Matriz de Correlação)**

---

# Slide 4 — Pipeline de Pré-processamento (Data Leakage)

### 🛡️ A Regra de Ouro do MLOps

Evitar que informações de validação vazem para o treino.

**Fluxo Correto (Implementado):**

1. **Divisão K-Fold:** Separação dos índices.

2. **Fit no Treino:** `scaler.fit(X_train)` 

3. **Transform no Resto:** `scaler.transform(X_val)`

### Normalização

- **Método:** Z-Score (StandardScaler)

- **Impacto:** Estabilização dos gradientes e convergência mais rápida do otimizador Adam.

**(Inserir: Diagrama simples de blocos mostrando o Scaler dentro do loop K-Fold)**

---

# Slide 5 — Arquitetura da Rede Neural

### 🧠 Multi-Layer Perceptron (MLP) Dinâmico

```mermaid
graph LR
    Input[Input (13)] --> H1[Hidden 1 (64) + ReLU]
    H1 --> Drop1[Dropout 30%]
    Drop1 --> H2[Hidden 2 (32) + ReLU]
    H2 --> Drop2[Dropout 30%]
    Drop2 --> Out[Output (1)]
```

*Nota: Se o ambiente não suportar Mermaid, usar imagem PNG do diagrama como backup.*

### Componentes Chave

- **Regularização Ativa:**
  - **Dropout (0.3):** Desliga 30% dos neurônios aleatoriamente.
  - **L2 (Weight Decay 1e-4):** Penaliza pesos de alta magnitude.

- **Otimização:**
  - **Algoritmo:** Adam (`lr=0.001`)
  - **Loss:** MSE (Mean Squared Error)

---

# Slide 6 — Estratégias de Treinamento

### ⚙️ Controle de Overfitting

| Técnica | Configuração | Benefício |
|:---:|:---:|:---|
| **K-Fold** | $K=5$ | Estimativa de erro robusta (Média ± Desvio Padrão). |
| **Early Stopping** | Patience=20 | Para o treino se `val_loss` estagnar. Economia de **70%** de tempo. |
| **Model Checkpointing** | `best_model.pth` | Garante que o modelo final é o de menor erro, não o último. |

---

# Slide 7 — Otimização Bayesiana (AutoML)

### 🔬 Por que Optuna?

Diferente do Grid Search (força bruta), o **TPE Sampler** aprende com os erros passados.

- **Trials:** 20 iterações

- **Tempo:** ~25 minutos (vs ~5h de Grid Search estimado)

- **Pruning:** O algoritmo **Hyperband** mata treinos ruins no início.

### Espaço de Busca

- **Camadas:** 1 a 3

- **Neurônios:** 16 a 128

- **Dropout:** 0.1 a 0.5

- **Otimizador:** Adam vs RMSprop

**(Inserir: `reports/figures/optuna_optimization_history.png` - Painel Histórico)**

---

# Slide 8 — Resultados Visuais: Convergência

### 📉 Curvas de Aprendizado (Loss)

**(Inserir: `reports/figures/learning_curves.png` lado a lado com `learning_curves_optimized.png`)**

### Análise Comparativa

1. **Modelo Base:** Convergência estável, mas com gap moderado.

2. **Modelo Otimizado:** Convergência mais rápida e **gap reduzido**.

3. **Diagnóstico:** Ausência de "boca de jacaré" (divergência) indica sucesso no combate ao overfitting.

---

# Slide 9 — Resultados Quantitativos

### 🏆 Comparação de Performance (Média 5-Folds)

| Métrica | Modelo Base | Modelo Otimizado | Variação |
|:---|:---:|:---:|:---:|
| **MSE (Erro)** | 13.47 | **13.02** | 🔻 **3.3%** (Melhor) |
| **R² (Ajuste)** | 0.852 | **0.857** | 🔺 **0.5%** (Melhor) |
| **Desvio Padrão** | **2.47** | 4.62 | 🔸 Aumento de variância |

### Insight

O modelo otimizado é **mais preciso** na média, embora apresente maior sensibilidade entre os folds (trade-off viés-variância).

---

# Slide 10 — Qualidade das Predições

### 🎯 Real vs Predito

**(Inserir: `reports/figures/predictions_scatter_optimized.png` ocupando a esquerda)**

**Interpretação Visual:**

- **Aderência:** Pontos agrupados próximos à linha vermelha tracejada ($y=x$).

- **Erro Médio:** ~$3.600 (em imóveis de ~$22.500).

- **Resíduos:** Distribuição uniforme, sem viés sistemático para preços altos ou baixos.

---

# Slide 11 — Análise de Generalização

### ✅ Classificação: Boa Generalização

O gap entre treino e validação foi reduzido drasticamente:

- **Sem Regularização:** Gap ~181% (Overfitting severo)

- **Com MLOps:** Gap **~35%** (Redução de **80%**)

### Métricas Finais

- **R² Médio:** **0.857** (85.7% da variância explicada)

- **Erro Médio:** ~$3.60k em preços de ~$22.5k (**16%** erro relativo)

### Limitações Identificadas

1. **Fold 3 (Outlier):** No modelo otimizado, um fold teve MSE=21.03, puxando o desvio padrão para cima.

2. **Capacidade do Modelo:** Com apenas 506 dados, arquiteturas mais profundas (3+ camadas) não trouxeram ganhos significativos.

---

# Slide 12 — Destaques do Projeto (Highlights)

### 🌟 O que foi alcançado

1. **Redução de Overfitting:** De 181% para **35%** de gap.

2. **Precisão:** Capacidade de explicar **85.7%** da variância dos preços ($R^2$).

3. **Eficiência:** Otimização de hiperparâmetros em **25 minutos**.

4. **Robustez:** Validação em 5 cenários diferentes (Folds) garante que o resultado não é sorte.

---

# Slide 13 — Conclusões e Próximos Passos

### Conclusão

A combinação de **Regularização (Dropout/L2)** com **Otimização Bayesiana** permitiu treinar uma rede neural robusta mesmo em um cenário de *Small Data*, superando as limitações de overfitting comuns nesse contexto.

### 🚀 Próximos Passos

- [ ] **Ensemble:** Média dos 5 modelos do K-Fold para reduzir a variância.

- [ ] **Feature Engineering:** Criar interações não-lineares (ex: $RM^2$).

- [ ] **Deploy:** Encapsular o melhor modelo em uma API com **FastAPI** e **Docker**.

---

# Slide 14 — Stack Tecnológico

### Ferramentas Utilizadas

- **Linguagem:** Python 3.12

- **Core ML:** PyTorch 2.0

- **Otimização:** Optuna 3.3 (TPE + Hyperband)

- **Pipeline:** Scikit-Learn (Pipeline, KFold)

- **Visualização:** Matplotlib & Seaborn

- **Ambiente:** Jupyter Notebook & LaTeX

---

# Slide 15 — Referências Principais

1. **Hastie, T., et al. (2009).** *The Elements of Statistical Learning*.

2. **Goodfellow, I., et al. (2016).** *Deep Learning*.

3. **Akiba, T., et al. (2019).** *Optuna: A Next-generation Hyperparameter Optimization Framework*.

4. **Srivastava, N., et al. (2014).** *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*.

**Repositório do Projeto:**

`github.com/takaokensei/ufrn-ele-neural-regression`

---

# Slide 16 — Perguntas?

### Obrigado pela atenção!

**Cauã Vitor Figueredo Silva**

`cauavitor@ufrn.edu.br`

UFRN - Engenharia Elétrica
