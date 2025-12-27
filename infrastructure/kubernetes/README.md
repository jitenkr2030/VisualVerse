# Kubernetes Configuration

## Overview
This directory contains Kubernetes manifests and Helm charts for deploying VisualVerse to Kubernetes clusters.

## License
**PROPRIETARY** - This infrastructure is part of VisualVerse's enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Directory Structure

```
kubernetes/
├── base/
│   ├── namespace.yaml
│   ├── deployment-admin.yaml
│   ├── deployment-creator.yaml
│   ├── deployment-engine.yaml
│   ├── deployment-worker.yaml
│   ├── service-admin.yaml
│   ├── service-creator.yaml
│   ├── service-engine.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
├── overlays/
│   ├── development/
│   ├── staging/
│   └── production/
└── helm/
    └── visualverse-chart/
        ├── Chart.yaml
        ├── values.yaml
        ├── templates/
        │   ├── _helpers.tpl
        │   ├── deployment.yaml
        │   ├── service.yaml
        │   ├── ingress.yaml
        │   ├── hpa.yaml
        │   └── pvc.yaml
        └── values/
            ├── dev.yaml
            ├── staging.yaml
            └── prod.yaml
```

## Deployments

### Admin Console
- Replicas: 2 (dev), 3 (staging), 5 (production)
- Resources: 512Mi RAM, 500m CPU
- Rolling update strategy

### Creator Portal
- Replicas: 2 (dev), 3 (staging), 5 (production)
- Resources: 1Gi RAM, 1000m CPU
- Rolling update strategy

### Animation Engine
- Replicas: 1 (dev), 2 (staging), 4 (production)
- Resources: 2Gi RAM, 2000m CPU
- GPU support available

### Worker
- Replicas: 1 (dev), 2 (staging), 4 (production)
- Resources: 1Gi RAM, 500m CPU
- HPA enabled

## Services

| Service | Port | Protocol | Type |
|---------|------|----------|------|
| admin | 3000 | TCP | ClusterIP |
| creator | 3001 | TCP | ClusterIP |
| engine | 8080 | TCP | ClusterIP |
| worker | - | - | - |

## Ingress Configuration

- TLS termination at ingress
- Path-based routing
- Rate limiting configured
- DDoS protection enabled

## Helm Usage

### Install
```bash
helm install visualverse ./helm/visualverse-chart -f values/prod.yaml
```

### Upgrade
```bash
helm upgrade visualverse ./helm/visualverse-chart -f values/prod.yaml
```

### Uninstall
```bash
helm uninstall visualverse
```

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
