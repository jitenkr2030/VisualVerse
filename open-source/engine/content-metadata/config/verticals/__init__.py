"""
Vertical Configurations Package

This package contains configuration files and schemas for all platform verticals:
- MathVerse: Mathematical visualization (algebra, calculus, linear algebra, probability)
- PhysicsVerse: Physics simulations (mechanics, optics, electromagnetism)
- ChemVerse: Chemistry visualizations (molecules, bonding, reactions)
- AlgoVerse: Algorithm visualizations (data structures, sorting, searching)
- FinVerse: Financial visualizations (models, risk, scenario planning)
"""

import json
import os
from typing import Dict, Any, Optional

# Vertical configuration files
VERTICAL_CONFIGS = {
    'math-verse': 'math-verse.json',
    'physics-verse': 'physics-verse.json',
    'chem-verse': 'chem-verse.json',
    'algo-verse': 'algo-verse.json',
    'fin-verse': 'fin-verse.json'
}


def load_vertical_config(vertical_id: str, config_dir: str = None) -> Optional[Dict[str, Any]]:
    """
    Load a vertical configuration from file.
    
    Args:
        vertical_id: The vertical identifier
        config_dir: Optional custom config directory
        
    Returns:
        Configuration dictionary or None if not found
    """
    if config_dir is None:
        config_dir = os.path.dirname(__file__)
    
    config_file = VERTICAL_CONFIGS.get(vertical_id)
    if config_file is None:
        return None
    
    config_path = os.path.join(config_dir, config_file)
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception:
        return None


def list_available_verticals() -> list:
    """
    List all available vertical configurations.
    
    Returns:
        List of vertical identifiers
    """
    return list(VERTICAL_CONFIGS.keys())


def get_vertical_info(vertical_id: str) -> Optional[Dict[str, Any]]:
    """
    Get basic information about a vertical.
    
    Args:
        vertical_id: The vertical identifier
        
    Returns:
        Dictionary with vertical info or None
    """
    config = load_vertical_config(vertical_id)
    if config is None:
        return None
    
    return {
        'id': config.get('id'),
        'name': config.get('name'),
        'version': config.get('version'),
        'description': config.get('description'),
        'domains': [d.get('id') for d in config.get('domains', [])],
        'visualization_types': list(config.get('visualization_types', {}).keys())
    }


__all__ = [
    'VERTICAL_CONFIGS',
    'load_vertical_config',
    'list_available_verticals',
    'get_vertical_info'
]
