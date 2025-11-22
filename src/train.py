"""
Módulo de Treinamento e Validação
Loops de treino com Early Stopping
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Tuple, Dict
import numpy as np


def train_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device
) -> float:
    """
    Executa uma época de treinamento
    
    Args:
        model: Modelo neural
        dataloader: DataLoader de treino
        criterion: Função de perda
        optimizer: Otimizador
        device: Device (CPU/GPU)
        
    Returns:
        Loss médio da época
    """
    model.train()
    total_loss = 0.0
    n_batches = 0
    
    for X_batch, y_batch in dataloader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device).unsqueeze(1)
        
        # Forward pass
        predictions = model(X_batch)
        loss = criterion(predictions, y_batch)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        n_batches += 1
    
    return total_loss / n_batches


def validate_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device
) -> float:
    """
    Executa validação (sem gradientes)
    
    Args:
        model: Modelo neural
        dataloader: DataLoader de validação
        criterion: Função de perda
        device: Device (CPU/GPU)
        
    Returns:
        Loss médio da validação
    """
    model.eval()
    total_loss = 0.0
    n_batches = 0
    
    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device).unsqueeze(1)
            
            predictions = model(X_batch)
            loss = criterion(predictions, y_batch)
            
            total_loss += loss.item()
            n_batches += 1
    
    return total_loss / n_batches


class EarlyStopping:
    """
    Implementação de Early Stopping para prevenir Overfitting
    """
    
    def __init__(self, patience: int = 20, min_delta: float = 0.0):
        """
        Args:
            patience: Número de épocas sem melhoria antes de parar
            min_delta: Melhoria mínima para considerar progresso
        """
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
    
    def __call__(self, val_loss: float) -> bool:
        """
        Verifica se deve parar o treinamento
        
        Args:
            val_loss: Loss de validação atual
            
        Returns:
            True se deve parar, False caso contrário
        """
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0
        
        return self.early_stop


def get_predictions(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Obtém predições do modelo
    
    Args:
        model: Modelo neural
        dataloader: DataLoader
        device: Device (CPU/GPU)
        
    Returns:
        Tupla (y_true, y_pred)
    """
    model.eval()
    y_true_list = []
    y_pred_list = []
    
    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch = X_batch.to(device)
            predictions = model(X_batch)
            
            y_true_list.append(y_batch.numpy())
            y_pred_list.append(predictions.cpu().numpy())
    
    y_true = np.concatenate(y_true_list)
    y_pred = np.concatenate(y_pred_list).flatten()
    
    return y_true, y_pred

