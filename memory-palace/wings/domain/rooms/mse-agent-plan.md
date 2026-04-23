# MSE Intelligence Agent — Research & Implementation Plan

**Created**: 2026-04-20
**Status**: Research Phase Complete, Ready for Implementation

## Tolu's MSE Education Profile

| Field | Value |
|-------|-------|
| Email | tas8ka@virginia.edu |
| Degree | BS Materials Science & Engineering |
| University | University of Virginia |
| Key Professor | Leonid Zhigilei (lz2n@virginia.edu) |
| Courses Confirmed | MSE 3050 (Thermodynamics & Phase Equilibria), MSE 6020 (Graduate Seminar) |
| ABET Contact | Claire Culver (coc6qq@virginia.edu) |
| MRS Status | Active subscriber — Materials 360, JMR, MRS Bulletin |
| Book Owned | De Graef & McHenry — Structure of Materials (Crystallography) |

## UVA MSE Curriculum

### Core Courses
- MSE 2090 — Introduction to Materials Science
- MSE 2101 — Investigations: Properties (Lab)
- MSE 3050 — Thermodynamics and Phase Equilibria (emails found)
- MSE 3060 — Structures and Defects of Materials
- MSE 3070 — Kinetics and Phase Transformation
- MSE 3101 — Materials Science Investigations (Lab)
- MSE 3670 — Electronic, Magnetic, and Optical Materials
- MSE 4320 — Origins of Mechanical Behavior
- MSE 4592 — Capstone Thesis (year-long)
- MSE 6020 — Graduate Course (emails found)

### Electives
- MSE 2200 — Additive Manufacturing & 3D Printing
- MSE 3080 — Corrosion, Batteries, and Fuel Cells
- MSE 4030 — X-Ray Scattering
- MSE 4055 — Nanoscale Science & Technology
- MSE 4220 — Polymer Physics
- MSE 4270 — Atomistic Simulations

## Takeout Intelligence Data

| Metric | Count |
|--------|-------|
| Total documents | 188,419 |
| MSE-classified docs | 53,669 |
| High-signal MSE content | 95 unique docs |
| UVA MSE course emails | 848 |
| MSE course content chunks | 30+ |
| MRS newsletter items | 50+ |

## Textbook & Reference Library

### Free Full PDFs Available
1. Bergeron & Risbud — Introduction to Phase Equilibria in Ceramics
2. Porter, Easterling & Sherif — Phase Transformations in Metals and Alloys (3rd ed)
3. Reed-Hill & Abbaschian — Physical Metallurgy Principles (4th ed)
4. Hull & Bacon — Introduction to Dislocations (5th ed)
5. Ashby — Materials Selection in Mechanical Design
6. Stevens — Polymer Chemistry: An Introduction
7. Fontana & Greene — Corrosion Engineering
8. Williams & Carter — Transmission Electron Microscopy

### Commercial (Owned or Need Access)
1. Callister & Rethwisch — MSE: An Introduction (10th ed) — Archive.org has 7th ed free
2. De Graef & McHenry — Structure of Materials (2nd ed) — Tolu owns this
3. Courtney — Mechanical Behavior of Materials
4. Hummel — Electronic Properties of Materials

## Open Educational Resources

### Courses
- MIT 3.091 — Solid-State Chemistry (36 video lectures)
- MIT 3.012 — Fundamentals of MSE
- MIT 3.020 — Thermodynamics of Materials
- NPTEL MSE courses (IIT system)

### YouTube
- Taylor Sparks (Univ. of Utah MSE)
- MaterialsProject workshops
- Real Engineering

### Databases (Free)
- MatWeb (185K+ materials)
- Materials Project (DFT-computed properties, free API)
- AFLOW (3.5M+ compounds)
- OQMD, JARVIS (NIST), NOMAD
- matminer Python library

---

## MSE Agent Architecture

### Phase 1: Knowledge Base Construction
1. Download free PDF textbooks → vectorize into RAG corpus
2. Extract UVA MSE course emails from takeout DB → structured notes
3. Scrape MIT OCW MSE course materials
4. Build phase diagram database (ASM-style)
5. Index Materials Project API data for property lookups

### Phase 2: Agent Profile
```
/a0/usr/agents/mse-engineer/
├── agent.yaml
├── prompts/
│   ├── agent.system.main.role.md
│   └── agent.system.tool.mse_tool.md
├── tools/
│   ├── mse_query.py
│   ├── phase_diagram.py
│   ├── property_lookup.py
│   └── unit_converter.py
└── extensions/
    └── system_prompt/
        └── _10_mse_context.py
```

### Phase 3: Integration Points
- A2A endpoint for calling from main agent
- Scheduled tasks: weekly MRS digest, daily MSE news
- Takeout-intelligence: continuous MSE content pipeline
- Materials Project API: real-time property queries
- Memory palace: auto-save learnings to wings/domain/rooms/

### Phase 4: Advanced Features
- Phase diagram interpreter
- Crystal structure visualizer
- Materials selection optimizer (Ashby method)
- Literature review generator
- Homework/problem solver with step-by-step explanations

---

## Implementation Priority

1. Immediate: Create MSE agent profile with RAG over textbooks
2. Week 1: Build knowledge base from free PDFs + UVA course emails
3. Week 2: Add Materials Project API integration
4. Week 3: Phase diagram + property lookup tools
5. Ongoing: Feed takeout-intelligence MSE content into agent knowledge
