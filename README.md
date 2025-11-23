# Neural Regression with K-Fold Cross-Validation

> Rigorous generalization analysis in neural networks for real estate price prediction using Boston Housing dataset.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0.1-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

---

## Overview

This project implements a Multi-Layer Perceptron (MLP) for real estate price regression with emphasis on robust generalization evaluation. The implementation follows MLOps best practices, including reproducible experimentation, data leakage prevention, and systematic model validation.

**Institution:** Federal University of Rio Grande do Norte (UFRN)  
**Department:** Electrical Engineering  
**Author:** Cauã Vitor Figueredo Silva  
**Student ID:** 20220014216  
**Date:** November 2025

---

## Key Features

- **K-Fold Cross-Validation** (K=5) for robust performance estimation
- **Early Stopping** with configurable patience to prevent overfitting
- **Model Checkpointing** to preserve best-performing weights
- **Data Leakage Prevention** through proper preprocessing pipeline
- **Reproducibility** via fixed random seeds across libraries
- **Modular Architecture** following software engineering principles

---

## Project Structure

```
ufrn-ele-neural-regression/
│
├── data/
│   ├── raw/                    # Original datasets
│   └── processed/              # Normalized/transformed data
│
├── src/
│   ├── dataset.py              # Data loading and PyTorch Dataset
│   ├── model.py                # MLP architecture definition
│   ├── train.py                # Training and validation loops
│   └── visualization.py        # Loss curves and scatter plots
│
├── notebooks/
│   └── project_main.ipynb      # Complete experimental workflow
│
├── models/                     # Model checkpoints
├── reports/                    # LaTeX documentation
│
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## Dataset

**Boston Housing Dataset**
- **Source:** Carnegie Mellon University Statistical Library
- **Instances:** 506
- **Features:** 13 (socioeconomic and environmental indicators)
- **Target:** Median home value (MEDV) in $1000s

### Feature Description

| Feature | Description |
|---------|-------------|
| CRIM | Per capita crime rate |
| ZN | Proportion of residential land zoned for large lots |
| INDUS | Proportion of non-retail business acres |
| CHAS | Charles River proximity (binary) |
| NOX | Nitric oxides concentration |
| RM | Average number of rooms per dwelling |
| AGE | Proportion of owner-occupied units built prior to 1940 |
| DIS | Weighted distances to employment centers |
| RAD | Accessibility to radial highways |
| TAX | Property tax rate |
| PTRATIO | Pupil-teacher ratio |
| B | Proportion of Black residents |
| LSTAT | Percentage of lower status population |

---

## Model Architecture

```
MLP Sequential Architecture
├── Input Layer: 13 features
├── Hidden Layer 1: 64 neurons + ReLU
├── Hidden Layer 2: 32 neurons + ReLU
└── Output Layer: 1 neuron (linear)
```

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Loss Function | Mean Squared Error (MSE) |
| Batch Size | 16 |
| Max Epochs | 500 |
| Early Stopping Patience | 20 |
| K-Fold Splits | 5 |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ufrn-ele-neural-regression.git
cd ufrn-ele-neural-regression

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
torch==2.0.1
scikit-learn==1.3.0
pandas==2.0.2
matplotlib==3.7.1
numpy==1.24.3
jupyter==1.0.0
```

---

## Usage

### Running the Main Notebook

```bash
jupyter notebook notebooks/project_main.ipynb
```

### Training Pipeline

The training pipeline automatically:
1. Downloads and loads the Boston Housing dataset
2. Applies StandardScaler normalization (fitted on training data only)
3. Performs 5-fold cross-validation
4. Trains MLP with early stopping
5. Saves best model checkpoint per fold
6. Generates learning curves and prediction scatter plots
7. Computes aggregate performance metrics

### Generating Report

```bash
cd reports
pdflatex relatorio_final.tex
bibtex relatorio_final
pdflatex relatorio_final.tex
pdflatex relatorio_final.tex
```

---

## Methodology

### Cross-Validation Strategy

The implementation uses stratified K-Fold cross-validation to ensure:
- Each fold serves as validation set exactly once
- Training data remains independent from validation data
- Performance metrics reflect true generalization capability

### Data Leakage Prevention

Normalization is performed within each fold:
```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)  # No fit on validation
```

### Reproducibility

Random seeds are fixed for:
- PyTorch operations (`torch.manual_seed`)
- NumPy operations (`np.random.seed`)
- Python random module (`random.seed`)

---

## Expected Results

### Performance Metrics
- **Target MSE:** < 20.0 (across all folds)
- **Standard Deviation:** Low variance between folds indicates stable generalization

### Visualizations
- **Learning Curves:** Training and validation loss converging without significant gap
- **Scatter Plot:** Predictions closely aligned with identity line (y=x)

---

## Development Timeline

The project followed an incremental development approach:

1. **Infrastructure** (Commits #01-#02): Project structure and data loading
2. **Model Implementation** (Commits #03-#04): MLP architecture and preprocessing
3. **Training Pipeline** (Commits #05-#08): K-Fold, training loop, early stopping, checkpointing
4. **Optimization** (Commits #09-#11): Hyperparameter tuning, visualization, reproducibility
5. **Refinement** (Commits #12-#16): Code modularization, documentation, validation
6. **Finalization** (Commits #17-#20): Report completion, analysis, cleanup

---

## Future Enhancements

- [ ] Experiment with deeper architectures (3+ hidden layers)
- [ ] Implement regularization techniques (Dropout, L2)
- [ ] Conduct hyperparameter grid search
- [ ] Add SHAP values for feature importance analysis
- [ ] Deploy model via REST API (FastAPI)
- [ ] Integrate MLflow for experiment tracking

---

## Contributing

This is an academic project. For suggestions or improvements, please contact the author.

---

## Citation

If you use this code for academic purposes, please cite:

```bibtex
@misc{silva2025neural,
  author = {Silva, Cauã Vitor Figueredo},
  title = {Neural Regression with K-Fold Cross-Validation},
  year = {2025},
  institution = {Federal University of Rio Grande do Norte},
  department = {Electrical Engineering}
}
```

---

## License

This project is developed for academic purposes at the Federal University of Rio Grande do Norte (UFRN). All rights reserved for educational use.

---

## Contact

**Cauã Vitor Figueredo Silva**  
Student ID: 20220014216  
Department of Electrical Engineering  
Federal University of Rio Grande do Norte (UFRN)

For inquiries, please use the institutional communication channels.