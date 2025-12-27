"""
ML Services Package

This package contains service modules for the ML layer of the adaptive
learning system, including the main ML orchestrator and supporting services.
"""

from .ml_service import MLService, get_ml_service

__all__ = ['MLService', 'get_ml_service']
