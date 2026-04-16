# Sentient Landing Page Deployment

**Created:** 2026-04-15
**Status:** LIVE (anonymous — claim within 24h!)

## URLs

| Resource | URL |
|----------|-----|
| **Live Site** | https://united-lasso-r2rt.here.now/ |
| **Claim URL** | https://here.now/claim?slug=united-lasso-r2rt&token=c5cdfb3388fad6f9443b0bc6ac64c839f42a0cf4324d4357783e6222015c1810 |

## Claim Token
```
c5cdfb3388fad6f9443b0bc6ac64c839f42a0cf4324d4357783e6222015c1810
```

⚠️ **VISIT THE CLAIM URL TO MAKE THE SITE PERMANENT** — anonymous sites expire in 24h!

## Local Files

| File | Path |
|------|------|
| Landing Page HTML | `/a0/usr/workdir/sentient-landing/index.html` (78.7KB) |
| Deployment Info | `/a0/usr/workdir/sentient-landing/deployment-info.txt` |
| Product Blueprint | `/a0/usr/workdir/sentient-product-system-blueprint.md` (2,883 lines) |

## Features
- 8 scroll-snapping sections with animations
- Animated emotional waveform canvas (hero)
- Confetti particle burst on waitlist signup
- Deterministic queue position from email hash
- Social sharing (Twitter/LinkedIn/Copy)
- Responsive design (mobile-friendly)
- `prefers-reduced-motion` support

## Waitlist System
- Client-side email capture with localStorage persistence
- Extensible: set `sentient_api_endpoint` in localStorage to POST to any backend
- Queue position derived from email hash (100-4100 range)
- Duplicate detection and error handling

## Design
- Fonts: Clash Display + Satoshi (Fontshare)
- Palette: Deep space blacks + coral/amber gradient + rose + blue/purple accents
- Noise texture overlay, radial gradient atmospheres
- 3D tilt on feature cards

## Next Steps
1. **Claim the site** (visit claim URL above)
2. **Connect waitlist backend** (Google Sheets, Formspree, or custom API)
3. **Set up here.now proxy route** to forward `/api/waitlist` to backend
4. **Custom domain** (sentient.ai or similar)
