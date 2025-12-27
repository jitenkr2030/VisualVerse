"""
Institutional Analytics Service module.

This module provides comprehensive analytics, reporting, cohort analysis,
and data export capabilities for institutional decision-making.
"""

from .analytics_service import (
    AnalyticsService,
    InstitutionalMetrics,
    UsageReport,
    PerformanceMetrics,
    CohortAnalysis,
    DataExport,
    DashboardWidget,
    AdminDashboard,
    MetricCategory,
    ReportType,
    TimeGranularity,
    create_analytics_service
)

__all__ = [
    "AnalyticsService",
    "InstitutionalMetrics",
    "UsageReport",
    "PerformanceMetrics",
    "CohortAnalysis",
    "DataExport",
    "DashboardWidget",
    "AdminDashboard",
    "MetricCategory",
    "ReportType",
    "TimeGranularity",
    "create_analytics_service"
]
