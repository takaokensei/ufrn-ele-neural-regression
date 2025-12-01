"""
Módulo para pré-processamento de dados
"""

import os
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path


# Valores médios e desvios padrão do Boston Housing Dataset (para normalização manual)
BOSTON_MEAN = np.array([
    3.613524,   # CRIM
    11.363636,  # ZN
    11.136779,  # INDUS
    0.069170,   # CHAS
    0.554695,   # NOX
    6.284634,   # RM
    68.574901,  # AGE
    3.795043,   # DIS
    9.549407,   # RAD
    408.237154, # TAX
    18.455534,  # PTRATIO
    356.674032, # B
    12.653063   # LSTAT
])

BOSTON_STD = np.array([
    8.601545,   # CRIM
    23.322453,  # ZN
    6.860353,   # INDUS
    0.253994,   # CHAS
    0.115878,   # NOX
    0.702617,   # RM
    28.148861,  # AGE
    2.105710,   # DIS
    8.707259,   # RAD
    168.537116, # TAX
    2.164946,   # PTRATIO
    91.294864,  # B
    7.141062    # LSTAT
])

# Ranges mínimos e máximos para validação
BOSTON_MIN = np.array([
    0.0,    # CRIM
    0.0,    # ZN
    0.46,   # INDUS
    0.0,    # CHAS
    0.385,  # NOX
    3.561,  # RM
    2.9,    # AGE
    1.1296, # DIS
    1.0,    # RAD
    187.0,  # TAX
    12.6,   # PTRATIO
    0.32,   # B
    1.73    # LSTAT
])

BOSTON_MAX = np.array([
    88.9762,  # CRIM
    100.0,    # ZN
    27.74,    # INDUS
    1.0,      # CHAS
    0.871,    # NOX
    8.78,     # RM
    100.0,    # AGE
    12.1265,  # DIS
    24.0,     # RAD
    711.0,    # TAX
    22.0,     # PTRATIO
    396.9,    # B
    37.97     # LSTAT
])


def load_scaler(scaler_path: str = None) -> StandardScaler:
    """
    Carrega o StandardScaler salvo (se disponível).
    
    Args:
        scaler_path: Caminho para o arquivo .pkl do scaler
        
    Returns:
        StandardScaler ou None se não encontrado
    """
    if scaler_path is None:
        base_path = Path(__file__).parent.parent.parent
        scaler_path = base_path / "streamlit_app" / "assets" / "scaler.pkl"
    
    try:
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                return pickle.load(f)
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível carregar scaler: {e}")
    
    return None


def preprocess_input(features: list, use_scaler: bool = False) -> torch.Tensor:
    """
    Pré-processa input do usuário para formato do modelo.
    
    Args:
        features: Lista com 13 valores de features na ordem:
                  [CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT]
        use_scaler: Se True, tenta usar StandardScaler salvo
        
    Returns:
        Tensor PyTorch normalizado (1, 13)
    """
    # Converter para numpy array
    features_array = np.array(features, dtype=np.float32).reshape(1, -1)
    
    # Validar número de features
    if features_array.shape[1] != 13:
        raise ValueError(f"Esperado 13 features, recebido {features_array.shape[1]}")
    
    # Normalizar
    if use_scaler:
        scaler = load_scaler()
        if scaler:
            features_scaled = scaler.transform(features_array)
        else:
            # Fallback para normalização manual
            features_scaled = (features_array - BOSTON_MEAN) / BOSTON_STD
    else:
        # Normalização manual usando valores do dataset
        features_scaled = (features_array - BOSTON_MEAN) / BOSTON_STD
    
    # Converter para tensor
    return torch.FloatTensor(features_scaled)


def validate_features(features: list) -> tuple[bool, str]:
    """
    Valida se os valores das features estão dentro dos ranges esperados.
    
    Args:
        features: Lista com 13 valores de features
        
    Returns:
        (is_valid, error_message)
    """
    if len(features) != 13:
        return False, f"Esperado 13 features, recebido {len(features)}"
    
    features_array = np.array(features)
    
    # Verificar ranges
    for i, (val, min_val, max_val) in enumerate(zip(features_array, BOSTON_MIN, BOSTON_MAX)):
        if val < min_val or val > max_val:
            feature_names = [
                "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
                "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
            ]
            return False, (
                f"Feature {feature_names[i]} ({val:.2f}) está fora do range "
                f"esperado [{min_val:.2f}, {max_val:.2f}]"
            )
    
    return True, ""


def get_feature_defaults() -> dict:
    """
    Retorna valores padrão (média) para cada feature.
    
    Returns:
        Dicionário com nome da feature e valor padrão
    """
    feature_names = [
        "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
        "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
    ]
    
    return {
        name: float(mean) 
        for name, mean in zip(feature_names, BOSTON_MEAN)
    }


def get_feature_ranges() -> dict:
    """
    Retorna ranges (min, max) para cada feature.
    
    Returns:
        Dicionário com nome da feature e tupla (min, max)
    """
    feature_names = [
        "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
        "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
    ]
    
    return {
        name: (float(min_val), float(max_val))
        for name, min_val, max_val in zip(feature_names, BOSTON_MIN, BOSTON_MAX)
    }

