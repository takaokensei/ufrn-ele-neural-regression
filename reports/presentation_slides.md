# Slide 1 — Título

**Análise de Generalização em Redes Neurais para Regressão de Preços Imobiliários**

**Validação Cruzada K-Fold e Otimização Bayesiana com Optuna**

**Autor:** Cauã Vitor Figueredo Silva  
**Matrícula:** 20220014216  
**Instituição:** UFRN - Centro de Tecnologia - Departamento de Engenharia Elétrica  
**Data:** Novembro de 2025

---

# Slide 2 — Objetivos

### Objetivo Geral
- Implementar um pipeline completo de MLOps para regressão neural com foco rigoroso em generalização, aplicando técnicas de regularização e otimização Bayesiana para alcançar o estado da arte.

### Objetivos Específicos
1. **Implementar** um pipeline MLOps completo desde o carregamento de dados até a avaliação final.
2. **Prevenir** Data Leakage através de normalização correta (StandardScaler ajustado apenas no treino).
3. **Aplicar** técnicas de regularização: Dropout (30%) e L2 Regularization (weight_decay=1e-4).
4. **Implementar** Early Stopping e Model Checkpointing para otimizar o treinamento.
5. **Utilizar** Otimização Bayesiana (Optuna) para encontrar hiperparâmetros ótimos.
6. **Avaliar** a generalização do modelo com K-Fold Cross-Validation (K=5).
7. **Analisar** quantitativamente e qualitativamente os resultados através de métricas e visualizações.

---

# Slide 3 — Base de Dados

### Dataset: Boston Housing

- **Fonte:** http://lib.stat.cmu.edu/datasets/boston
- **Compilado por:** Harrison e Rubinfeld (1978)
- **Características:**
  - **506 amostras** de imóveis residenciais
  - **13 features** independentes (taxa de criminalidade, número de cômodos, concentração de óxido nítrico, etc.)
  - **1 target:** MEDV (Preço mediano das casas em $1000)
- **Desafio:** Dataset pequeno (Small Data) requer técnicas robustas de validação

### Features Principais
- **CRIM:** Taxa de criminalidade per capita
- **RM:** Número médio de cômodos por residência
- **LSTAT:** Porcentagem de população de baixa renda
- **NOX:** Concentração de óxido nítrico (ppm)
- **PTRATIO:** Razão aluno-professor por cidade

**(Inserir print do gráfico de distribuição de classes gerado em `reports/figures/kfold_results.png` aqui)**

---

# Slide 4 — Métodos e Abordagem: Pipeline de Pré-processamento

### Etapas de Preparação dos Dados

O pré-processamento é executado dentro do loop K-Fold para prevenir Data Leakage:

1. **Carregamento Robusto:**
   - Download direto da URL original do dataset
   - Tratamento de cabeçalho complexo
   - Fallback para dados simulados em caso de falha de conexão

2. **Normalização (StandardScaler):**
   - **CRÍTICO:** O scaler é ajustado (`fit`) **apenas no conjunto de treino** de cada fold
   - Os dados de validação são apenas transformados (`transform`) usando estatísticas do treino
   - **Fórmula:** $x_{\text{scaled}} = \frac{x - \mu}{\sigma}$
   - **Justificativa:** Acelera convergência do Gradiente Descendente e evita dominância de features

3. **Divisão dos Dados (K-Fold Cross-Validation):**
   - **K=5 folds** estratificados
   - Para cada fold: 80% treino, 20% validação
   - **Seed fixada (42)** para reprodutibilidade

---

# Slide 5 — Métodos e Abordagem: Arquitetura do Modelo

### Modelo: Multi-Layer Perceptron (MLP)

- **Tipo:** Rede Neural Feedforward totalmente conectada
- **Implementação:** Classe `MLP` em `src/model.py` e `notebooks/project_main.ipynb`
- **Racional:** Arquitetura simples e eficaz para regressão, com capacidade de aprender padrões não-lineares

### Esquema Passo a Passo:

1. **Camada de Entrada (Input Layer):**
   - `nn.Linear(13, 64)` ou `nn.Linear(13, 32)` (dinâmico via Optuna)
   - Recebe 13 features normalizadas

2. **Camada Oculta 1:**
   - `nn.Linear(13, 64)` → `nn.BatchNorm1d(64)` (opcional) → `nn.ReLU()` → `nn.Dropout(0.3)`
   - 64 neurônios com ativação ReLU e Dropout de 30%

3. **Camada Oculta 2:**
   - `nn.Linear(64, 32)` → `nn.BatchNorm1d(32)` (opcional) → `nn.ReLU()` → `nn.Dropout(0.3)`
   - 32 neurônios (arquitetura decrescente)

4. **Camada de Saída (Output Layer):**
   - `nn.Linear(32, 1)`
   - 1 neurônio para predição contínua (sem ativação)

### Regularização Aplicada:
- **Dropout (30%):** Previne overfitting desligando neurônios aleatoriamente
- **L2 Regularization (λ=10⁻⁴):** Penaliza pesos grandes via weight_decay no otimizador
- **Batch Normalization (Opcional):** Normaliza ativações entre camadas

**(Inserir print do `print(model)` que mostra a arquitetura aqui)**

---

# Slide 6 — Pipeline de Treinamento

### Configuração do Treinamento (`src/train.py` e notebook)

- **Divisão de Dados:**
  - Dados encapsulados em `DataLoaders` do PyTorch
  - `batch_size`: 16 (modelo base) ou 8-32 (otimizado via Optuna)
  - `drop_last=True` quando BatchNorm está ativo (evita erro com batch size=1)

- **Hiperparâmetros (Modelo Base):**
  - `epochs`: 500 (máximo, com Early Stopping)
  - `learning_rate`: 0.001
  - `weight_decay`: 0.0001 (L2 Regularization)
  - `dropout_rate`: 0.3 (30%)
  - `patience`: 20 épocas (Early Stopping)

- **Loop de Treino:**
  1. Modelo em modo treino (`model.train()`)
  2. Para cada batch:
     - Forward pass → Calcula loss (MSE)
     - Backward pass (`loss.backward()`)
     - Atualiza pesos (`optimizer.step()`)
  3. Após cada época: avaliação no conjunto de validação
  4. Early Stopping: para se val_loss não melhorar por 20 épocas
  5. Model Checkpointing: salva melhor modelo (menor val_loss)

- **Função de Perda e Otimizador:**
  - **Loss:** `nn.MSELoss` (Mean Squared Error para regressão)
  - **Otimizador:** `torch.optim.Adam` com weight_decay (combina momentum e adaptatividade)

---

# Slide 7 — Otimização Bayesiana com Optuna

### Metodologia de AutoML

- **Framework:** Optuna com TPE Sampler (Tree-structured Parzen Estimator)
- **Pruner:** HyperbandPruner (interrompe trials não-promissores)
- **Trials:** 20 configurações testadas (~25 minutos vs ~5h de Grid Search)

### Espaço de Busca (8 Hiperparâmetros):

1. **n_layers:** 1-3 camadas ocultas
2. **hidden_units:** [16, 32, 64, 128] neurônios por camada
3. **dropout_rate:** 0.1-0.5 (contínuo)
4. **learning_rate:** 1e-4 a 1e-2 (log-uniforme)
5. **weight_decay:** 1e-6 a 1e-3 (log-uniforme)
6. **batch_size:** [8, 16, 32]
7. **optimizer:** Adam ou RMSprop
8. **use_batch_norm:** True/False

### Vantagens da Otimização Bayesiana:
- **Memória:** Aprende com trials anteriores (vs Grid Search cego)
- **Eficiência:** Pruning interrompe trials ruins early (economiza 70% do tempo)
- **Automação:** Elimina tuning manual de hiperparâmetros

**(Inserir imagem `reports/figures/optuna_optimization_history.png` aqui)**

---

# Slide 8 — Análise do Treinamento

### Curvas de Aprendizado

- As curvas de loss de treino e validação indicam o comportamento do modelo ao longo das épocas.

- **Observações (baseado nos resultados):**
  - **Modelo Base:** Loss de treino e validação convergem suavemente
  - **Early Stopping:** Ativado em média após 150-200 épocas (vs máximo de 500)
  - **Gap Reduzido:** Overfitting inicial (gap de 181%) foi reduzido para ~35% com regularização
  - **Modelo Otimizado:** Apresenta convergência similar, mas com arquitetura otimizada

**(Inserir imagem `reports/figures/learning_curves.png` e `reports/figures/learning_curves_optimized.png` aqui)**

---

# Slide 9 — Métricas e Resultados

### Avaliação no Conjunto de Validação (K-Fold)

O modelo final é avaliado através de K-Fold Cross-Validation (K=5) para estimativa robusta de generalização.

### Resultados do Modelo Base (com Dropout + L2):

| Fold | MSE | R² |
|------|-----|-----|
| Fold 1 | 12.5203 | 0.8609 |
| Fold 2 | 10.8016 ⭐ | 0.8899 |
| Fold 3 | 18.1186 | 0.7996 |
| Fold 4 | 12.5295 | 0.8608 |
| Fold 5 | 13.3764 | 0.8514 |
| **Média** | **13.4693** | **0.8525** |
| **Desvio Padrão** | **2.4708** | **0.0314** |

### Resultados do Modelo Otimizado (Optuna):

| Fold | MSE | R² |
|------|-----|-----|
| Fold 1 | 11.9913 | 0.8668 |
| Fold 2 | 9.9177 | 0.8989 |
| Fold 3 | 21.0343 | 0.7674 |
| Fold 4 | 7.6037 ⭐ | 0.9157 |
| Fold 5 | 14.5738 | 0.8383 |
| **Média** | **13.0242** | **0.8574** |
| **Desvio Padrão** | **4.6187** | **0.0519** |

**Melhoria:** 3.3% de redução no MSE médio (13.47 → 13.02)

**(Inserir print do Relatório de Resultados gerado no notebook aqui)**

---

# Slide 10 — Análise dos Resultados

### Scatter Plot: Predições vs Valores Reais

- Os gráficos de dispersão mostram a qualidade das predições em relação aos valores reais.
- **Linha Identidade (y=x):** Representa a predição perfeita.

**Observações:**
- **Modelo Base:** R² = 0.925 (92.5% da variância explicada)
- **Modelo Otimizado:** R² = 0.916 (91.6% da variância explicada)
- **Dispersão Uniforme:** Pontos bem distribuídos em torno da diagonal, sem viés sistemático
- **Erro Médio:** ~$3.60k em preços medianos de ~$22.5k (erro relativo de ~16%)

**(Inserir print dos Scatter Plots de `reports/figures/predictions_scatter.png` e `reports/figures/predictions_scatter_optimized.png` aqui)**

### Análise de Generalização

- **Classificação:** ✅ **Boa Generalização**
  - Gap treino-validação: ~35% (aceitável)
  - R² médio: 0.857 (85.7% da variância explicada)
  - Curvas convergentes sem divergência

### Limitações Identificadas

- **Dataset Pequeno:** 506 amostras limitam capacidade de aprender padrões muito complexos
- **Variabilidade entre Folds:** Fold 3 no modelo otimizado apresentou MSE=21.03 (outlier)
- **Trade-off Bias-Variance:** Modelo otimizado tem MSE menor, mas desvio padrão maior (4.62 vs 2.47)

---

# Slide 11 — Impacto das Técnicas MLOps

### Técnicas Aplicadas e Seus Efeitos

1. **Dropout (30%):**
   - **Efeito:** Reduziu gap treino-validação de 181% para ~35%
   - **Mecanismo:** Desliga neurônios aleatoriamente, forçando representações redundantes

2. **L2 Regularization (λ=10⁻⁴):**
   - **Efeito:** Complementa Dropout ao penalizar pesos grandes
   - **Mecanismo:** Adiciona termo $\lambda \sum w_i^2$ à função de perda

3. **K-Fold Cross-Validation (K=5):**
   - **Efeito:** Forneceu estimativa robusta mesmo com dataset pequeno
   - **Mecanismo:** Reduz variância da métrica através de múltiplas avaliações

4. **StandardScaler Correto:**
   - **Efeito:** Preveniu data leakage (R² realista ~0.85 vs artificial >0.95)
   - **Mecanismo:** Normalização dentro do loop K-Fold, apenas no treino

5. **Early Stopping (patience=20):**
   - **Efeito:** Economizou 60-70% do tempo computacional
   - **Mecanismo:** Interrompe quando val_loss estagna

6. **Otimização Bayesiana (Optuna):**
   - **Efeito:** Encontrou configuração ótima em 20 trials (~25 min vs ~5h Grid Search)
   - **Mecanismo:** TPE aprende com trials anteriores, HyperbandPruner elimina trials ruins

---

# Slide 12 — Próximos Passos e Melhorias Técnicas

1. **Ensemble Learning:**
   - Combinar os 5 modelos K-Fold através de média ponderada
   - **Benefício:** Reduzir variância e melhorar estabilidade

2. **Feature Engineering:**
   - Criar interações entre features (ex: $RM \times LSTAT$)
   - Transformações não-lineares (log, polinomiais)
   - **Benefício:** Capturar relações não-lineares explícitas

3. **Comparação com Baselines:**
   - Avaliar modelos mais simples (Ridge Regression, Lasso)
   - Ensemble clássicos (XGBoost, Random Forest)
   - **Benefício:** Quantificar ganho real da rede neural

4. **Interpretabilidade (SHAP Values):**
   - Analisar contribuição de cada feature para as predições
   - **Benefício:** Validação com especialistas do domínio e transparência

5. **Transfer Learning:**
   - Pré-treinar em datasets similares (preços imobiliários de outras cidades)
   - Fine-tuning em Boston Housing
   - **Benefício:** Aproveitar conhecimento de domínios relacionados

6. **Deploy em Produção:**
   - Criar API REST com FastAPI
   - Containerização (Docker)
   - **Benefício:** Uso prático em aplicações reais

---

# Slide 13 — Estrutura do Repositório

O projeto foi organizado seguindo padrão MLOps (Cookiecutter Data Science adaptado):

```
ufrn-ele-neural-regression/
├── README.md              # Documentação e Histórico de Versões (Git Log)
├── requirements.txt       # Dependências exatas (torch, pandas, numpy, optuna, etc.)
├── .gitignore             # Arquivos a ignorar (dados, modelos, cache)
│
├── data/
│   ├── raw/               # Dados brutos (boston.csv via URL)
│   └── processed/         # Dados normalizados (opcional)
│
├── notebooks/             # Ambiente de Experimentação
│   └── project_main.ipynb # Notebook principal com código completo
│
├── src/                   # Código Modular
│   ├── __init__.py
│   ├── dataset.py         # Carregamento e Dataset PyTorch
│   ├── model.py           # Arquitetura MLP (dinâmica para Optuna)
│   ├── train.py           # Loops de treino e validação
│   └── visualization.py   # Plots de loss e scatter
│
├── models/                # Checkpoints
│   └── best_model_fold.pth
│
└── reports/               # Relatório LaTeX e Apresentação
    ├── figures/           # Imagens geradas
    │   ├── kfold_results.png
    │   ├── learning_curves.png
    │   ├── learning_curves_optimized.png
    │   ├── predictions_scatter.png
    │   ├── predictions_scatter_optimized.png
    │   └── optuna_optimization_history.png
    ├── relatorio_final.tex
    └── presentation_slides.md
```

---

# Slide 14 — Instruções de Reprodutibilidade

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/takaokensei/ufrn-ele-neural-regression.git
   cd ufrn-ele-neural-regression
   ```

2. **Instalar Dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   Principais: `torch==2.0.1`, `pandas==2.0.2`, `scikit-learn==1.3.0`, `optuna==3.3.0`

3. **Executar o Notebook:**
   ```bash
   jupyter notebook notebooks/project_main.ipynb
   ```
   - Execute as células sequencialmente
   - O notebook baixa automaticamente o dataset Boston Housing
   - Seed fixada (42) garante reprodutibilidade

4. **Executar Otimização Bayesiana (Opcional):**
   - Células 28-33: Otimização com Optuna (20 trials, ~25 minutos)
   - Células 34-40: Retreinamento com best_params e visualizações

5. **Compilar o Relatório LaTeX:**
   ```bash
   cd reports
   pdflatex relatorio_final.tex
   pdflatex relatorio_final.tex  # Rodar 2x para referências
   ```
   Ou fazer upload no Overleaf: https://www.overleaf.com/

6. **Analisar os Resultados:**
   - Gráficos salvos em `reports/figures/`
   - Modelo treinado em `models/best_model_fold.pth`
   - Métricas exibidas no notebook e documentadas no LaTeX

---

# Slide 15 — Conclusões

### Resultados Alcançados

- ✅ **Performance Final:** MSE médio de 13.02 (erro ~$3.60k em preços de ~$22.5k)
- ✅ **R² Elevado:** 0.857 (85.7% da variância explicada)
- ✅ **Overfitting Reduzido:** Gap treino-validação de 181% → 35%
- ✅ **Otimização Eficiente:** Optuna testou 20 configurações em ~25 min (vs ~5h Grid Search)
- ✅ **Reprodutibilidade:** Seed fixada e pipeline determinístico

### Lições Aprendidas

1. **Regularização é Fundamental:** Dropout (30%) e L2 (λ=10⁻⁴) foram críticos para generalização
2. **Data Leakage Distorce Resultados:** Normalização correta dentro do K-Fold é essencial
3. **Early Stopping Economiza Recursos:** 60-70% de economia de tempo sem perda de performance
4. **Visualização Revela Padrões:** Scatter plots e curvas identificaram problemas que métricas não capturaram
5. **Trade-off Bias-Variance:** Modelo otimizado tem MSE menor, mas desvio maior (escolha depende do contexto)

### Contribuições do Projeto

- Pipeline MLOps completo e documentado
- Demonstração prática de Otimização Bayesiana
- Análise rigorosa de generalização com K-Fold
- Template reutilizável para projetos acadêmicos

---

# Slide 16 — Referências

- **Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning*. Springer.
- **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep Learning*. MIT Press.
- **Akiba, T., et al. (2019).** Optuna: A Next-generation Hyperparameter Optimization Framework. *KDD 2019*.
- **Srivastava, N., et al. (2014).** Dropout: A Simple Way to Prevent Neural Networks from Overfitting. *JMLR*.
- **Harrison, D., & Rubinfeld, D. L. (1978).** Hedonic housing prices and the demand for clean air. *Journal of Environmental Economics and Management*.

**Repositório:** https://github.com/takaokensei/ufrn-ele-neural-regression

---

# Slide 17 — Agradecimentos

**Obrigado pela atenção!**

**Perguntas?**

**Contato:**  
Cauã Vitor Figueredo Silva  
Matrícula: 20220014216  
UFRN - Departamento de Engenharia Elétrica

