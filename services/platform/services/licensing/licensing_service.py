"""
Licensing and Monetization Service - Core Implementation

This module provides the core functionality for payment processing, license
management, revenue distribution, and subscription management in the
VisualVerse Creator Platform.

Author: MiniMax Agent
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP
import json
import uuid
import hashlib
import logging
import threading
import re

from visualverse.platform.packages.shared_types import (
    User,
    Product as DomainProduct,
    Transaction as DomainTransaction,
    License as DomainLicense,
    LicenseType as DomainLicenseType,
)


logger = logging.getLogger(__name__)


class LicenseType(str, Enum):
    """Types of content licenses."""
    FREE = "free"
    PERSONAL = "personal"
    COMMERCIAL = "commercial"
    INSTITUTIONAL = "institutional"
    SUBSCRIPTION = "subscription"
    TEMPORARY = "temporary"


class TransactionStatus(str, Enum):
    """Status of a transaction."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class SubscriptionStatus(str, Enum):
    """Status of a subscription."""
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    TRIAL = "trial"


class SubscriptionTier(str, Enum):
    """Subscription tiers for creators and consumers."""
    FREE = "free"
    CREATOR = "creator"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


@dataclass
class PlatformFeeConfig:
    """
    Platform fee configuration for monetization.
    
    Attributes:
        standard_fee_percent: Standard platform fee percentage
        creator_fee_percent: Creator revenue share percentage
        transaction_fee_fixed: Fixed fee per transaction
        minimum_transaction_amount: Minimum transaction amount
        maximum_discount_percent: Maximum discount allowed
        stripe_fee_percent: Stripe payment processing fee
    """
    standard_fee_percent: float = 30.0
    creator_fee_percent: float = 70.0
    transaction_fee_fixed: float = 0.30
    minimum_transaction_amount: float = 0.99
    maximum_discount_percent: float = 50.0
    stripe_fee_percent: float = 2.9
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "standardFeePercent": self.standard_fee_percent,
            "creatorFeePercent": self.creator_fee_percent,
            "transactionFeeFixed": self.transaction_fee_fixed,
            "minimumTransactionAmount": self.minimum_transaction_amount,
            "maximumDiscountPercent": self.maximum_discount_percent,
            "stripeFeePercent": self.stripe_fee_percent
        }


@dataclass
class Product:
    """
    Marketplace product representation.
    
    Attributes:
        id: Unique product identifier
        project_id: Associated project identifier
        seller_id: Creator selling the product
        title: Product title
        description: Product description
        price: Product price
        currency: Currency code (USD, INR, etc.)
        license_type: Type of license
        features: List of included features
        is_active: Whether product is available
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    project_id: str
    seller_id: str
    title: str
    description: str = ""
    price: float = 0.0
    currency: str = "USD"
    license_type: str = LicenseType.PERSONAL.value
    features: List[str] = field(default_factory=list)
    is_active: bool = True
    discount_percent: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "sellerId": self.seller_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "currency": self.currency,
            "licenseType": self.license_type,
            "features": self.features,
            "isActive": self.is_active,
            "discountPercent": self.discount_percent,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    @property
    def effective_price(self) -> float:
        """Get the price after discount."""
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price


@dataclass
class Transaction:
    """
    Transaction record for monetization.
    
    Attributes:
        id: Unique transaction identifier
        buyer_id: User making the purchase
        seller_id: Creator receiving payment
        product_id: Product being purchased
        amount: Transaction amount
        platform_fee: Platform commission
        net_amount: Amount after fees
        currency: Currency code
        status: Transaction status
        payment_method: Payment method used
        stripe_payment_id: Stripe payment intent ID
        stripe_transfer_id: Stripe transfer ID
        discount_applied: Discount percentage applied
        coupon_code: Coupon code used if any
        created_at: Transaction timestamp
        completed_at: Completion timestamp
        metadata: Additional transaction metadata
    """
    id: str
    buyer_id: str
    seller_id: str
    product_id: str
    amount: float
    platform_fee: float
    net_amount: float
    currency: str = "USD"
    status: str = TransactionStatus.PENDING.value
    payment_method: str = ""
    stripe_payment_id: Optional[str] = None
    stripe_transfer_id: Optional[str] = None
    discount_applied: float = 0.0
    coupon_code: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "buyerId": self.buyer_id,
            "sellerId": self.seller_id,
            "productId": self.product_id,
            "amount": self.amount,
            "platformFee": self.platform_fee,
            "netAmount": self.net_amount,
            "currency": self.currency,
            "status": self.status,
            "paymentMethod": self.payment_method,
            "stripePaymentId": self.stripe_payment_id,
            "stripeTransferId": self.stripe_transfer_id,
            "discountApplied": self.discount_applied,
            "couponCode": self.coupon_code,
            "createdAt": self.created_at.isoformat(),
            "completedAt": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata
        }


@dataclass
class License:
    """
    Content license record.
    
    Attributes:
        id: Unique license identifier
        user_id: Licensed user
        product_id: Product being licensed
        license_type: Type of license
        starts_at: License start timestamp
        expires_at: License expiration (None for perpetual)
        is_active: Whether license is valid
        usage_count: Number of times license used
        max_uses: Maximum allowed uses (None for unlimited)
        restrictions: Dictionary of usage restrictions
        scope: License scope (personal, commercial, etc.)
        created_at: Creation timestamp
        metadata: Additional license metadata
    """
    id: str
    user_id: str
    product_id: str
    license_type: str
    starts_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    usage_count: int = 0
    max_uses: Optional[int] = None
    restrictions: Dict[str, Any] = field(default_factory=dict)
    scope: str = "personal"
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "productId": self.product_id,
            "licenseType": self.license_type,
            "startsAt": self.starts_at.isoformat(),
            "expiresAt": self.expires_at.isoformat() if self.expires_at else None,
            "isActive": self.is_active,
            "usageCount": self.usage_count,
            "maxUses": self.max_uses,
            "restrictions": self.restrictions,
            "scope": self.scope,
            "createdAt": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    def is_valid(self) -> bool:
        """Check if license is currently valid."""
        now = datetime.utcnow()
        
        if not self.is_active:
            return False
        
        if self.expires_at and now > self.expires_at:
            return False
        
        if self.max_uses and self.usage_count >= self.max_uses:
            return False
        
        return True
    
    def can_use(self, context: Dict[str, Any] = None) -> Tuple[bool, str]:
        """
        Check if license can be used in the given context.
        
        Args:
            context: Usage context (ip, device, location, etc.)
            
        Returns:
            Tuple of (allowed, reason)
        """
        if not self.is_valid():
            return False, "License is not valid or has expired"
        
        # Check scope restrictions
        if "scope" in self.restrictions:
            if context and "usage_type" in context:
                if context["usage_type"] not in self.restrictions["scope"]:
                    return False, f"License does not cover {context.get('usage_type')} usage"
        
        # Check location restrictions
        if "allowed_countries" in self.restrictions:
            if context and "country" in context:
                if context["country"] not in self.restrictions["allowed_countries"]:
                    return False, "License not valid in your region"
        
        # Check device restrictions
        if "max_devices" in self.restrictions:
            if context and "device_id" in context:
                if self.usage_count >= self.restrictions["max_devices"]:
                    return False, "Maximum device limit reached"
        
        return True, "License is valid"
    
    def record_usage(self, context: Dict[str, Any] = None):
        """Record a license usage."""
        self.usage_count += 1
        
        if context:
            if "usage_history" not in self.metadata:
                self.metadata["usage_history"] = []
            
            self.metadata["usage_history"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "context": context
            })


@dataclass
class Subscription:
    """
    User subscription record.
    
    Attributes:
        id: Unique subscription identifier
        user_id: Subscribed user
        tier: Subscription tier
        status: Subscription status
        stripe_subscription_id: Stripe subscription ID
        stripe_customer_id: Stripe customer ID
        current_period_start: Current period start
        current_period_end: Current period end
        cancel_at_period_end: Whether subscription will cancel
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    user_id: str
    tier: str
    status: str = SubscriptionStatus.ACTIVE.value
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    current_period_start: datetime = field(default_factory=datetime.utcnow)
    current_period_end: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=30))
    cancel_at_period_end: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "tier": self.tier,
            "status": self.status,
            "stripeSubscriptionId": self.stripe_subscription_id,
            "stripeCustomerId": self.stripe_customer_id,
            "currentPeriodStart": self.current_period_start.isoformat(),
            "currentPeriodEnd": self.current_period_end.isoformat(),
            "cancelAtPeriodEnd": self.cancel_at_period_end,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    def is_active(self) -> bool:
        """Check if subscription is currently active."""
        now = datetime.utcnow()
        return (
            self.status == SubscriptionStatus.ACTIVE.value or
            self.status == SubscriptionStatus.TRIAL.value
        ) and now < self.current_period_end
    
    def days_remaining(self) -> int:
        """Get days remaining in current period."""
        now = datetime.utcnow()
        delta = self.current_period_end - now
        return max(0, delta.days)


@dataclass
class RevenueShare:
    """
    Revenue share record for creator earnings.
    
    Attributes:
        id: Unique record identifier
        transaction_id: Associated transaction
        creator_id: Creator receiving share
        gross_amount: Total transaction amount
        platform_fee: Platform commission
        net_amount: Creator's share
        currency: Currency code
        status: Payment status
        paid_at: Payment completion timestamp
        created_at: Record creation timestamp
    """
    id: str
    transaction_id: str
    creator_id: str
    gross_amount: float
    platform_fee: float
    net_amount: float
    currency: str = "USD"
    status: str = "pending"
    paid_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "transactionId": self.transaction_id,
            "creatorId": self.creator_id,
            "grossAmount": self.gross_amount,
            "platformFee": self.platform_fee,
            "netAmount": self.net_amount,
            "currency": self.currency,
            "status": self.status,
            "paidAt": self.paid_at.isoformat() if self.paid_at else None,
            "createdAt": self.created_at.isoformat()
        }


@dataclass
class PaymentMethod:
    """
    Payment method record.
    
    Attributes:
        id: Unique identifier
        user_id: Associated user
        type: Payment method type (card, bank_account, etc.)
        last_four: Last four digits
        brand: Card brand (visa, mastercard, etc.)
        expiry_month: Card expiry month
        expiry_year: Card expiry year
        stripe_payment_method_id: Stripe payment method ID
        is_default: Whether this is the default payment method
        created_at: Creation timestamp
    """
    id: str
    user_id: str
    type: str
    last_four: str
    brand: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    stripe_payment_method_id: Optional[str] = None
    is_default: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "type": self.type,
            "lastFour": self.last_four,
            "brand": self.brand,
            "expiryMonth": self.expiry_month,
            "expiryYear": self.expiry_year,
            "stripePaymentMethodId": self.stripe_payment_method_id,
            "isDefault": self.is_default,
            "createdAt": self.created_at.isoformat()
        }
    
    def is_expired(self) -> bool:
        """Check if payment method is expired."""
        if self.expiry_month and self.expiry_year:
            now = datetime.utcnow()
            if now.year > self.expiry_year:
                return True
            if now.year == self.expiry_year and now.month > self.expiry_month:
                return True
        return False


class LicensingService:
    """
    Core licensing and monetization service.
    
    This service manages:
    - Product creation and management
    - License issuance and validation
    - Transaction processing
    - Payment processing
    - Revenue distribution
    - Subscription management
    - Creator payouts
    
    Attributes:
        storage_dir: Directory for persisting data
        products: Dictionary of products by ID
        transactions: Dictionary of transactions by ID
        licenses: Dictionary of licenses by ID
        subscriptions: Dictionary of subscriptions by ID
        revenue_shares: Dictionary of revenue shares by ID
        payment_methods: Dictionary of payment methods by ID
        fee_config: Platform fee configuration
        lock: Thread lock for concurrent operations
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the licensing service.
        
        Args:
            storage_dir: Directory for persisting data
        """
        self.storage_dir = storage_dir or "/tmp/visualverse-licensing"
        
        self.products: Dict[str, Product] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.licenses: Dict[str, License] = {}
        self.subscriptions: Dict[str, Subscription] = {}
        self.revenue_shares: Dict[str, RevenueShare] = {}
        self.payment_methods: Dict[str, PaymentMethod] = {}
        self.creator_balances: Dict[str, float] = {}
        
        self.fee_config = PlatformFeeConfig()
        self.lock = threading.RLock()
        
        # Load existing data
        self._load_state()
        
        logger.info("LicensingService initialized")
    
    def _load_state(self):
        """Load persisted state from storage."""
        import os
        os.makedirs(self.storage_dir, exist_ok=True)
        
        products_file = f"{self.storage_dir}/products.json"
        transactions_file = f"{self.storage_dir}/transactions.json"
        licenses_file = f"{self.storage_dir}/licenses.json"
        subscriptions_file = f"{self.storage_dir}/subscriptions.json"
        revenue_shares_file = f"{self.storage_dir}/revenue_shares.json"
        payment_methods_file = f"{self.storage_dir}/payment_methods.json"
        balances_file = f"{self.storage_dir}/balances.json"
        
        if os.path.exists(products_file):
            try:
                with open(products_file, 'r') as f:
                    data = json.load(f)
                    self.products = {p["id"]: Product(**p) for p in data}
            except Exception as e:
                logger.warning(f"Failed to load products: {e}")
        
        if os.path.exists(transactions_file):
            try:
                with open(transactions_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = {t["id"]: Transaction(**t) for t in data}
            except Exception as e:
                logger.warning(f"Failed to load transactions: {e}")
        
        if os.path.exists(licenses_file):
            try:
                with open(licenses_file, 'r') as f:
                    data = json.load(f)
                    self.licenses = {l["id"]: License(**l) for l in data}
            except Exception as e:
                logger.warning(f"Failed to load licenses: {e}")
        
        if os.path.exists(subscriptions_file):
            try:
                with open(subscriptions_file, 'r') as f:
                    data = json.load(f)
                    self.subscriptions = {s["id"]: Subscription(**s) for s in data}
            except Exception as e:
                logger.warning(f"Failed to load subscriptions: {e}")
        
        if os.path.exists(revenue_shares_file):
            try:
                with open(revenue_shares_file, 'r') as f:
                    data = json.load(f)
                    self.revenue_shares = {r["id"]: RevenueShare(**r) for r in data}
            except Exception as e:
                logger.warning(f"Failed to load revenue shares: {e}")
        
        if os.path.exists(payment_methods_file):
            try:
                with open(payment_methods_file, 'r') as f:
                    data = json.load(f)
                    self.payment_methods = {pm["id"]: PaymentMethod(**pm) for p in data for pm in p}
            except Exception as e:
                logger.warning(f"Failed to load payment methods: {e}")
        
        if os.path.exists(balances_file):
            try:
                with open(balances_file, 'r') as f:
                    self.creator_balances = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load balances: {e}")
    
    def _save_state(self):
        """Persist state to storage."""
        with self.lock:
            products_file = f"{self.storage_dir}/products.json"
            transactions_file = f"{self.storage_dir}/transactions.json"
            licenses_file = f"{self.storage_dir}/licenses.json"
            subscriptions_file = f"{self.storage_dir}/subscriptions.json"
            revenue_shares_file = f"{self.storage_dir}/revenue_shares.json"
            payment_methods_file = f"{self.storage_dir}/payment_methods.json"
            balances_file = f"{self.storage_dir}/balances.json"
            
            with open(products_file, 'w') as f:
                json.dump([p.to_dict() for p in self.products.values()], f, indent=2)
            
            with open(transactions_file, 'w') as f:
                json.dump([t.to_dict() for t in self.transactions.values()], f, indent=2)
            
            with open(licenses_file, 'w') as f:
                json.dump([l.to_dict() for l in self.licenses.values()], f, indent=2)
            
            with open(subscriptions_file, 'w') as f:
                json.dump([s.to_dict() for s in self.subscriptions.values()], f, indent=2)
            
            with open(revenue_shares_file, 'w') as f:
                json.dump([r.to_dict() for r in self.revenue_shares.values()], f, indent=2)
            
            with open(payment_methods_file, 'w') as f:
                json.dump([pm.to_dict() for pm in self.payment_methods.values()], f, indent=2)
            
            with open(balances_file, 'w') as f:
                json.dump(self.creator_balances, f, indent=2)
    
    # Product management
    def create_product(self, project_id: str, seller_id: str, title: str,
                       description: str = "", price: float = 0.0,
                       currency: str = "USD", license_type: str = "personal",
                       features: List[str] = None) -> Product:
        """
        Create a new product for marketplace.
        
        Args:
            project_id: Associated project
            seller_id: Creator selling the product
            title: Product title
            description: Product description
            price: Product price
            currency: Currency code
            license_type: Type of license
            features: List of included features
            
        Returns:
            Created Product object
        """
        with self.lock:
            product = Product(
                id=f"prod-{uuid.uuid4().hex[:12]}",
                project_id=project_id,
                seller_id=seller_id,
                title=title,
                description=description,
                price=price,
                currency=currency,
                license_type=license_type,
                features=features or []
            )
            
            self.products[product.id] = product
            self._save_state()
            
            logger.info(f"Product created: {product.id}")
            return product
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID."""
        return self.products.get(product_id)
    
    def update_product(self, product_id: str, **updates) -> Optional[Product]:
        """Update a product."""
        with self.lock:
            if product_id not in self.products:
                return None
            
            product = self.products[product_id]
            
            for field, value in updates.items():
                if hasattr(product, field) and field not in ["id", "project_id", "seller_id"]:
                    setattr(product, field, value)
            
            product.updated_at = datetime.utcnow()
            self._save_state()
            
            return product
    
    def list_products(self, seller_id: str = None, active_only: bool = True) -> List[Product]:
        """List products with optional filters."""
        products = list(self.products.values())
        
        if seller_id:
            products = [p for p in products if p.seller_id == seller_id]
        if active_only:
            products = [p for p in products if p.is_active]
        
        return products
    
    # Transaction processing
    def create_transaction(self, buyer_id: str, seller_id: str, product_id: str,
                          amount: float, currency: str = "USD",
                          payment_method: str = "") -> Transaction:
        """
        Create a new transaction.
        
        Args:
            buyer_id: Purchasing user
            seller_id: Creator receiving payment
            product_id: Product being purchased
            amount: Transaction amount
            currency: Currency code
            payment_method: Payment method used
            
        Returns:
            Created Transaction object
        """
        with self.lock:
            product = self.products.get(product_id)
            if not product:
                raise ValueError(f"Product not found: {product_id}")
            
            # Calculate fees
            platform_fee = self._calculate_platform_fee(amount)
            net_amount = amount - platform_fee
            
            transaction = Transaction(
                id=f"txn-{uuid.uuid4().hex[:12]}",
                buyer_id=buyer_id,
                seller_id=seller_id,
                product_id=product_id,
                amount=amount,
                platform_fee=platform_fee,
                net_amount=net_amount,
                currency=currency,
                payment_method=payment_method,
                status=TransactionStatus.PENDING.value
            )
            
            self.transactions[transaction.id] = transaction
            self._save_state()
            
            logger.info(f"Transaction created: {transaction.id}")
            return transaction
    
    def _calculate_platform_fee(self, amount: float) -> float:
        """Calculate platform fee for a transaction."""
        percentage_fee = amount * (self.fee_config.standard_fee_percent / 100)
        fixed_fee = self.fee_config.transaction_fee_fixed
        return round(percentage_fee + fixed_fee, 2)
    
    def complete_transaction(self, transaction_id: str, stripe_payment_id: str = None) -> Optional[Transaction]:
        """
        Mark a transaction as completed and issue license.
        
        Args:
            transaction_id: Transaction to complete
            stripe_payment_id: Stripe payment intent ID
            
        Returns:
            Updated Transaction object
        """
        with self.lock:
            if transaction_id not in self.transactions:
                return None
            
            transaction = self.transactions[transaction_id]
            transaction.status = TransactionStatus.COMPLETED.value
            transaction.completed_at = datetime.utcnow()
            transaction.stripe_payment_id = stripe_payment_id
            
            # Update creator balance
            self.creator_balances[transaction.seller_id] = (
                self.creator_balances.get(transaction.seller_id, 0) + transaction.net_amount
            )
            
            # Create revenue share record
            revenue_share = RevenueShare(
                id=f"rs-{uuid.uuid4().hex[:12]}",
                transaction_id=transaction_id,
                creator_id=transaction.seller_id,
                gross_amount=transaction.amount,
                platform_fee=transaction.platform_fee,
                net_amount=transaction.net_amount,
                currency=transaction.currency
            )
            self.revenue_shares[revenue_share.id] = revenue_share
            
            # Auto-issue license for the product
            product = self.products.get(transaction.product_id)
            if product:
                self.issue_license(
                    user_id=transaction.buyer_id,
                    product_id=transaction.product_id,
                    license_type=product.license_type
                )
            
            self._save_state()
            
            logger.info(f"Transaction completed: {transaction_id}")
            return transaction
    
    def refund_transaction(self, transaction_id: str, reason: str = "") -> Optional[Transaction]:
        """
        Process a refund for a transaction.
        
        Args:
            transaction_id: Transaction to refund
            reason: Refund reason
            
        Returns:
            Updated Transaction object
        """
        with self.lock:
            if transaction_id not in self.transactions:
                return None
            
            transaction = self.transactions[transaction_id]
            
            if transaction.status != TransactionStatus.COMPLETED.value:
                raise ValueError("Can only refund completed transactions")
            
            transaction.status = TransactionStatus.REFUNDED.value
            transaction.metadata["refund_reason"] = reason
            
            # Revoke license
            self.revoke_user_license(transaction.buyer_id, transaction.product_id)
            
            # Reverse creator balance (simplified)
            self.creator_balances[transaction.seller_id] = max(
                0, self.creator_balances.get(transaction.seller_id, 0) - transaction.net_amount
            )
            
            self._save_state()
            
            logger.info(f"Transaction refunded: {transaction_id}")
            return transaction
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a transaction by ID."""
        return self.transactions.get(transaction_id)
    
    def list_transactions(self, user_id: str = None, 
                         status: str = None) -> List[Transaction]:
        """List transactions with optional filters."""
        transactions = list(self.transactions.values())
        
        if user_id:
            transactions = [t for t in transactions if t.buyer_id == user_id or t.seller_id == user_id]
        
        if status:
            transactions = [t for t in transactions if t.status == status]
        
        # Sort by creation date descending
        transactions.sort(key=lambda t: t.created_at, reverse=True)
        
        return transactions
    
    # License management
    def issue_license(self, user_id: str, product_id: str,
                     license_type: str = "personal",
                     expires_at: datetime = None,
                     max_uses: int = None,
                     restrictions: Dict[str, Any] = None) -> License:
        """
        Issue a license to a user.
        
        Args:
            user_id: User to license
            product_id: Product to license
            license_type: Type of license
            expires_at: Expiration datetime
            max_uses: Maximum usage count
            restrictions: Usage restrictions
            
        Returns:
            Created License object
        """
        with self.lock:
            product = self.products.get(product_id)
            if not product:
                raise ValueError(f"Product not found: {product_id}")
            
            # Check for existing license
            existing = None
            for license in self.licenses.values():
                if license.user_id == user_id and license.product_id == product_id:
                    if license.is_valid():
                        existing = license
                        break
            
            if existing:
                # Extend or update existing license
                if expires_at and not existing.expires_at:
                    existing.expires_at = expires_at
                if max_uses:
                    existing.max_uses = max_uses
                if restrictions:
                    existing.restrictions.update(restrictions)
                existing.updated_at = datetime.utcnow()
                return existing
            
            license = License(
                id=f"lic-{uuid.uuid4().hex[:12]}",
                user_id=user_id,
                product_id=product_id,
                license_type=license_type,
                expires_at=expires_at,
                max_uses=max_uses,
                restrictions=restrictions or {},
                scope=license_type
            )
            
            self.licenses[license.id] = license
            self._save_state()
            
            logger.info(f"License issued: {license.id}")
            return license
    
    def validate_license(self, user_id: str, product_id: str,
                        context: Dict[str, Any] = None) -> Tuple[bool, str, Optional[License]]:
        """
        Validate a user's license for a product.
        
        Args:
            user_id: User to validate
            product_id: Product to check
            context: Usage context
            
        Returns:
            Tuple of (is_valid, reason, license)
        """
        for license in self.licenses.values():
            if license.user_id == user_id and license.product_id == product_id:
                if not license.is_active:
                    return False, "License is inactive", None
                
                if license.expires_at and datetime.utcnow() > license.expires_at:
                    return False, "License has expired", None
                
                can_use, reason = license.can_use(context)
                if not can_use:
                    return False, reason, None
                
                return True, "License is valid", license
        
        return False, "No license found", None
    
    def revoke_user_license(self, user_id: str, product_id: str) -> bool:
        """
        Revoke a user's license for a product.
        
        Args:
            user_id: User whose license to revoke
            product_id: Product to revoke access for
            
        Returns:
            True if revoked, False if not found
        """
        with self.lock:
            for license in self.licenses.values():
                if license.user_id == user_id and license.product_id == product_id:
                    license.is_active = False
                    self._save_state()
                    logger.info(f"License revoked: {license.id}")
                    return True
            return False
    
    def get_user_licenses(self, user_id: str) -> List[License]:
        """Get all licenses for a user."""
        return [l for l in self.licenses.values() if l.user_id == user_id and l.is_active]
    
    # Subscription management
    def create_subscription(self, user_id: str, tier: str) -> Subscription:
        """
        Create a new subscription.
        
        Args:
            user_id: User subscribing
            tier: Subscription tier
            
        Returns:
            Created Subscription object
        """
        with self.lock:
            subscription = Subscription(
                id=f"sub-{uuid.uuid4().hex[:12]}",
                user_id=user_id,
                tier=tier,
                status=SubscriptionStatus.ACTIVE.value
            )
            
            self.subscriptions[subscription.id] = subscription
            self._save_state()
            
            logger.info(f"Subscription created: {subscription.id}")
            return subscription
    
    def cancel_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Subscription to cancel
            
        Returns:
            Updated Subscription object
        """
        with self.lock:
            if subscription_id not in self.subscriptions:
                return None
            
            subscription = self.subscriptions[subscription_id]
            subscription.cancel_at_period_end = True
            subscription.updated_at = datetime.utcnow()
            
            self._save_state()
            
            logger.info(f"Subscription cancellation scheduled: {subscription_id}")
            return subscription
    
    def get_user_subscription(self, user_id: str) -> Optional[Subscription]:
        """Get active subscription for a user."""
        for subscription in self.subscriptions.values():
            if subscription.user_id == user_id and subscription.is_active():
                return subscription
        return None
    
    def check_subscription_access(self, user_id: str, required_tier: str) -> bool:
        """
        Check if user has required subscription tier.
        
        Args:
            user_id: User to check
            required_tier: Required tier level
            
        Returns:
            True if user has access
        """
        tier_order = [SubscriptionTier.FREE.value, SubscriptionTier.CREATOR.value,
                     SubscriptionTier.PROFESSIONAL.value, SubscriptionTier.ENTERPRISE.value]
        
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return required_tier == SubscriptionTier.FREE.value
        
        user_tier_index = tier_order.index(subscription.tier)
        required_tier_index = tier_order.index(required_tier)
        
        return user_tier_index >= required_tier_index
    
    # Creator revenue management
    def get_creator_balance(self, creator_id: str) -> float:
        """Get creator's available balance."""
        return self.creator_balances.get(creator_id, 0.0)
    
    def get_creator_earnings(self, creator_id: str, 
                            start_date: datetime = None,
                            end_date: datetime = None) -> Dict[str, Any]:
        """
        Get creator's earnings report.
        
        Args:
            creator_id: Creator to check
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Earnings report dictionary
        """
        start_date = start_date or datetime.utcnow() - timedelta(days=30)
        end_date = end_date or datetime.utcnow()
        
        total_earnings = 0.0
        total_fees = 0.0
        transaction_count = 0
        product_sales: Dict[str, int] = {}
        
        for share in self.revenue_shares.values():
            if share.creator_id != creator_id:
                continue
            
            if not (start_date <= share.created_at <= end_date):
                continue
            
            total_earnings += share.gross_amount
            total_fees += share.platform_fee
            transaction_count += 1
            
            # Track by product
            transaction = self.transactions.get(share.transaction_id)
            if transaction:
                product_sales[transaction.product_id] = product_sales.get(transaction.product_id, 0) + 1
        
        return {
            "totalEarnings": total_earnings,
            "totalFees": total_fees,
            "netEarnings": total_earnings - total_fees,
            "transactionCount": transaction_count,
            "productSales": product_sales,
            "periodStart": start_date.isoformat(),
            "periodEnd": end_date.isoformat()
        }
    
    def request_payout(self, creator_id: str, amount: float) -> Dict[str, Any]:
        """
        Request a payout from creator balance.
        
        Args:
            creator_id: Creator requesting payout
            amount: Amount to withdraw
            
        Returns:
            Payout request result
        """
        with self.lock:
            balance = self.creator_balances.get(creator_id, 0.0)
            
            if amount > balance:
                return {
                    "success": False,
                    "message": f"Insufficient balance. Available: ${balance:.2f}"
                }
            
            # In a real implementation, this would create a Stripe payout
            self.creator_balances[creator_id] -= amount
            
            self._save_state()
            
            logger.info(f"Payout requested: ${amount:.2f} for creator {creator_id}")
            
            return {
                "success": True,
                "message": "Payout request submitted",
                "amount": amount,
                "remainingBalance": self.creator_balances[creator_id]
            }
    
    # Payment method management
    def add_payment_method(self, user_id: str, payment_method_data: Dict[str, Any]) -> PaymentMethod:
        """
        Add a payment method for a user.
        
        Args:
            user_id: User adding payment method
            payment_method_data: Payment method details
            
        Returns:
            Created PaymentMethod object
        """
        with self.lock:
            payment_method = PaymentMethod(
                id=f"pm-{uuid.uuid4().hex[:12]}",
                user_id=user_id,
                type=payment_method_data.get("type", "card"),
                last_four=payment_method_data.get("last_four", "****"),
                brand=payment_method_data.get("brand"),
                expiry_month=payment_method_data.get("expiry_month"),
                expiry_year=payment_method_data.get("expiry_year"),
                stripe_payment_method_id=payment_method_data.get("stripe_payment_method_id"),
                is_default=False
            )
            
            self.payment_methods[payment_method.id] = payment_method
            self._save_state()
            
            logger.info(f"Payment method added: {payment_method.id}")
            return payment_method
    
    def get_user_payment_methods(self, user_id: str) -> List[PaymentMethod]:
        """Get all payment methods for a user."""
        return [pm for pm in self.payment_methods.values() if pm.user_id == user_id]
    
    def set_default_payment_method(self, user_id: str, payment_method_id: str) -> bool:
        """Set a payment method as default."""
        with self.lock:
            for pm in self.payment_methods.values():
                if pm.user_id == user_id:
                    pm.is_default = (pm.id == payment_method_id)
            
            self._save_state()
            return True
    
    # Analytics
    def get_platform_analytics(self, start_date: datetime = None,
                               end_date: datetime = None) -> Dict[str, Any]:
        """
        Get platform-wide analytics.
        
        Args:
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Analytics report
        """
        start_date = start_date or datetime.utcnow() - timedelta(days=30)
        end_date = end_date or datetime.utcnow()
        
        total_revenue = 0.0
        total_fees = 0.0
        transaction_count = 0
        completed_transactions = 0
        refunded_amount = 0.0
        
        active_products = len([p for p in self.products.values() if p.is_active])
        active_subscriptions = len([s for s in self.subscriptions.values() if s.is_active()])
        
        for transaction in self.transactions.values():
            if not (start_date <= transaction.created_at <= end_date):
                continue
            
            total_revenue += transaction.amount
            total_fees += transaction.platform_fee
            transaction_count += 1
            
            if transaction.status == TransactionStatus.COMPLETED.value:
                completed_transactions += 1
            elif transaction.status == TransactionStatus.REFUNDED.value:
                refunded_amount += transaction.amount
        
        return {
            "totalRevenue": total_revenue,
            "totalFees": total_fees,
            "netRevenue": total_revenue - total_fees,
            "transactionCount": transaction_count,
            "completedTransactions": completed_transactions,
            "refundedAmount": refunded_amount,
            "activeProducts": active_products,
            "activeSubscriptions": active_subscriptions,
            "periodStart": start_date.isoformat(),
            "periodEnd": end_date.isoformat()
        }


# Global service instance
_licensing_service: Optional[LicensingService] = None
_licensing_lock = threading.Lock()


def create_licensing_service(storage_dir: str = None) -> LicensingService:
    """
    Create and return the global licensing service.
    
    Args:
        storage_dir: Optional storage directory
        
    Returns:
        LicensingService instance
    """
    global _licensing_service
    
    with _licensing_lock:
        if _licensing_service is None:
            _licensing_service = LicensingService(storage_dir)
        return _licensing_service


__all__ = [
    "LicenseType",
    "TransactionStatus",
    "SubscriptionStatus",
    "SubscriptionTier",
    "PlatformFeeConfig",
    "Product",
    "Transaction",
    "License",
    "Subscription",
    "RevenueShare",
    "PaymentMethod",
    "LicensingService",
    "create_licensing_service"
]
