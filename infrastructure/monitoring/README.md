# Monitoring Configuration

## Overview
This directory contains monitoring and observability configurations for VisualVerse, including Prometheus metrics, Grafana dashboards, and alerting rules.

## License
**PROPRIETARY** - This infrastructure is part of VisualVerse's enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Directory Structure

```
monitoring/
├── prometheus/
│   ├── prometheus.yml
│   ├── alerts.yml
│   └── recording-rules.yml
├── grafana/
│   ├── dashboards/
│   │   ├── overview.json
│   │   ├── services.json
│   │   ├── performance.json
│   │   └── business-metrics.json
│   ├── datasources/
│   │   └── prometheus.yml
│   └── alerting/
│       └── notification-channels.yml
├── alerting/
│   ├── alertmanager.yml
│   └── templates/
└── docs/
    ├── metrics-guide.md
    └── alerting-guide.md
```

## Prometheus Configuration

### Metrics Collected

#### Application Metrics
- `http_requests_total`: HTTP request count
- `http_request_duration_seconds`: Request latency
- `http_request_size_bytes`: Request size
- `visualverse_animations_total`: Animation count
- `visualverse_renders_total`: Render count

#### System Metrics
- `process_cpu_seconds_total`: CPU usage
- `process_memory_bytes`: Memory usage
- `process_open_fds`: Open file descriptors
- `go_goroutines`: Go routines (if applicable)

#### Business Metrics
- `visualverse_users_total`: Total users
- `visualverse_active_users`: Active users
- `visualverse_content_created`: Content created
- `visualverse_revenue`: Revenue metrics

## Grafana Dashboards

### Overview Dashboard
- System health at a glance
- Service status indicators
- Key metrics summary
- Recent alerts

### Services Dashboard
- Per-service metrics
- Error rates
- Latency percentiles
- Throughput

### Performance Dashboard
- Animation render times
- Export performance
- Resource utilization
- Bottleneck identification

### Business Dashboard
- User growth
- Content metrics
- Revenue tracking
- Conversion rates

## Alerting Rules

### Critical Alerts
- **ServiceDown**: Service unavailable > 2 minutes
- **HighErrorRate**: Error rate > 5%
- **DiskFull**: Disk usage > 90%

### Warning Alerts
- **HighLatency**: P95 latency > 1s
- **MemoryPressure**: Memory usage > 80%
- **CPUHigh**: CPU usage > 85%

## Alertmanager Configuration

Notification channels:
- Slack (#visualverse-alerts)
- PagerDuty
- Email (ops@visualverse.in)
- Webhook (custom integrations)

## Usage

### Start Prometheus
```bash
prometheus --config.file=prometheus.yml
```

### Import Dashboards
```bash
curl -X POST http://localhost:3001/api/dashboards/import \
  -H "Content-Type: application/json" \
  -d @grafana/dashboards/overview.json
```

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
