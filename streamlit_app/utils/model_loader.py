"""
Módulo para carregamento do modelo treinado
"""

import torch
import sys
import os
from pathlib import Path

# Adicionar src ao path para importar MLP
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.model import MLP

# Importar streamlit apenas se disponível (para warnings)
try:
    import streamlit as st
except ImportError:
    st = None


def load_model(checkpoint_path: str = None) -> MLP:
    """
    Carrega o modelo treinado do checkpoint.
    
    Args:
        checkpoint_path: Caminho para o arquivo .pth. Se None, tenta múltiplos locais.
        
    Returns:
        Modelo MLP carregado e em modo eval
    """
    if checkpoint_path is None:
        # Tentar múltiplos caminhos (para deploy no Streamlit Cloud e local)
        possible_paths = [
            # Caminho relativo à raiz do projeto (local)
            Path(__file__).parent.parent.parent / "models" / "best_model_fold.pth",
            # Caminho dentro de streamlit_app (alternativo local)
            Path(__file__).parent.parent / "assets" / "model" / "best_model_fold.pth",
            # Caminho absoluto do Streamlit Cloud
            Path("/mount/src/ufrn-ele-neural-regression/models/best_model_fold.pth"),
            # Caminho alternativo do Streamlit Cloud
            Path("/mount/src/ufrn-ele-neural-regression/streamlit_app/assets/model/best_model_fold.pth"),
        ]
        
        checkpoint_path = None
        for path in possible_paths:
            if os.path.exists(path):
                checkpoint_path = path
                break
        
        if checkpoint_path is None:
            raise FileNotFoundError(
                f"Checkpoint não encontrado em nenhum dos locais esperados:\n"
                + "\n".join([f"  - {p}" for p in possible_paths]) +
                "\n\nCertifique-se de que o modelo foi treinado e salvo."
            )
    
    # Verificar se o arquivo existe
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(
            f"Checkpoint não encontrado em: {checkpoint_path}\n"
            "Certifique-se de que o modelo foi treinado e salvo."
        )
    
    # Carregar checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    # Extrair configuração do modelo
    if 'architecture' in checkpoint:
        model_config = checkpoint['architecture']
    elif 'model_config' in checkpoint:
        model_config = checkpoint['model_config']
    else:
        # Configuração padrão (baseline)
        model_config = {
            'input_dim': 13,
            'hidden_dims': [64, 32],
            'output_dim': 1,
            'dropout_rate': 0.3,
            'use_batch_norm': False
        }
    
    # Adicionar dropout_rate se não estiver presente
    if 'dropout_rate' not in model_config:
        model_config['dropout_rate'] = 0.3
    
    # Adicionar use_batch_norm se não estiver presente
    if 'use_batch_norm' not in model_config:
        model_config['use_batch_norm'] = False
    
    # Instanciar modelo
    model = MLP(**model_config)
    
    # Carregar pesos se disponíveis
    model_loaded = False
    if 'model_state_dict' in checkpoint:
        try:
            model.load_state_dict(checkpoint['model_state_dict'])
            model_loaded = True
        except Exception as e:
            if st:
                st.warning(f"⚠️ Erro ao carregar model_state_dict: {e}")
            else:
                print(f"⚠️ Erro ao carregar model_state_dict: {e}")
    elif 'state_dict' in checkpoint:
        try:
            model.load_state_dict(checkpoint['state_dict'])
            model_loaded = True
        except Exception as e:
            if st:
                st.warning(f"⚠️ Erro ao carregar state_dict: {e}")
            else:
                print(f"⚠️ Erro ao carregar state_dict: {e}")
    elif 'model' in checkpoint:
        # Se o modelo completo foi salvo
        model = checkpoint['model']
        model_loaded = True
    else:
        # Tentar carregar como modelo completo
        try:
            # Se o checkpoint é o modelo completo
            if isinstance(checkpoint, torch.nn.Module):
                model = checkpoint
                model_loaded = True
            else:
                raise KeyError("state_dict não encontrado")
        except:
            pass
    
    # Avisar apenas se realmente não foi possível carregar
    if not model_loaded:
        if st:
            st.warning("⚠️ Aviso: Checkpoint não contém state_dict válido. Modelo será inicializado aleatoriamente.")
        else:
            print("⚠️ Aviso: Checkpoint não contém state_dict válido. Modelo será inicializado aleatoriamente.")
    
    # Colocar em modo eval
    model.eval()
    
    return model


def get_model_info(checkpoint_path: str = None) -> dict:
    """
    Retorna informações sobre o modelo carregado.
    
    Args:
        checkpoint_path: Caminho para o arquivo .pth. Se None, tenta múltiplos locais.
        
    Returns:
        Dicionário com informações do modelo
    """
    if checkpoint_path is None:
        # Tentar múltiplos caminhos (mesma lógica do load_model)
        possible_paths = [
            Path(__file__).parent.parent.parent / "models" / "best_model_fold.pth",
            Path(__file__).parent.parent / "assets" / "model" / "best_model_fold.pth",
            Path("/mount/src/ufrn-ele-neural-regression/models/best_model_fold.pth"),
            Path("/mount/src/ufrn-ele-neural-regression/streamlit_app/assets/model/best_model_fold.pth"),
        ]
        
        checkpoint_path = None
        for path in possible_paths:
            if os.path.exists(path):
                checkpoint_path = path
                break
        
        if checkpoint_path is None:
            raise FileNotFoundError("Checkpoint não encontrado para obter informações do modelo.")
    
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    info = {
        'fold': checkpoint.get('fold', 'N/A'),
        'mse': checkpoint.get('mse', 'N/A'),
        'r2': checkpoint.get('r2', 'N/A'),
        'architecture': checkpoint.get('architecture', {}),
        'config': checkpoint.get('config', {})
    }
    
    return info

