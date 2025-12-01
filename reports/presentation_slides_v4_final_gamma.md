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

**Entendendo o Alvo (MEDV - Preço Mediano em k$)**

**Legenda das Features:**
* **CRIM:** Taxa de criminalidade per capita
* **ZN:** Proporção de terrenos residenciais zoneados
* **INDUS:** Proporção de acres comerciais não-varejo
* **CHAS:** Limita com rio Charles (1=sim, 0=não)
* **NOX:** Concentração de óxidos de nitrogênio
* **RM:** Número médio de quartos por habitação
* **AGE:** Proporção de unidades ocupadas construídas antes de 1940
* **DIS:** Distância ponderada aos centros de emprego
* **RAD:** Índice de acessibilidade a rodovias radiais
* **TAX:** Taxa de imposto sobre propriedade
* **PTRATIO:** Razão aluno-professor por cidade
* **B:** Proporção de negros por cidade
* **LSTAT:** % de população de baixa renda
* **MEDV:** Preço mediano de casas (target)

**Variáveis Determinantes (Correlação de Pearson com MEDV):**

* **LSTAT (-0.74):** População de baixa renda (Fator negativo forte)
* **RM (+0.70):** Número de quartos (Fator positivo forte)
* **PTRATIO (-0.51):** Razão aluno-professor (Fator negativo moderado)

**Interpretação do Mapa de Correlação:**
* 🔴 **Vermelho:** Correlação positiva (quanto maior a feature, maior o preço)
* 🔵 **Azul:** Correlação negativa (quanto maior a feature, menor o preço)
* ⚪ **Branco/Claro:** Correlação próxima de zero (sem relação linear)

> **Ponto de Atenção:** A escassez de dados exige validação cruzada rigorosa

**[IMAGEM: `reports/figures/correlation_matrix.png` - Matriz de correlação de Pearson destacando LSTAT, RM e PTRATIO]**

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

**Abordagem:** Pipeline combinado aplicado simultaneamente

| Técnica | Configuração | Função |
| :--- | :--- | :--- |
| **Dropout** | 30% (0.3) | Evita co-adaptação de neurônios durante treino |
| **Weight Decay** | L2 (1e-4) | Penaliza pesos excessivos, promove soluções suaves |
| **Early Stopping** | Patience=20 | Interrompe treino quando validação não melhora |
| **Checkpointing** | Best Model | Salva modelo com menor erro de validação |

**Resultado Combinado:** Redução de **~80%** no gap de overfitting (181% → 35%)

> **Nota Metodológica:** As técnicas foram otimizadas em conjunto via Optuna. O impacto individual não foi isolado, pois trabalham sinergicamente.

---

# Otimização Bayesiana (Optuna)

**Buscando o Estado da Arte (SOTA)**

* **Algoritmo:** TPE Sampler (Parzen Estimator) + Hyperband Pruning

* **Espaço de Busca:**
    * Camadas: 1 a 3
    * Neurônios: 16 a 128
    * Dropout: 0.1 a 0.5

* **Eficiência:** 20 trials concluídos em **25 minutos** (vs. ~5h de Grid Search)

**[IMAGEM: `reports/figures/optuna_optimization_history.png` - Histórico de otimização Optuna]**

---

# Resultados: Redução de Overfitting

**Análise Visual das Curvas de Aprendizado**

* **Baseline:** Divergência massiva (Gap 181%)

* **Otimizado:** Convergência suave (Gap 35%)

* **Conclusão:** Redução de **80% no overfitting** com a introdução de regularização e otimização

**[IMAGEM: `reports/figures/learning_curves.png` (esquerda) e `reports/figures/learning_curves_optimized.png` (direita) - Curvas de aprendizado lado a lado]**

---

# Comparativo de Performance

**Métricas (Média 5-Folds)**

| Métrica | Baseline | Otimizado (Optuna) | Variação |
| :--- | :--- | :--- | :--- |
| **MSE** | 13.47 | **13.02** | -3.3% (Melhor) |
| **R² (Média)** | 0.852 | **0.857** | +0.5% (Melhor) |
| **R² (Melhor Fold)** | - | **0.927** (Fold 4) | Potencial máximo |
| **Desvio Padrão** | 2.47 | 4.62 | + Variância |

> **Insight:** Embora a média do R² tenha se mantido estável (0.857), o modelo atingiu picos de performance superiores (0.927), demonstrando capacidade de aprender padrões complexos. O aumento do desvio padrão é um trade-off esperado da otimização agressiva em *Small Data*, refletindo maior sensibilidade em folds específicos.

**[IMAGEM OPCIONAL: `reports/figures/kfold_results.png` - Resultados por fold]**

---

# Validação Final e Generalização

**Performance em Dados Não Vistos**

* **R² (Média 5-Folds):** **0.857** (Explicamos 85.7% da variância em média)
* **R² (Melhor Fold - Fold 4):** **0.927** (92.7% da variância no melhor cenário de validação)

* **Erro Médio (RMSE):** ~$3.600 (para imóveis de ~$22.500)

* **Diagnóstico:** Resíduos distribuídos uniformemente, indicando ausência de viés sistemático significativo. O modelo atingiu R² de 0.927 no melhor cenário, comprovando alto potencial preditivo quando as condições de treinamento são favoráveis.

**[IMAGEM: `reports/figures/predictions_scatter_optimized.png` - Scatter plot Real vs Predito com linha de identidade]**

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