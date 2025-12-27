"""
Licensing and Monetization Service for VisualVerse Creator Platform

This module provides payment processing, license management, revenue
distribution, and subscription management for the VisualVerse Creator
Platform ecosystem.

Author: MiniMax Agent
Version: 1.0.0
"""

from .licensing_service import (
    LicensingService,
    LicenseManager,
    PaymentProcessor,
    RevenueDistributor,
    SubscriptionManager,
    License,
    Product,
    Transaction,
    Subscription,
    RevenueShare,
    PaymentMethod,
    LicenseType,
    TransactionStatus,
    SubscriptionStatus,
    SubscriptionTier,
    PlatformFeeConfig,
    create_licensing_service
)

__version__ = "1.0.0"

__all__ = [
    "LicensingService",
    "LicenseManager",
    "PaymentProcessor",
    "RevenueDistributor",
    "SubscriptionManager",
    "License",
    "Product",
    "Transaction",
    "Subscription",
    "RevenueShare",
    "PaymentMethod",
    "LicenseType",
    "TransactionStatus",
    "SubscriptionStatus",
    "SubscriptionTier",
    "PlatformFeeConfig",
    "create_licensing_service"
]
