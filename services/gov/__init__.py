"""
VisualVerse Governance & Administration Platform.

A comprehensive governance system for institutional management,
content moderation, analytics, and regulatory compliance.

This package provides the following services:
- Identity & Access Management (identity_service)
- Content Moderation (moderation_service)
- Institutional Analytics (analytics_service)
- Compliance & Audit (compliance_service)
- Admin Console (admin_service)
"""

from typing import Dict, Any

__version__ = "1.0.0"
__author__ = "MiniMax Agent"


def get_governance_version() -> str:
    """Get the governance platform version."""
    return __version__


def initialize_gov_platform(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Initialize all governance platform services.
    
    This function creates and configures all services required for the
    Governance & Administration platform, providing a unified entry point
    for service initialization.
    
    Args:
        config: Optional configuration dictionary for customizing service behavior.
               Supported keys:
               - enable_audit: Enable comprehensive audit logging (default: True)
               - audit_retention_days: Retention period for audit logs (default: 365)
               - moderation_auto_approve_threshold: Quality score threshold for auto-approval (default: 85)
               - privacy_regulation: Default privacy regulation (default: GDPR)
               - session_timeout_minutes: Session timeout in minutes (default: 60)
               - mfa_required: Require MFA for admin accounts (default: False)
               - content_approval_required: Require moderation approval (default: True)
               - allow_self_registration: Allow user self-registration (default: True)
               - api_rate_limit: API rate limit per minute (default: 100)
               - default_storage_limit_mb: Default storage limit in MB (default: 10240)
    
    Returns:
        Dictionary containing all initialized services:
        - identity: IdentityService instance for user and access management
        - moderation: ModerationService instance for content moderation
        - analytics: AnalyticsService instance for institutional analytics
        - compliance: ComplianceService instance for compliance and auditing
        - admin: AdminService instance for administrative operations
    
    Example:
        >>> services = initialize_gov_platform({"enable_audit": True})
        >>> identity_service = services["identity"]
        >>> moderation_service = services["moderation"]
    """
    from .services.identity import create_identity_service
    from .services.moderation import create_moderation_service
    from .services.analytics import create_analytics_service
    from .services.compliance import create_compliance_service
    from .services.admin import create_admin_service
    
    # Apply configuration if provided
    moderation_config = config.get("moderation", {}) if config else {}
    compliance_config = config.get("compliance", {}) if config else {}
    admin_config = config.get("admin", {}) if config else {}
    
    # Initialize services
    services = {
        "identity": create_identity_service(),
        "moderation": create_moderation_service(),
        "analytics": create_analytics_service(),
        "compliance": create_compliance_service(),
        "admin": create_admin_service()
    }
    
    return services


# For backwards compatibility
initialize_governance = initialize_gov_platform


__all__ = [
    "__version__",
    "__author__",
    "get_governance_version",
    "initialize_gov_platform",
    "initialize_governance"
]
