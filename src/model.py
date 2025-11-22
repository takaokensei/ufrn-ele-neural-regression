"""
Módulo de Arquitetura de Redes Neurais
MLP (Multi-Layer Perceptron) para Regressão
"""

import torch
import torch.nn as nn
from typing import List


class MLP(nn.Module):
    """
    Multi-Layer Perceptron Dinâmico para Regressão com Regularização
    
    Suporta arquitetura variável (de 1 a N camadas ocultas) para uso com Optuna.
    Inclui Batch Normalization e Dropout configuráveis.
    
    Exemplo:
        >>> model = MLP(input_dim=13, hidden_dims=[128, 64, 32], dropout_rate=0.3)
        >>> model = MLP.from_trial(trial, input_dim=13)  # Para Optuna
    """
    
    def __init__(
        self,
        input_dim: int = 13,
        hidden_dims: List[int] = [64, 32],
        output_dim: int = 1,
        dropout_rate: float = 0.3,
        use_batch_norm: bool = False
    ):
        """
        Args:
            input_dim: Número de features de entrada
            hidden_dims: Lista com dimensões das camadas ocultas (pode ser dinâmica)
            output_dim: Dimensão da saída (1 para regressão)
            dropout_rate: Taxa de dropout (0.0 a 1.0). Padrão: 0.3 (30%)
            use_batch_norm: Se True, aplica Batch Normalization antes da ativação
        """
        super(MLP, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.dropout_rate = dropout_rate
        self.use_batch_norm = use_batch_norm
        
        layers = []
        
        # Camadas ocultas com Batch Norm (opcional) e Dropout
        prev_dim = input_dim
        for i, hidden_dim in enumerate(hidden_dims):
            # Linear
            layers.append(nn.Linear(prev_dim, hidden_dim))
            
            # Batch Normalization (antes da ativação)
            if use_batch_norm:
                layers.append(nn.BatchNorm1d(hidden_dim))
            
            # Ativação ReLU
            layers.append(nn.ReLU())
            
            # Dropout (após ativação)
            if dropout_rate > 0.0:
                layers.append(nn.Dropout(p=dropout_rate))
            
            prev_dim = hidden_dim
        
        # Camada de saída (sem Dropout, sem BN, sem ativação para regressão)
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        
        # Inicialização de pesos (Xavier/Glorot)
        self._initialize_weights()
    
    @classmethod
    def from_trial(cls, trial, input_dim: int = 13, output_dim: int = 1):
        """
        Factory method para criar MLP dinamicamente a partir de um Optuna Trial.
        
        Args:
            trial: optuna.Trial object
            input_dim: Dimensão de entrada
            output_dim: Dimensão de saída
            
        Returns:
            Instância de MLP com hiperparâmetros sugeridos pelo trial
        """
        n_layers = trial.suggest_int('n_layers', 1, 3)
        hidden_units = trial.suggest_categorical('hidden_units', [16, 32, 64, 128])
        dropout_rate = trial.suggest_float('dropout_rate', 0.1, 0.5)
        use_batch_norm = trial.suggest_categorical('use_batch_norm', [True, False])
        
        # Construir hidden_dims dinamicamente
        # Estratégia: decrescer gradualmente (ex: [128, 64, 32])
        hidden_dims = []
        current_units = hidden_units
        for i in range(n_layers):
            hidden_dims.append(current_units)
            current_units = max(16, current_units // 2)  # Reduzir pela metade, mínimo 16
        
        return cls(
            input_dim=input_dim,
            hidden_dims=hidden_dims,
            output_dim=output_dim,
            dropout_rate=dropout_rate,
            use_batch_norm=use_batch_norm
        )
    
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

