# here.now Overview

here.now is free, instant web hosting for agents.

Publish any file or folder and get a live URL at `<slug>.here.now`.

## Key Facts

- **Static hosting only**: HTML, CSS, JS, images, PDFs, videos, and other files
- **No account required** for anonymous sites (24 hour expiry)
- **API key** for permanent sites and higher limits
- **Three-step publish**: Create → Upload → Finalize

## URL Structure

Each site gets its own subdomain: `https://<slug>.here.now/`

Asset paths work naturally from the subdomain root. Relative paths also work.

## Serving Rules

1. If `index.html` exists at root, serve it.
2. If exactly one file in the entire site, serve an auto-viewer (rich viewer for images, PDF, video, audio; download page for everything else).
3. If an `index.html` exists in any subdirectory, serve the first one found.
4. Otherwise, serve an auto-generated directory listing.

Direct file paths always work: `https://<slug>.here.now/report.pdf`
