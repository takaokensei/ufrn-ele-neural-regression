"""
Módulo de Visualização
Gráficos de Learning Curves e Predições
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import seaborn as sns


# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11


def plot_learning_curves(
    train_losses: List[float],
    val_losses: List[float],
    save_path: str = None
) -> None:
    """
    Plota curvas de aprendizado (Train vs Validation Loss)
    
    Args:
        train_losses: Lista de losses de treino por época
        val_losses: Lista de losses de validação por época
        save_path: Caminho para salvar a figura (opcional)
    """
    epochs = range(1, len(train_losses) + 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_losses, 'b-o', label='Train Loss', linewidth=2, markersize=4)
    plt.plot(epochs, val_losses, 'r-s', label='Validation Loss', linewidth=2, markersize=4)
    
    plt.xlabel('Época', fontsize=12, fontweight='bold')
    plt.ylabel('MSE Loss', fontsize=12, fontweight='bold')
    plt.title('Curvas de Aprendizado - Train vs Validation', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    save_path: str = None
) -> None:
    """
    Plota gráfico de dispersão (Real vs Predito)
    
    Args:
        y_true: Valores reais
        y_pred: Valores preditos
        save_path: Caminho para salvar a figura (opcional)
    """
    plt.figure(figsize=(8, 8))
    
    # Scatter plot
    plt.scatter(y_true, y_pred, alpha=0.6, edgecolors='k', linewidth=0.5, s=50)
    
    # Linha identidade (y=x)
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Predição Ideal (y=x)')
    
    # Calcular R²
    from sklearn.metrics import r2_score
    r2 = r2_score(y_true, y_pred)
    
    plt.xlabel('Valor Real (MEDV)', fontsize=12, fontweight='bold')
    plt.ylabel('Valor Predito (MEDV)', fontsize=12, fontweight='bold')
    plt.title(f'Predições vs Valores Reais (R² = {r2:.3f})', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_kfold_results(
    fold_results: List[float],
    save_path: str = None
) -> None:
    """
    Plota resultados do K-Fold Cross-Validation
    
    Args:
        fold_results: Lista com MSE de cada fold
        save_path: Caminho para salvar a figura (opcional)
    """
    folds = range(1, len(fold_results) + 1)
    mean_mse = np.mean(fold_results)
    std_mse = np.std(fold_results)
    
    plt.figure(figsize=(10, 6))
    plt.bar(folds, fold_results, alpha=0.7, color='steelblue', edgecolor='black')
    plt.axhline(y=mean_mse, color='r', linestyle='--', linewidth=2, label=f'Média: {mean_mse:.2f}')
    plt.fill_between([0.5, len(folds) + 0.5], mean_mse - std_mse, mean_mse + std_mse, 
                     alpha=0.2, color='red', label=f'±1 Desvio Padrão: {std_mse:.2f}')
    
    plt.xlabel('Fold', fontsize=12, fontweight='bold')
    plt.ylabel('MSE', fontsize=12, fontweight='bold')
    plt.title('Resultados do K-Fold Cross-Validation', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.xticks(folds)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

