# Terraform - AWS Infrastructure

## Overview
This directory contains Terraform configurations for deploying VisualVerse infrastructure on Amazon Web Services (AWS).

## License
**PROPRIETARY** - This infrastructure is part of VisualVerse's enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Directory Structure

```
terraform/aws/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── provider.tf          # Provider configuration
├── network.tf           # VPC and networking
├── compute.tf           # EC2, ECS, Lambda
├── storage.tf           # S3, EFS
├── database.tf          # RDS, ElastiCache
├── security.tf          # IAM, Security Groups
├── s3.tf                # S3 buckets
├── cloudfront.tf        # CDN configuration
├── route53.tf           # DNS configuration
└── README.md            # This file
```

## Resources Created

### Network
- **VPC**: 10.0.0.0/16 with public/private subnets
- **Subnets**: 3 public, 3 private across AZs
- **NAT Gateways**: One per public subnet
- **Internet Gateway**: For public access
- **Route Tables**: Private and public routing

### Compute
- **ECS Cluster**: For containerized services
- **EC2 Instances**: Bastion host for administration
- **Auto Scaling Groups**: For worker nodes
- **Lambda Functions**: For serverless workloads

### Database
- **RDS PostgreSQL**: Primary database
- **ElastiCache Redis**: Caching and queue
- **DocumentDB**: Content metadata storage

### Storage
- **S3 Buckets**: Static assets, exports, backups
- **CloudFront CDN**: Global content delivery
- **EFS**: Shared file storage

### Security
- **IAM Roles**: Service and task roles
- **Security Groups**: Network isolation
- **KMS Keys**: Encryption at rest
- **Secrets Manager**: Sensitive configuration

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform >= 1.5.0 installed
3. Remote state backend (S3 + DynamoDB)

## Usage

### Initialize
```bash
cd infrastructure/terraform/aws
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
| environment | string | - | Environment name |
| region | string | ap-south-1 | AWS region |
| vpc_cidr | string | 10.0.0.0/16 | VPC CIDR block |
| instance_type | string | t3.medium | EC2 instance type |
| db_instance_class | string | db.t3.medium | RDS instance class |
| enable_monitoring | bool | true | Enable CloudWatch |

## Outputs

| Output | Description |
|--------|-------------|
| vpc_id | VPC identifier |
| endpoint_urls | Service endpoints |
| bucket_names | S3 bucket names |
| arns | Resource ARNs |

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
