# Sentient GitHub Repository

**Created:** 2026-04-15
**Repo:** https://github.com/ToXMon/sentient
**GHCR Image:** `ghcr.io/toxmon/sentient-api:latest`
**License:** MIT

## Structure

```
sentient/
├── api/                    # FastAPI backend
│   ├── app/                #   main, models, schemas, database, routers, utils
│   ├── .herenow/           #   proxy.json for here.now routes
│   ├── Dockerfile          #   Multi-stage Alpine, non-root
│   ├── deploy.yaml         #   Akash Network SDL
│   └── requirements.txt
├── landing/                # Static landing page
│   └── index.html
├── docs/
│   ├── blueprint.md        # Product system blueprint
│   └── architecture.md     # Architecture deep-dive
├── .github/workflows/
│   └── ci.yml              # Lint (ruff) + build Docker + push to GHCR
├── .gitignore
├── LICENSE
├── README.md               # 266 lines, deslop-compliant
└── docker-compose.yml      # Local dev setup
```

## CI/CD
- On push to main (paths: api/**): ruff lint + Docker build + push to GHCR
- On PR to main: lint only
- GHCR: ghcr.io/toxmon/sentient-api:latest and :{sha}

## Local Dev
```bash
git clone https://github.com/ToXMon/sentient.git && cd sentient
docker compose up --build
# API: http://localhost:8000 | Landing: http://localhost:3000
```

## Related
- Landing page live: https://united-lasso-r2rt.here.now/
- Claim URL: https://here.now/claim?slug=united-lasso-r2rt&token=c5cdfb3388fad6f9443b0bc6ac64c839f42a0cf4324d4357783e6222015c1810
- Product blueprint: /a0/usr/workdir/sentient-product-system-blueprint.md
