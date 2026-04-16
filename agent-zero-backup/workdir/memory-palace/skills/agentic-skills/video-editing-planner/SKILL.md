---
name: "video-editing-planner"
description: "Create scene cuts, transition plans, pacing guides, and editing timelines for video production. Generates shot lists and post-production workflows."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["video", "editing", "production", "post-production", "planning"]
trigger_patterns:
  - "editing plan"
  - "video edit"
  - "shot list"
  - "scene plan"
  - "pacing guide"
  - "cut plan"
---

# Video Editing Planner

## When to Use
Activate when asked to plan video editing, create shot lists, design pacing, or structure post-production workflow.

## The Process

### Step 1: Analyze the Footage
- What raw footage is available?
- What's the total runtime of raw clips?
- What's the target final runtime?
- What's the narrative arc?

### Step 2: Create the Edit Plan

```markdown
## Edit Plan: [Video Title]

### Overview
- **Target Runtime:** [X:XX]
- **Style:** [Fast-paced/Cinematic/Vlog/Tutorial]
- **Aspect Ratio:** [16:9 / 9:16 / 1:1]

### Shot List
| # | Clip | Timestamp | Duration | Type | Notes |
|---|------|-----------|----------|------|-------| |
| 1 | [Name] | 00:00-00:15 | 15s | A-Roll | [Description] |
| 2 | [Name] | 00:15-00:20 | 5s | B-Roll | [Cutaway] |
| 3 | [Name] | ... | ... | ... | ... |

### Transitions
| From | To | Type | Reason |
|------|----|------|--------| |
| Shot 1 | Shot 2 | Hard cut | [Reason] |
| Shot 3 | Shot 4 | J-cut | [Reason] |

### Pacing Guide
- [0:00-0:30] Fast cuts, high energy (intro hook)
- [0:30-3:00] Medium pace, steady delivery
- [3:00-5:00] Slow down for key point
- [5:00-6:00] Build energy toward conclusion

### Audio Plan
- **Music:** [Style/mood, when to swell/drop]
- **Sound Effects:** [Where needed]
- **Audio Levels:** Dialogue on top, music -6dB under voice

### Color and Effects
- **Grade:** [Warm/Cool/Natural/Moody]
- **Text Overlays:** [Where and what text]
- **Zoom Effects:** [Where to add emphasis]
```

## Constraints
- Compression ratio: aim for 3:1 raw to final
- Every cut should serve the story
- Audio transitions should be smooth (crossfade music changes)
- Include B-roll for every A-roll segment longer than 10 seconds

