# 🧠 UFRN - Neural Regression Project

**Análise de Generalização em Redes Neurais para Regressão de Preços Imobiliários com Validação Cruzada K-Fold**

---

## 📋 Informações do Projeto

- **Instituição:** Universidade Federal do Rio Grande do Norte (UFRN)
- **Departamento:** Engenharia Elétrica - Centro de Tecnologia
- **Autor:** Cauã Vitor Figueredo Silva
- **Matrícula:** 20220014216
- **Data:** Novembro de 2025

---

## 🎯 Objetivo

Este projeto implementa uma **Rede Neural Artificial (MLP)** para regressão de preços imobiliários utilizando o dataset Boston Housing. O foco principal é a análise rigorosa de **generalização**, aplicando técnicas de MLOps como:

- ✅ **K-Fold Cross-Validation (K=5)**
- ✅ **Early Stopping**
- ✅ **Model Checkpointing**
- ✅ **Data Leakage Prevention**
- ✅ **Reprodutibilidade (Seed Fixing)**

---

## 📂 Estrutura do Projeto

```
ufrn-ele-neural-regression/
│
├── README.md              # Documentação e Histórico de Versões
├── requirements.txt       # Dependências exatas (torch, pandas, numpy, etc.)
├── .gitignore             # Arquivos a ignorar (dados, modelos, cache)
│
├── data/
│   ├── raw/               # Dados brutos (boston.csv via URL)
│   └── processed/         # Dados normalizados (opcional)
│
├── notebooks/             # Ambiente de Experimentação
│   └── project_main.ipynb # Notebook principal com código completo
│
├── src/                   # Código Modular (Simulado dentro do Notebook)
│   ├── __init__.py        # Inicializador do pacote
│   ├── dataset.py         # Carregamento e Dataset PyTorch
│   ├── model.py           # Arquitetura MLP
│   ├── train.py           # Loops de treino e validação
│   └── visualization.py   # Plots de loss e scatter
│
├── models/                # Checkpoints
│   └── best_model_fold.pth
│
└── reports/               # Relatório LaTeX
    ├── figures/           # Imagens geradas
    └── relatorio_final.tex
```

### 📁 Descrição das Pastas

| Pasta | Função |
|-------|--------|
| `data/raw/` | Dados originais sem processamento |
| `data/processed/` | Dados após normalização/transformação |
| `notebooks/` | Experimentação e prototyping |
| `src/` | Código modular e reutilizável |
| `models/` | Checkpoints dos melhores modelos |
| `reports/` | Documentação técnica (LaTeX) |

---

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Notebook Principal

```bash
jupyter notebook notebooks/project_main.ipynb
```

### 3. Compilar o Relatório LaTeX

```bash
cd reports
pdflatex relatorio_final.tex
```

---

## 📊 Dataset

**Boston Housing Dataset**
- **Fonte:** http://lib.stat.cmu.edu/datasets/boston
- **Instâncias:** 506
- **Features:** 13 (CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT)
- **Target:** MEDV (Preço mediano das casas em $1000)

---

## 🏗️ Arquitetura da Rede Neural

```
Input Layer (13 features)
    ↓
Hidden Layer 1 (64 neurônios, ReLU)
    ↓
Hidden Layer 2 (32 neurônios, ReLU)
    ↓
Output Layer (1 neurônio, Linear)
```

**Hiperparâmetros:**
- Otimizador: Adam (lr=0.001)
- Loss Function: MSELoss
- Batch Size: 16
- Epochs: 500 (com Early Stopping)
- K-Fold: 5 splits

---

## 📈 Resultados Esperados

- **Curvas de Aprendizado:** Convergência suave entre treino e validação
- **Scatter Plot:** Predições próximas à linha identidade (y=x)
- **Métrica:** MSE médio < 20.0 (após K-Fold)

---

## 🔄 Histórico de Commits Simulado

Este projeto foi desenvolvido seguindo um fluxo de trabalho incremental. Abaixo está o histórico de commits que representa a evolução do código:

```
commit #01 - feat: initialize project structure
  └─ Criação da estrutura de diretórios (data, src, models, reports)
  └─ Adição de requirements.txt e .gitignore

commit #02 - feat: add data loading module
  └─ Implementação de src/dataset.py
  └─ Função robusta para download do Boston Housing Dataset
  └─ Tratamento de cabeçalho complexo da URL original

commit #03 - feat: implement MLP architecture
  └─ Criação de src/model.py
  └─ Classe MLP com 2 camadas ocultas
  └─ Utilização de torch.nn.Module

commit #04 - feat: add preprocessing with StandardScaler
  └─ Integração do StandardScaler no pipeline
  └─ Prevenção de Data Leakage (fit apenas no treino)

commit #05 - feat: implement K-Fold Cross-Validation
  └─ Loop manual de K-Fold (K=5)
  └─ Separação correta de treino/validação

commit #06 - feat: add training loop with validation
  └─ Implementação de src/train.py
  └─ Loop de treino com cálculo de loss

commit #07 - feat: implement Early Stopping mechanism
  └─ Lógica de parada antecipada (patience=20)
  └─ Monitoramento de val_loss para evitar overfitting

commit #08 - feat: add Model Checkpointing
  └─ Salvamento automático do melhor modelo
  └─ torch.save() e torch.load() integrados

commit #09 - fix: adjust learning rate for better convergence
  └─ Mudança de lr=0.01 para lr=0.001
  └─ Melhoria na estabilidade do treino

commit #10 - feat: add visualization module
  └─ Criação de src/visualization.py
  └─ Gráfico de Learning Curves (train vs validation)
  └─ Scatter Plot (Real vs Predito)

commit #11 - feat: implement seed fixing for reproducibility
  └─ Fixação de seeds (torch, numpy, random)
  └─ Garantia de resultados determinísticos

commit #12 - refactor: modularize code structure
  └─ Separação de responsabilidades entre módulos
  └─ Type hints adicionados para melhor legibilidade

commit #13 - docs: add LaTeX report template
  └─ Criação de reports/relatorio_final.tex
  └─ Estrutura ABNT com Introduction, Methodology, Results

commit #14 - feat: integrate metrics aggregation
  └─ Cálculo de média e desvio padrão do MSE
  └─ Tabela final com resultados do K-Fold

commit #15 - style: improve plot aesthetics
  └─ Ajuste de fontes, cores e legendas
  └─ Gráficos profissionais para publicação

commit #16 - test: validate data leakage prevention
  └─ Verificação manual do fluxo de normalização
  └─ Confirmação de que scaler não vê dados de validação

commit #17 - docs: complete LaTeX report content
  └─ Preenchimento de Introduction e Methodology
  └─ Adição de placeholders para tabelas de resultados

commit #18 - feat: add analysis of generalization
  └─ Célula Markdown com análise final
  └─ Classificação: Overfitting/Underfitting/Generalização

commit #19 - docs: update README with usage instructions
  └─ Adição de seção "Como Executar"
  └─ Documentação completa da estrutura do projeto

commit #20 - chore: final cleanup and organization
  └─ Remoção de arquivos temporários
  └─ Validação final de todos os módulos
```

---

## 🛠️ Tecnologias Utilizadas

- **PyTorch 2.0.1** - Framework de Deep Learning
- **scikit-learn 1.3.0** - Pré-processamento e K-Fold
- **Pandas 2.0.2** - Manipulação de dados
- **Matplotlib 3.7.1** - Visualização
- **NumPy 1.24.3** - Operações numéricas

---

## 📝 Próximos Passos

- [ ] Experimentar arquiteturas mais profundas
- [ ] Testar regularização (Dropout, L2)
- [ ] Implementar Grid Search para hiperparâmetros
- [ ] Adicionar análise de SHAP Values
- [ ] Deployar modelo via FastAPI

---

## 📄 Licença

Este projeto é de uso acadêmico para a disciplina de Engenharia Elétrica da UFRN.

---

## 👤 Contato

**Cauã Vitor Figueredo Silva**  
Matrícula: 20220014216  
UFRN - Departamento de Engenharia Elétrica

