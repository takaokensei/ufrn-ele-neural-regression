"""
Módulo de Arquitetura de Redes Neurais
MLP (Multi-Layer Perceptron) para Regressão
"""

import torch
import torch.nn as nn
from typing import List


class MLP(nn.Module):
    """
    Multi-Layer Perceptron para Regressão
    
    Arquitetura:
        Input (13) -> Hidden1 (64, ReLU) -> Hidden2 (32, ReLU) -> Output (1)
    """
    
    def __init__(
        self,
        input_dim: int = 13,
        hidden_dims: List[int] = [64, 32],
        output_dim: int = 1
    ):
        """
        Args:
            input_dim: Número de features de entrada
            hidden_dims: Lista com dimensões das camadas ocultas
            output_dim: Dimensão da saída (1 para regressão)
        """
        super(MLP, self).__init__()
        
        layers = []
        
        # Camadas ocultas
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        
        # Camada de saída
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        
        # Inicialização de pesos (Xavier/Glorot)
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Inicialização Xavier para melhor convergência"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            x: Input tensor (batch_size, input_dim)
            
        Returns:
            Output tensor (batch_size, output_dim)
        """
        return self.network(x)
    
    def count_parameters(self) -> int:
        """Retorna o número total de parâmetros treináveis"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

