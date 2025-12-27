# Infrastructure - Docker Configuration

## Overview
This directory contains Docker configuration files for containerizing VisualVerse services and applications.

## License
**PROPRIETARY** - This infrastructure is part of VisualVerse's enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Directory Structure

```
docker/
├── Dockerfiles/
│   ├── Dockerfile.admin
│   ├── Dockerfile.creator
│   ├── Dockerfile.engine
│   └── Dockerfile.worker
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
└── .dockerignore
```

## Docker Images

### Admin Console (Dockerfile.admin)
- Base image: node:20-alpine
- Purpose: Administrative dashboard container
- Port: 3000
- Environment variables configured

### Creator Portal (Dockerfile.creator)
- Base image: node:20-alpine
- Purpose: Content creator application
- Port: 3001
- Includes build tooling

### Animation Engine (Dockerfile.engine)
- Base image: node:20-alpine
- Purpose: Rendering engine service
- Port: 8080
- Optimized for performance

### Worker (Dockerfile.worker)
- Base image: python:3.11-slim
- Purpose: Background job processing
- Queue: Redis-based
- Auto-scaling capable

## Usage

### Development
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Individual Service
```bash
docker build -f Dockerfiles/Dockerfile.admin -t visualverse/admin .
docker run -p 3000:3000 visualverse/admin
```

## Environment Variables

Configure services via environment:

```env
NODE_ENV=production
API_URL=https://api.visualverse.in
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## Volumes

- **uploads**: User-uploaded media files
- **exports**: Generated animation exports
- **logs**: Application logs
- **cache**: Build caches

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
