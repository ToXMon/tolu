---
name: "devops-assistant"
description: "Provide commit guidance, deployment steps, CI/CD configuration, and workflow optimization for DevOps practices. Covers git workflows, Docker, and infrastructure."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["devops", "deployment", "ci-cd", "git", "docker", "infrastructure"]
trigger_patterns:
  - "devops"
  - "deploy"
  - "deployment"
  - "ci cd"
  - "pipeline"
  - "docker"
  - "commit strategy"
  - "release"
---

# DevOps Assistant

## When to Use
Activate when asked about deployment, CI/CD pipelines, git workflows, Docker, release management, or infrastructure automation.

## The Process

### Git and Commits

#### Commit Strategy
- **Conventional Commits:** type(scope): description
  - feat(auth): add OAuth2 login
  - fix(api): handle null response
  - docs(readme): update setup guide
  - refactor(db): optimize query layer
- **Commit often, push when tests pass**
- **Never commit secrets** — use environment variables

#### Branch Strategy
- main — production-ready code only
- develop — integration branch
- feature/* — new features
- hotfix/* — urgent fixes
- release/* — release preparation

### CI/CD Pipeline

```markdown
## Pipeline: [Name]

### Stage 1: Build
- Install dependencies
- Compile/build artifacts
- Run linting

### Stage 2: Test
- Unit tests
- Integration tests
- Security scan
- Code coverage check (minimum: 80%)

### Stage 3: Package
- Build Docker image
- Tag with version + commit hash
- Push to registry

### Stage 4: Deploy
- Deploy to staging
- Run smoke tests
- Deploy to production (manual approval)

### Stage 5: Verify
- Health checks
- Monitor error rates
- Rollback if error rate > threshold
```

### Docker Best Practices
- Use multi-stage builds for smaller images
- Pin base image versions (no latest tag in production)
- Run as non-root user
- Use .dockerignore
- One process per container

### Deployment Checklist
- [ ] All tests passing
- [ ] Database migrations ready
- [ ] Environment variables configured
- [ ] Secrets rotated if needed
- [ ] Rollback plan documented
- [ ] Monitoring/alerts configured
- [ ] Stakeholders notified

## Constraints
- Never deploy on Fridays (or before weekends)
- Always test in staging before production
- Automate everything that's done more than twice
- Document runbooks for manual processes

