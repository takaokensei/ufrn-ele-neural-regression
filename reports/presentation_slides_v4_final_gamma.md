# Análise de Generalização em Redes Neurais para Regressão

## Validação Cruzada K-Fold e Otimização Bayesiana

---

**Autor:** Cauã Vitor Figueredo Silva | **Orientador:** Prof. Dr. Allan de Medeiros Martins

**UFRN - Engenharia Elétrica - ELE 604 | Novembro 2025**

---

# O Desafio do Small Data

**Contexto: Boston Housing Dataset**

* **Volume:** Apenas 506 amostras (Risco crítico de viés)

* **Dimensionalidade:** 13 features para prever preço (MEDV)

* **O Problema:** O modelo baseline apresentava **Overfitting severo**, com um gap de **181%** entre treino e validação

---

# Análise de Features e Correlação

**Entendendo o Alvo (MEDV - Preço em k$)**

Variáveis determinantes (Correlação de Pearson):

* **LSTAT (-0.74):** População de baixa renda (Fator negativo forte)

* **RM (+0.70):** Número de quartos (Fator positivo forte)

* **PTRATIO (-0.51):** Razão aluno-professor

> **Ponto de Atenção:** A escassez de dados exige validação cruzada rigorosa

---

# Arquitetura da Rede Neural (MLP)

**Topologia e Hiperparâmetros Base**

* **Input Layer:** 13 Neurônios

* **Hidden Layers:**
    * Camada 1: 64 Neurônios (ReLU)
    * Camada 2: 32 Neurônios (ReLU)

* **Output Layer:** 1 Neurônio (Linear)

* **Otimizador:** Adam (`lr=0.001`)

* **Loss Function:** Mean Squared Error (MSE)

---

# Metodologia: Pipeline Anti-Leakage

**Garantindo Robustez no Treinamento**

1. **Validação Cruzada:** K-Fold com **K=5** para estimativa realística de erro

2. **Prevenção de Vazamento:**
    * `scaler.fit` aplicado **apenas** no conjunto de treino
    * `scaler.transform` aplicado na validação

3. **Objetivo:** Evitar que o modelo "veja" dados de teste através da normalização global

---

# Estratégias de Regularização

**Combatendo o Gap de 181%**

| Técnica | Configuração | Impacto |
| :--- | :--- | :--- |
| **Dropout** | 30% (0.3) | Evita co-adaptação de neurônios |
| **Weight Decay** | L2 (1e-4) | Penaliza pesos excessivos |
| **Early Stopping** | Patience=20 | Economiza 70% de tempo de treino |
| **Checkpointing** | Best Model | Garante o modelo de menor erro, não o último |

---

# Otimização Bayesiana (Optuna)

**Buscando o Estado da Arte (SOTA)**

* **Algoritmo:** TPE Sampler (Parzen Estimator) + Hyperband Pruning

* **Espaço de Busca:**
    * Camadas: 1 a 3
    * Neurônios: 16 a 128
    * Dropout: 0.1 a 0.5

* **Eficiência:** 20 trials concluídos em **25 minutos** (vs. ~5h de Grid Search)

---

# Resultados: Redução de Overfitting

**Análise Visual das Curvas de Aprendizado**

* **Baseline:** Divergência massiva (Gap 181%)

* **Otimizado:** Convergência suave (Gap 35%)

* **Conclusão:** Redução de **80% no overfitting** com a introdução de regularização e otimização

---

# Comparativo de Performance

**Métricas (Média 5-Folds)**

| Métrica | Baseline | Otimizado (Optuna) | Variação |
| :--- | :--- | :--- | :--- |
| **MSE** | 13.47 | **13.02** | -3.3% (Melhor) |
| **R²** | 0.852 | **0.857** | +0.5% (Melhor) |
| **Desvio Padrão** | 2.47 | 4.62 | + Variância |

> **Insight:** O modelo otimizado é mais preciso na média, mas o aumento no desvio padrão reflete a sensibilidade do *Small Data* em folds específicos

---

# Validação Final e Generalização

**Performance em Dados Não Vistos**

* **R² Final:** **0.857** (Explicamos 85.7% da variância)

* **Erro Médio:** ~$3.600 (para imóveis de ~$22.500)

* **Diagnóstico:** Resíduos distribuídos uniformemente, indicando ausência de viés sistemático significativo

---

# Conclusões e Próximos Passos

**Principais Conquistas:**

1. Pipeline MLOps robusto e reprodutível

2. Redução drástica de overfitting (181% → 35%)

3. Otimização eficiente de hiperparâmetros

**Limitações & Futuro:**

* O **Fold 3** apresentou comportamento outlier (MSE=21.03)

* **Próximos passos:** Ensemble de modelos e Feature Engineering (ex: interações não-lineares)

**Repositório:** `github.com/takaokensei/ufrn-ele-neural-regression`

---

# Obrigado!

**Perguntas?**

**Cauã Vitor Figueredo Silva**

`cauavitorfigueredo@gmail.com`

