"""
UFRN - Projeto Neural Regression
Módulo de Machine Learning para Regressão de Preços Imobiliários

Autor: Cauã Vitor Figueredo Silva
Matrícula: 20220014216
"""

__version__ = "1.0.0"
__author__ = "Cauã Vitor Figueredo Silva"

from .dataset import load_boston_data, BostonDataset
from .model import MLP
from .train import train_epoch, validate_epoch
from .visualization import plot_learning_curves, plot_predictions

__all__ = [
    'load_boston_data',
    'BostonDataset',
    'MLP',
    'train_epoch',
    'validate_epoch',
    'plot_learning_curves',
    'plot_predictions'
]

