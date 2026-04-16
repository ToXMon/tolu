---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
version: "1.0.0"
author: adapted from zarazhangrui/frontend-slides for Agent Zero
tags: ["presentation", "slides", "html", "powerpoint", "pptx", "design"]
trigger_patterns:
  - "create presentation"
  - "build slides"
  - "make a deck"
  - "convert pptx"
  - "convert powerpoint"
  - "html presentation"
  - "slide deck"
  - "pitch deck"
---

# Frontend Slides

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:

- **Typography:** Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- **Color & Theme:** Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- **Motion:** Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions.
- **Backgrounds:** Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:

- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read the viewport-base.css file and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type    | Maximum Content                                           |
| ------------- | --------------------------------------------------------- |
| Title slide   | 1 heading + 1 subtitle + optional tagline                 |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid  | 1 heading + 6 cards maximum (2x3 or 3x2)                  |
| Code slide    | 1 heading + 8-10 lines of code                            |
| Quote slide   | 1 quote (max 3 lines) + attribution                       |
| Image slide   | 1 heading + 1 image (max 60vh height)                     |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**

### Mode C: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to new slide or reduce other content first. Never add images without checking if existing content already fills the viewport.

---

## Phase 1: Content Discovery (New Presentations)

**Ask ALL questions in a single response** so the user can answer everything at once:

> **Purpose:** What is this presentation for? (Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation)
>
> **Length:** Approximately how many slides? (Short 5-10 / Medium 10-20 / Long 20+)
>
> **Content:** Do you have content ready? (All content ready / Rough notes / Topic only)
>
> **Inline Editing:** Do you need to edit text directly in the browser after generation?
> - "Yes (Recommended)" — Can edit text in-browser, auto-save to localStorage, export file
> - "No" — Presentation only, keeps file smaller

**Remember the user's editing choice — it determines whether edit-related code is included in Phase 3.**

If user has content, ask them to share it.

### Step 1.2: Image Evaluation (if images provided)

If user selected "No images" → skip to Phase 2.

If user provides an image folder:

1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.) using `code_execution_tool` with `ls`
2. **View each image** — Use `vision_load` to inspect each image
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. Design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm with user** via `response`: Present the outline and ask "Does this slide outline and image selection look right?" (Looks good / Adjust images / Adjust outline)

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Phase 2 — the user sees their brand styled three different ways.

---

## Phase 2: Style Discovery

**This is the "show, don't tell" phase.** Most people can't articulate design preferences in words.

### Step 2.0: Style Path

Ask the user how they want to choose:

- "Show me options" (recommended) — Generate 3 previews based on mood
- "I know what I want" — Pick from preset list directly

**If direct selection:** Show preset picker (read `§§include(/a0/skills/frontend-slides/docs/STYLE_PRESETS.md)` for available presets) and skip to Phase 3.

### Step 2.1: Mood Selection (Guided Discovery)

Ask the user (can select up to 2):

> What feeling should the audience have?
>
> - **Impressed/Confident** — Professional, trustworthy
> - **Excited/Energized** — Innovative, bold
> - **Calm/Focused** — Clear, thoughtful
> - **Inspired/Moved** — Emotional, memorable

### Step 2.2: Generate 3 Style Previews

Based on mood, generate 3 distinct single-slide HTML previews showing typography, colors, animation, and overall aesthetic. Read the style presets doc for available presets and their specifications using `text_editor:read` on `/a0/skills/frontend-slides/docs/STYLE_PRESETS.md`.

| Mood                | Suggested Presets                                  |
| ------------------- | -------------------------------------------------- |
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical       |
| Excited/Energized   | Creative Voltage, Neon Cyber, Split Pastel         |
| Calm/Focused        | Notebook Tabs, Paper & Ink, Swiss Modern           |
| Inspired/Moved      | Dark Botanical, Vintage Editorial, Pastel Geometry |

Save previews to `/a0/usr/workdir/.slide-previews/` (style-a.html, style-b.html, style-c.html). Each should be self-contained, ~50-100 lines, showing one animated title slide. Use `text_editor:write` to create each file.

### Step 2.3: User Picks

Ask the user which style preview they prefer (Style A / Style B / Style C / Mix elements). If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

**Before generating, read these supporting files using `text_editor:read`:**

- `/a0/skills/frontend-slides/docs/html-template.md` — HTML architecture and JS features
- `/a0/skills/frontend-slides/docs/viewport-base.css` — Mandatory CSS (include in full)
- `/a0/skills/frontend-slides/docs/animation-patterns.md` — Animation reference for the chosen feeling

**Key requirements:**

- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `<style>` block
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block
- Save the final presentation using `text_editor:write` to `/a0/usr/workdir/` (or user's preferred location)

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python3 /a0/skills/frontend-slides/scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Style selection** — Proceed to Phase 2 for style discovery
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

---

## Phase 5: Delivery

1. **Clean up** — Delete `.slide-previews/` if it exists
2. **Report** — Tell the user:
   - **File location**, style name, slide count
   - **Navigation:** Arrow keys, Space, scroll/swipe, click nav dots
   - **How to customize:** `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - If inline editing was enabled: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save

---

## Phase 6: Share & Export (Optional)

After delivery, **ask the user:** _"Would you like to share this presentation? I can deploy it to a live URL (works on any device including phones) or export it as a PDF."_

Options:

- **Deploy to URL** — Shareable link that works on any device
- **Export to PDF** — Universal file for email, Slack, print
- **Both**
- **No thanks**

If the user declines, stop here. If they choose one or both, proceed below.

### 6A: Deploy to a Live URL (Vercel)

This deploys the presentation to Vercel — a free hosting platform. The link works on any device (phones, tablets, laptops) and stays live until the user takes it down.

**If the user has never deployed before, guide them step by step:**

1. **Check if Vercel CLI is installed** — Run `npx vercel --version`. If not found, install Node.js first.

2. **Check if user is logged in** — Run `npx vercel whoami`.
   - If NOT logged in, explain: _"Vercel is a free hosting service. You need an account to deploy. Let me walk you through it:"_
     - Step 1: Ask user to go to https://vercel.com/signup in their browser
     - Step 2: They can sign up with GitHub, Google, email — whatever is easiest
     - Step 3: Once signed up, run `vercel login` and follow the prompts
     - Step 4: Confirm login with `vercel whoami`
   - Wait for the user to confirm they're logged in before proceeding.

3. **Deploy** — Run the deploy script:

   ```bash
   bash /a0/skills/frontend-slides/scripts/deploy.sh <path-to-presentation>
   ```

   The script accepts either a folder (with index.html) or a single HTML file.

4. **Share the URL** — Tell the user the live URL from the script output.

**Deployment gotchas:**

- Local images/videos must travel with the HTML. The deploy script auto-detects files referenced via `src="..."` in the HTML and bundles them.
- Prefer folder deployments when the presentation has many assets.
- Filenames with spaces can cause issues. Rename to use hyphens if images break.
- Redeploying updates the same URL.

### 6B: Export to PDF

This captures each slide as a screenshot and combines them into a PDF. Perfect for email attachments, embedding in documents, or printing.

**Note:** Animations and interactivity are not preserved — the PDF is a static snapshot.

1. **Run the export script:**

   ```bash
   bash /a0/skills/frontend-slides/scripts/export-pdf.sh <path-to-html> [output.pdf]
   ```

   If no output path is given, the PDF is saved next to the HTML file.

2. **What happens behind the scenes** (explain briefly to the user):
   - A headless browser opens the presentation at 1920×1080
   - It screenshots each slide one by one
   - All screenshots are combined into a single PDF
   - Playwright installs automatically if missing

3. **If PDF exceeds 10MB**, offer to re-run with `--compact` flag for 50-70% smaller file:
   ```bash
   bash /a0/skills/frontend-slides/scripts/export-pdf.sh <path-to-html> [output.pdf] --compact
   ```

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| `/a0/skills/frontend-slides/docs/STYLE_PRESETS.md` | 12 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| `/a0/skills/frontend-slides/docs/viewport-base.css` | Mandatory responsive CSS — copy into every presentation | Phase 3 (generation) |
| `/a0/skills/frontend-slides/docs/html-template.md` | HTML structure, JS features, code quality standards | Phase 3 (generation) |
| `/a0/skills/frontend-slides/docs/animation-patterns.md` | CSS/JS animation snippets and effect-to-feeling guide | Phase 3 (generation) |
| `/a0/skills/frontend-slides/scripts/extract-pptx.py` | Python script for PPT content extraction | Phase 4 (conversion) |
| `/a0/skills/frontend-slides/scripts/deploy.sh` | Deploy slides to Vercel for instant sharing | Phase 6 (sharing) |
| `/a0/skills/frontend-slides/scripts/export-pdf.sh` | Export slides to PDF | Phase 6 (export) |

## Agent Zero Tool Usage

When executing this skill, use these Agent Zero tools:

| Task | Tool |
|------|------|
| Read supporting files | `text_editor:read` |
| Write HTML files | `text_editor:write` |
| Run scripts (extract, deploy, export) | `code_execution_tool` with `runtime: terminal` |
| View user-provided images | `vision_load` |
| Ask questions, present options | `response` |
| Browse web for inspiration | `browser_agent` |
| Search for design references | `search_engine` |
