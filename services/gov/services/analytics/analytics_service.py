"""
Institutional Analytics Service for Governance Platform.

Provides comprehensive analytics, reporting, cohort analysis,
and data export capabilities for institutional decision-making.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from uuid import uuid4
from collections import defaultdict
import json


class MetricCategory(Enum):
    """Categories of analytics metrics."""
    USAGE = "usage"
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    CONTENT = "content"
    USER = "user"
    REVENUE = "revenue"


class ReportType(Enum):
    """Types of analytics reports."""
    USAGE_SUMMARY = "usage_summary"
    CONTENT_EFFECTIVENESS = "content_effectiveness"
    USER_ENGAGEMENT = "user_engagement"
    LEARNING_OUTCOMES = "learning_outcomes"
    COHORT_ANALYSIS = "cohort_analysis"
    COMPLIANCE = "compliance"
    CUSTOM = "custom"


class TimeGranularity(Enum):
    """Time granularity for data aggregation."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class InstitutionalMetrics:
    """Core institutional metrics."""
    tenant_id: str
    period_start: datetime
    period_end: datetime
    
    # User metrics
    total_users: int = 0
    active_users: int = 0
    new_users: int = 0
    churned_users: int = 0
    
    # Usage metrics
    total_sessions: int = 0
    total_time_spent: int = 0  # seconds
    average_session_duration: float = 0.0
    daily_active_users: Dict[str, int] = field(default_factory=dict)
    
    # Content metrics
    total_content_items: int = 0
    content_views: int = 0
    content_completions: int = 0
    average_completion_rate: float = 0.0
    
    # Engagement metrics
    average_engagement_score: float = 0.0
    interaction_rate: float = 0.0
    return_visit_rate: float = 0.0
    
    # Performance metrics
    average_assessment_score: float = 0.0
    skill_mastery_rate: float = 0.0
    certification_rate: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "user_metrics": {
                "total_users": self.total_users,
                "active_users": self.active_users,
                "new_users": self.new_users,
                "churned_users": self.churned_users
            },
            "usage_metrics": {
                "total_sessions": self.total_sessions,
                "total_time_hours": round(self.total_time_spent / 3600, 2),
                "average_session_minutes": round(self.average_session_duration / 60, 2),
                "daily_active_users": self.daily_active_users
            },
            "content_metrics": {
                "total_items": self.total_content_items,
                "content_views": self.content_views,
                "content_completions": self.content_completions,
                "completion_rate": f"{self.average_completion_rate:.1f}%"
            },
            "engagement_metrics": {
                "average_engagement_score": round(self.average_engagement_score, 2),
                "interaction_rate": f"{self.interaction_rate:.1f}%",
                "return_visit_rate": f"{self.return_visit_rate:.1f}%"
            },
            "performance_metrics": {
                "average_assessment_score": f"{self.average_assessment_score:.1f}%",
                "skill_mastery_rate": f"{self.skill_mastery_rate:.1f}%",
                "certification_rate": f"{self.certification_rate:.1f}%"
            }
        }


@dataclass
class UsageReport:
    """Usage analytics report."""
    report_id: str
    tenant_id: str
    report_type: ReportType
    time_range: Tuple[datetime, datetime]
    granularity: TimeGranularity
    
    # Data
    data_points: List[Dict[str, Any]] = field(default_factory=list)
    summary_stats: Dict[str, Any] = field(default_factory=dict)
    
    # Generated
    generated_at: datetime = field(default_factory=datetime.now)
    generated_by: Optional[str] = None
    filters_applied: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "tenant_id": self.tenant_id,
            "report_type": self.report_type.value,
            "time_range": {
                "start": self.time_range[0].isoformat(),
                "end": self.time_range[1].isoformat()
            },
            "granularity": self.granularity.value,
            "data_points": self.data_points,
            "summary_stats": self.summary_stats,
            "generated_at": self.generated_at.isoformat(),
            "generated_by": self.generated_by,
            "filters_applied": self.filters_applied
        }


@dataclass
class PerformanceMetrics:
    """Content and learner performance metrics."""
    content_id: Optional[str]
    tenant_id: str
    period_start: datetime
    period_end: datetime
    
    # Content metrics
    views: int = 0
    unique_viewers: int = 0
    completions: int = 0
    completion_rate: float = 0.0
    average_time_spent: float = 0.0
    average_score: float = 0.0
    rating: float = 0.0
    
    # Engagement
    engagement_score: float = 0.0
    drop_off_rate: float = 0.0
    retry_rate: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "tenant_id": self.tenant_id,
            "period": {
                "start": self.period_start.isoformat(),
                "end": self.period_end.isoformat()
            },
            "views": self.views,
            "unique_viewers": self.unique_viewers,
            "completions": self.completions,
            "completion_rate": f"{self.completion_rate:.1f}%",
            "average_time_minutes": round(self.average_time_spent / 60, 2),
            "average_score": f"{self.average_score:.1f}%",
            "rating": round(self.rating, 2),
            "engagement_score": round(self.engagement_score, 2),
            "drop_off_rate": f"{self.drop_off_rate:.1f}%",
            "retry_rate": f"{self.retry_rate:.1f}%"
        }


@dataclass
class CohortAnalysis:
    """Cohort analysis data."""
    cohort_id: str
    tenant_id: str
    cohort_definition: Dict[str, Any]  # e.g., {"join_date": "2024-01", "department": "engineering"}
    users: List[str] = field(default_factory=list)
    
    # Retention data
    retention_by_week: Dict[int, float] = field(default_factory=dict)  # week -> retention %
    engagement_by_week: Dict[int, float] = field(default_factory=dict)
    completion_by_week: Dict[int, float] = field(default_factory=dict)
    
    # Progress metrics
    average_progress: float = 0.0
    average_score: float = 0.0
    time_to_completion: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cohort_id": self.cohort_id,
            "tenant_id": self.tenant_id,
            "cohort_definition": self.cohort_definition,
            "user_count": len(self.users),
            "retention": self.retention_by_week,
            "engagement": self.engagement_by_week,
            "completion": self.completion_by_week,
            "average_progress": f"{self.average_progress:.1f}%",
            "average_score": f"{self.average_score:.1f}%",
            "time_to_completion_hours": self.time_to_completion
        }


@dataclass
class DataExport:
    """Data export job."""
    export_id: str
    tenant_id: str
    export_type: str
    format: str  # csv, json, xlsx
    filters: Dict[str, Any] = field(default_factory=dict)
    fields: List[str] = field(default_factory=list)
    
    status: str = "pending"  # pending, processing, completed, failed
    progress: float = 0.0
    
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    record_count: int = 0
    
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "export_id": self.export_id,
            "tenant_id": self.tenant_id,
            "export_type": self.export_type,
            "format": self.format,
            "status": self.status,
            "progress": f"{self.progress:.1f}%",
            "record_count": self.record_count,
            "file_size_bytes": self.file_size,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error_message
        }


@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""
    widget_id: str
    title: str
    widget_type: str  # metric, chart, table, list
    data_source: str
    config: Dict[str, Any] = field(default_factory=dict)
    position: Dict[str, int] = field(default_factory=lambda: {"x": 0, "y": 0, "width": 1, "height": 1})
    refresh_interval: int = 300  # seconds


@dataclass
class AdminDashboard:
    """Admin dashboard configuration."""
    dashboard_id: str
    tenant_id: Optional[str]
    name: str
    description: str
    widgets: List[DashboardWidget] = field(default_factory=list)
    is_default: bool = False
    created_by: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dashboard_id": self.dashboard_id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "widget_count": len(self.widgets),
            "is_default": self.is_default,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat()
        }


class AnalyticsService:
    """
    Institutional analytics service for the governance platform.
    
    Provides comprehensive analytics capabilities including usage tracking,
    performance metrics, cohort analysis, and data export for institutional
    decision-making and platform optimization.
    """
    
    def __init__(self):
        # Data stores
        self.metrics_history: List[InstitutionalMetrics] = []
        self.reports: Dict[str, UsageReport] = {}
        self.performance_data: Dict[str, List[PerformanceMetrics]] = defaultdict(list)
        self.cohorts: Dict[str, CohortAnalysis] = {}
        self.exports: Dict[str, DataExport] = {}
        self.dashboards: Dict[str, AdminDashboard] = {}
        
        # Raw data storage (simulated)
        self.raw_events: List[Dict[str, Any]] = []
        self.aggregations: Dict[str, Dict[str, Any]] = {}
        
        # Initialize default dashboard
        self._init_default_dashboard()
    
    def _init_default_dashboard(self):
        """Initialize default admin dashboard."""
        dashboard = AdminDashboard(
            dashboard_id="default_dashboard",
            tenant_id=None,
            name="Default Admin Dashboard",
            description="Default dashboard for platform administrators",
            is_default=True,
            widgets=[
                DashboardWidget(
                    widget_id="w1",
                    title="Total Users",
                    widget_type="metric",
                    data_source="user_count",
                    position={"x": 0, "y": 0, "width": 1, "height": 1}
                ),
                DashboardWidget(
                    widget_id="w2",
                    title="Active Users Today",
                    widget_type="metric",
                    data_source="daily_active_users",
                    position={"x": 1, "y": 0, "width": 1, "height": 1}
                ),
                DashboardWidget(
                    widget_id="w3",
                    title="Content Completion Rate",
                    widget_type="metric",
                    data_source="completion_rate",
                    position={"x": 2, "y": 0, "width": 1, "height": 1}
                ),
                DashboardWidget(
                    widget_id="w4",
                    title="User Activity",
                    widget_type="chart",
                    data_source="activity_trend",
                    config={"chart_type": "line", "days": 30},
                    position={"x": 0, "y": 1, "width": 2, "height": 2}
                ),
                DashboardWidget(
                    widget_id="w5",
                    title="Top Content",
                    widget_type="table",
                    data_source="top_content",
                    config={"limit": 10},
                    position={"x": 2, "y": 1, "width": 1, "height": 2}
                )
            ]
        )
        
        self.dashboards[dashboard.dashboard_id] = dashboard
    
    # Metrics Management
    def record_metrics(
        self,
        tenant_id: str,
        metrics: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ):
        """Record new metrics data point."""
        # In production, this would aggregate from raw events
        self.raw_events.append({
            "tenant_id": tenant_id,
            "timestamp": (timestamp or datetime.now()).isoformat(),
            "data": metrics
        })
    
    def calculate_institutional_metrics(
        self,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> InstitutionalMetrics:
        """Calculate comprehensive metrics for a period."""
        # Filter events for the period
        events = [
            e for e in self.raw_events
            if e["tenant_id"] == tenant_id and
            datetime.fromisoformat(e["timestamp"]) >= start_date and
            datetime.fromisoformat(e["timestamp"]) <= end_date
        ]
        
        # Calculate metrics (simplified)
        metrics = InstitutionalMetrics(
            tenant_id=tenant_id,
            period_start=start_date,
            period_end=end_date
        )
        
        # Aggregate user metrics
        user_ids = set()
        active_dates = defaultdict(set)
        
        for event in events:
            data = event.get("data", {})
            
            if "user_id" in data:
                user_ids.add(data["user_id"])
                if "date" in data:
                    active_dates[data["date"]].add(data["user_id"])
            
            # Aggregate usage
            metrics.total_sessions += data.get("sessions", 0)
            metrics.total_time_spent += data.get("time_spent", 0)
            metrics.content_views += data.get("views", 0)
            metrics.content_completions += data.get("completions", 0)
        
        metrics.total_users = len(user_ids)
        metrics.active_users = len(user_ids)  # Simplified
        metrics.daily_active_users = {
            date: len(users) for date, users in active_dates.items()
        }
        
        if metrics.total_sessions > 0:
            metrics.average_session_duration = metrics.total_time_spent / metrics.total_sessions
        
        if metrics.content_views > 0:
            metrics.average_completion_rate = (
                metrics.content_completions / metrics.content_views * 100
            )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_metrics_summary(
        self,
        tenant_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get summary metrics for a tenant."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = self.calculate_institutional_metrics(tenant_id, start_date, end_date)
        return metrics.to_dict()
    
    # Report Generation
    def generate_report(
        self,
        tenant_id: str,
        report_type: ReportType,
        start_date: datetime,
        end_date: datetime,
        granularity: TimeGranularity = TimeGranularity.DAILY,
        filters: Optional[Dict[str, Any]] = None,
        generated_by: Optional[str] = None
    ) -> UsageReport:
        """Generate an analytics report."""
        report_id = f"report_{uuid4().hex[:12]}"
        
        # Calculate date ranges based on granularity
        date_ranges = self._generate_date_ranges(start_date, end_date, granularity)
        
        data_points = []
        summary_stats = {
            "total_records": 0,
            "sum_values": 0,
            "avg_values": 0,
            "min_value": float('inf'),
            "max_value": float('-inf')
        }
        
        for range_start, range_end in date_ranges:
            # Calculate metrics for this range
            metrics = self.calculate_institutional_metrics(tenant_id, range_start, range_end)
            
            data_point = {
                "period_start": range_start.isoformat(),
                "period_end": range_end.isoformat(),
                "users": metrics.active_users,
                "sessions": metrics.total_sessions,
                "time_spent_hours": round(metrics.total_time_spent / 3600, 2),
                "completions": metrics.content_completions,
                "completion_rate": round(metrics.average_completion_rate, 2)
            }
            
            data_points.append(data_point)
            
            # Update summary stats
            summary_stats["total_records"] += 1
            summary_stats["sum_values"] += metrics.active_users
            if metrics.active_users < summary_stats["min_value"]:
                summary_stats["min_value"] = metrics.active_users
            if metrics.active_users > summary_stats["max_value"]:
                summary_stats["max_value"] = metrics.active_users
        
        if summary_stats["total_records"] > 0:
            summary_stats["avg_values"] = round(
                summary_stats["sum_values"] / summary_stats["total_records"], 2
            )
        
        if summary_stats["min_value"] == float('inf'):
            summary_stats["min_value"] = 0
        if summary_stats["max_value"] == float('-inf'):
            summary_stats["max_value"] = 0
        
        report = UsageReport(
            report_id=report_id,
            tenant_id=tenant_id,
            report_type=report_type,
            time_range=(start_date, end_date),
            granularity=granularity,
            data_points=data_points,
            summary_stats=summary_stats,
            generated_by=generated_by,
            filters_applied=filters or {}
        )
        
        self.reports[report_id] = report
        return report
    
    def _generate_date_ranges(
        self,
        start: datetime,
        end: datetime,
        granularity: TimeGranularity
    ) -> List[Tuple[datetime, datetime]]:
        """Generate date ranges based on granularity."""
        ranges = []
        current = start
        
        while current < end:
            if granularity == TimeGranularity.HOURLY:
                next_time = current + timedelta(hours=1)
            elif granularity == TimeGranularity.DAILY:
                next_time = current + timedelta(days=1)
            elif granularity == TimeGranularity.WEEKLY:
                next_time = current + timedelta(weeks=1)
            elif granularity == TimeGranularity.MONTHLY:
                next_time = current + timedelta(days=30)
            elif granularity == TimeGranularity.QUARTERLY:
                next_time = current + timedelta(days=90)
            else:  # YEARLY
                next_time = current + timedelta(days=365)
            
            next_time = min(next_time, end)
            ranges.append((current, next_time))
            current = next_time
        
        return ranges
    
    def get_report(self, report_id: str) -> Optional[UsageReport]:
        """Get a specific report."""
        return self.reports.get(report_id)
    
    def list_reports(
        self,
        tenant_id: Optional[str] = None,
        report_type: Optional[ReportType] = None,
        limit: int = 50
    ) -> List[UsageReport]:
        """List reports with filters."""
        reports = list(self.reports.values())
        
        if tenant_id:
            reports = [r for r in reports if r.tenant_id == tenant_id]
        if report_type:
            reports = [r for r in reports if r.report_type == report_type]
        
        reports.sort(key=lambda r: r.generated_at, reverse=True)
        return reports[:limit]
    
    # Performance Metrics
    def record_content_performance(
        self,
        content_id: str,
        tenant_id: str,
        metrics: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ):
        """Record content performance metrics."""
        perf = PerformanceMetrics(
            content_id=content_id,
            tenant_id=tenant_id,
            period_start=timestamp or datetime.now(),
            period_end=timestamp or datetime.now(),
            **metrics
        )
        
        self.performance_data[content_id].append(perf)
    
    def get_content_performance(
        self,
        content_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[PerformanceMetrics]:
        """Get performance metrics for content."""
        metrics = self.performance_data.get(content_id, [])
        
        if start_date:
            metrics = [m for m in metrics if m.period_start >= start_date]
        if end_date:
            metrics = [m for m in metrics if m.period_end <= end_date]
        
        return metrics
    
    def get_top_performing_content(
        self,
        tenant_id: str,
        metric: str = "completion_rate",
        limit: int = 10,
        days: int = 30
    ) -> List[PerformanceMetrics]:
        """Get top performing content by metric."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        all_performance = []
        for content_id, perf_list in self.performance_data.items():
            for perf in perf_list:
                if perf.tenant_id == tenant_id and perf.period_start >= start_date:
                    all_performance.append(perf)
        
        # Sort by metric
        all_performance.sort(
            key=lambda p: getattr(p, metric, 0) or 0,
            reverse=True
        )
        
        return all_performance[:limit]
    
    # Cohort Analysis
    def create_cohort(
        self,
        tenant_id: str,
        cohort_definition: Dict[str, Any],
        user_ids: List[str]
    ) -> CohortAnalysis:
        """Create a new cohort for analysis."""
        import hashlib
        definition_str = json.dumps(cohort_definition, sort_keys=True)
        cohort_id = f"cohort_{hashlib.md5(definition_str.encode()).hexdigest()[:12]}"
        
        cohort = CohortAnalysis(
            cohort_id=cohort_id,
            tenant_id=tenant_id,
            cohort_definition=cohort_definition,
            users=user_ids
        )
        
        self.cohorts[cohort_id] = cohort
        return cohort
    
    def calculate_cohort_retention(
        self,
        cohort_id: str
    ) -> Dict[int, float]:
        """Calculate retention for a cohort over weeks."""
        cohort = self.cohorts.get(cohort_id)
        if not cohort:
            return {}
        
        # Simplified retention calculation
        user_count = len(cohort.users)
        if user_count == 0:
            return {}
        
        # Simulate retention data
        retention = {}
        for week in range(1, 13):
            # Simulated: retention decreases over time
            retention_rate = max(0.1, 1.0 - (week * 0.05))
            retention[week] = round(retention_rate * 100, 1)
        
        cohort.retention_by_week = retention
        return retention
    
    def analyze_cohorts(
        self,
        tenant_id: str,
        group_by: str = "join_month"
    ) -> List[CohortAnalysis]:
        """Analyze all cohorts grouped by criteria."""
        # Simulated cohort analysis
        cohorts = []
        
        for month_offset in range(6):
            join_date = datetime.now() - timedelta(days=month_offset * 30)
            definition = {"join_month": join_date.strftime("%Y-%m")}
            
            # Simulate users
            user_count = 50 + (5 - month_offset) * 10
            user_ids = [f"user_{uuid4().hex[:8]}" for _ in range(user_count)]
            
            cohort = self.create_cohort(
                tenant_id=tenant_id,
                cohort_definition=definition,
                user_ids=user_ids
            )
            
            # Calculate metrics
            cohort.average_progress = 50 + (5 - month_offset) * 8
            cohort.average_score = 70 + (5 - month_offset) * 3
            cohort.time_to_completion = 20 + month_offset * 5
            
            self.calculate_cohort_retention(cohort.cohort_id)
            cohorts.append(cohort)
        
        return cohorts
    
    def get_cohort(self, cohort_id: str) -> Optional[CohortAnalysis]:
        """Get a specific cohort."""
        return self.cohorts.get(cohort_id)
    
    # Data Export
    def create_export(
        self,
        tenant_id: str,
        export_type: str,
        export_format: str,
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None
    ) -> DataExport:
        """Create a new data export job."""
        export = DataExport(
            export_id=f"export_{uuid4().hex[:12]}",
            tenant_id=tenant_id,
            export_type=export_type,
            format=export_format,
            filters=filters or {},
            fields=fields or []
        )
        
        self.exports[export.id] = export
        return export
    
    def start_export(self, export_id: str) -> Optional[DataExport]:
        """Start processing an export."""
        export = self.exports.get(export_id)
        if not export:
            return None
        
        export.status = "processing"
        export.started_at = datetime.now()
        
        # Simulate processing
        export.progress = 50.0
        export.record_count = 1000
        export.file_size = 50000
        
        export.status = "completed"
        export.completed_at = datetime.now()
        export.progress = 100.0
        
        return export
    
    def get_export_status(self, export_id: str) -> Optional[DataExport]:
        """Get export status."""
        return self.exports.get(export_id)
    
    def list_exports(
        self,
        tenant_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[DataExport]:
        """List exports with filters."""
        exports = list(self.exports.values())
        
        if tenant_id:
            exports = [e for e in exports if e.tenant_id == tenant_id]
        if status:
            exports = [e for e in exports if e.status == status]
        
        exports.sort(key=lambda e: e.created_at, reverse=True)
        return exports[:limit]
    
    # Dashboard Management
    def get_dashboard(
        self,
        dashboard_id: str
    ) -> Optional[AdminDashboard]:
        """Get a dashboard by ID."""
        return self.dashboards.get(dashboard_id)
    
    def get_default_dashboard(self) -> Optional[AdminDashboard]:
        """Get the default dashboard."""
        for dashboard in self.dashboards.values():
            if dashboard.is_default:
                return dashboard
        return None
    
    def list_dashboards(
        self,
        tenant_id: Optional[str] = None
    ) -> List[AdminDashboard]:
        """List dashboards."""
        dashboards = list(self.dashboards.values())
        
        if tenant_id:
            dashboards = [
                d for d in dashboards
                if d.tenant_id is None or d.tenant_id == tenant_id
            ]
        
        return dashboards
    
    def create_dashboard(
        self,
        tenant_id: Optional[str],
        name: str,
        description: str = "",
        created_by: Optional[str] = None
    ) -> AdminDashboard:
        """Create a new dashboard."""
        dashboard = AdminDashboard(
            dashboard_id=f"dash_{uuid4().hex[:12]}",
            tenant_id=tenant_id,
            name=name,
            description=description,
            created_by=created_by
        )
        
        self.dashboards[dashboard.dashboard_id] = dashboard
        return dashboard
    
    def add_widget_to_dashboard(
        self,
        dashboard_id: str,
        widget: DashboardWidget
    ) -> Optional[AdminDashboard]:
        """Add a widget to a dashboard."""
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            return None
        
        dashboard.widgets.append(widget)
        dashboard.updated_at = datetime.now()
        return dashboard
    
    # Real-time Dashboard Data
    def get_dashboard_metrics(
        self,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Get current metrics for dashboard display."""
        return {
            "user_count": 1500,
            "daily_active_users": 450,
            "weekly_active_users": 890,
            "monthly_active_users": 1200,
            "content_count": 350,
            "completion_rate": 72.5,
            "average_score": 78.3,
            "engagement_score": 85.2,
            "storage_used_gb": 45.6,
            "api_calls_today": 125000
        }
    
    def get_activity_trend(
        self,
        tenant_id: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get activity trend data for charts."""
        trend = []
        for i in range(days):
            date = datetime.now() - timedelta(days=days - i)
            trend.append({
                "date": date.strftime("%Y-%m-%d"),
                "users": 300 + (i * 5) + (hash(str(date)) % 50),
                "sessions": 500 + (i * 10) + (hash(str(date)) % 100),
                "completions": 100 + (i * 2) + (hash(str(date)) % 20)
            })
        return trend
    
    # Utility Methods
    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status."""
        return {
            "status": "healthy",
            "metrics_count": len(self.metrics_history),
            "reports_count": len(self.reports),
            "cohorts_count": len(self.cohorts),
            "exports_count": len(self.exports),
            "dashboards_count": len(self.dashboards),
            "raw_events_count": len(self.raw_events)
        }


# Service factory function
def create_analytics_service() -> AnalyticsService:
    """Create and configure a new analytics service instance."""
    return AnalyticsService()
