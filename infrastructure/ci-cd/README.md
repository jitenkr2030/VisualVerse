# Infrastructure - CI/CD Pipeline Configuration

## Overview
This directory contains CI/CD pipeline configurations for automated testing, building, and deployment of VisualVerse components.

## License
**PROPRIETARY** - This infrastructure is part of VisualVerse's enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Directory Structure

```
ci-cd/
├── .github/
│   └── workflows/
│       ├── pr-checks.yml
│       ├── build.yml
│       ├── test.yml
│       ├── deploy-staging.yml
│       └── deploy-production.yml
├── scripts/
│   ├── validate-license.sh
│   ├── run-tests.sh
│   ├── build.sh
│   └── deploy.sh
└── configs/
    ├── conventional-commits.json
    └── codeowners
```

## GitHub Actions Workflows

### PR Checks (pr-checks.yml)
Runs on every pull request:
- Linting (ESLint, Prettier)
- Type checking (TypeScript)
- License header validation
- Security scanning (npm audit)

### Build (build.yml)
Triggered on merge to main:
- Builds all packages in the monorepo
- Runs integration tests
- Generates build artifacts
- Publishes to package registry

### Test (test.yml)
Comprehensive test suite:
- Unit tests (Jest)
- Integration tests (Supertest)
- E2E tests (Playwright)
- Performance benchmarks

### Deploy Staging (deploy-staging.yml)
Deploys to staging environment:
- Builds Docker images
- Updates Kubernetes manifests
- Deploys to staging cluster
- Runs smoke tests

### Deploy Production (deploy-production.yml)
Production deployment:
- Requires manual approval
- Blue/green deployment strategy
- Health check verification
- Rollback capability

## Scripts

### validate-license.sh
Validates license headers in all source files:
```bash
./scripts/validate-license.sh --strict
```

### run-tests.sh
Runs the test suite:
```bash
./scripts/run-tests.sh --coverage --ci
```

### build.sh
Builds all packages:
```bash
./scripts/build.sh --production --parallel
```

### deploy.sh
Deployment automation:
```bash
./scripts/deploy.sh --environment=production --strategy=rolling
```

## Pipeline Features

- **Caching**: Dependency caching for faster builds
- **Parallel Jobs**: Independent jobs run concurrently
- **Matrix Builds**: Multiple configurations tested
- **Artifact Management**: Build artifacts stored and versioned
- **Notifications**: Slack/Discord integration for status
- **Security**: Secret scanning and dependency updates

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
