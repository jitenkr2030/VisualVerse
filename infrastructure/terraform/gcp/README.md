# Terraform - GCP Infrastructure

## Overview
This directory contains Terraform configurations for deploying VisualVerse infrastructure on Google Cloud Platform (GCP).

## License
**PROPRIETARY** - This infrastructure is part of VisualVerse's enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Directory Structure

```
terraform/gcp/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── provider.tf          # Provider configuration
├── network.tf           # VPC and networking
├── compute.tf           # GKE, Compute Engine
├── storage.tf           # Cloud Storage
├── database.tf          # Cloud SQL, Firestore
├── security.tf          # IAM, Service Accounts
├── cloudrun.tf          # Cloud Run services
├── cloudbuild.tf        # Cloud Build triggers
└── README.md            # This file
```

## Resources Created

### Network
- **VPC Network**: Custom mode VPC
- **Subnets**: Regional subnets with secondary ranges
- **Cloud NAT**: For private instance egress
- **Cloud DNS**: Managed DNS zones
- **Firewall Rules**: Security group equivalent

### Compute
- **GKE Cluster**: For container orchestration
- **Cloud Run**: Serverless container services
- **Compute Engine**: Bastion and management VMs
- **Instance Groups**: Managed instance groups

### Database
- **Cloud SQL PostgreSQL**: Primary database
- **Cloud Memorystore**: Redis caching
- **Firestore**: Document database

### Storage
- **Cloud Storage Buckets**: Static assets, media
- **Cloud CDN**: Global content delivery

### Security
- **Service Accounts**: Least privilege access
- **IAM Roles**: Predefined and custom roles
- **Secret Manager**: Sensitive data storage
- **Workload Identity**: GKE service account access

## Prerequisites

1. Google Cloud SDK installed and configured
2. Terraform >= 1.5.0 installed
3. Billing account linked
4. Required APIs enabled

## Usage

### Initialize
```bash
cd infrastructure/terraform/gcp
terraform init
```

### Plan
```bash
terraform plan -var-file=prod.tfvars
```

### Apply
```bash
terraform apply -var-file=prod.tfvars
```

### Destroy
```bash
terraform destroy -var-file=prod.tfvars
```

## Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| project_id | string | - | GCP project ID |
| region | string | asia-south1 | GCP region |
| zone | string | asia-south1-a | GCP zone |
| vpc_cidr | string | 10.0.0.0/16 | VPC CIDR block |
| machine_type | string | e2-medium | GCE machine type |
| db_tier | string | db-custom-2-8192 | Cloud SQL tier |

## Outputs

| Output | Description |
|--------|-------------|
| network_name | VPC network name |
| cluster_name | GKE cluster name |
| bucket_urls | Cloud Storage URLs |
| service_accounts | Service account emails |

## Cloud Run Services

| Service | Region | Min | Max | Memory |
|---------|--------|-----|-----|--------|
| admin | asia-south1 | 1 | 10 | 512Mi |
| creator | asia-south1 | 1 | 10 | 1Gi |
| api | asia-south1 | 2 | 20 | 1Gi |

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
