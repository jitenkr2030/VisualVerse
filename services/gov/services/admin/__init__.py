"""
Admin Console Service module.

This module provides comprehensive administrative operations, system configuration,
batch operations, and unified management interfaces for the governance platform.
"""

from .admin_service import (
    AdminService,
    AdminDashboard,
    BatchOperation,
    SystemConfig,
    SystemHealth,
    TenantStats,
    AdminNotification,
    BatchOperationType,
    BatchOperationStatus,
    ConfigCategory,
    create_admin_service
)

__all__ = [
    "AdminService",
    "AdminDashboard",
    "BatchOperation",
    "SystemConfig",
    "SystemHealth",
    "TenantStats",
    "AdminNotification",
    "BatchOperationType",
    "BatchOperationStatus",
    "ConfigCategory",
    "create_admin_service"
]
