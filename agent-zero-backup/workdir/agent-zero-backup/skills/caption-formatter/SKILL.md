---
name: "caption-formatter"
description: "Generate timed, readable caption and subtitle blocks for video content. Creates SRT-compatible formats with proper line breaks and timing."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["video", "captions", "subtitles", "accessibility", "srt", "formatting"]
trigger_patterns:
  - "captions"
  - "subtitles"
  - "srt"
  - "caption format"
  - "subtitle file"
  - "timed text"
---

# Caption and Subtitle Formatter

## When to Use
Activate when asked to create, format, or fix captions, subtitles, SRT files, or timed text for video content.

## The Process

### Step 1: Receive Input
- **Transcript text** (with or without timestamps)
- **Video duration** (to calculate timing)
- **Style preference:** Standard, Creative, Minimal
- **Language:** Source and target (if translating)

### Step 2: Segment the Text
Rules for good captions:
- **Max 32 characters per line**
- **Max 2 lines per caption block**
- **Max 5-7 seconds per caption**
- **Break at natural pauses** (commas, periods, phrase boundaries)
- **Don't break mid-word or mid-phrase**

### Step 3: Generate SRT Format

```srt
1
00:00:00,000 --> 00:00:03,500
[First caption line]
[Second line if needed]

2
00:00:03,500 --> 00:00:07,000
[Next caption]

3
00:00:07,000 --> 00:00:10,500
[Next caption]
```

### Step 4: Apply Style
- **Standard:** Clean, verbatim
- **Creative:** Add emphasis (*italic* for thoughts, **bold** for key terms)
- **Minimal:** Only key phrases, remove filler words

### Step 5: Quality Check
- Read-through makes sense without audio
- No caption exceeds 2 lines or 7 seconds
- Timing doesn't overlap
- Speaker changes are noted

## Output Formats
Return in requested format (default SRT):
- **SRT:** Standard subtitle format
- **VTT:** Web video text tracks
- **Plain text:** With timestamps inline

## Constraints
- Maintain accuracy — don't alter meaning
- Remove filler words only in Minimal style
- Include [MUSIC], [LAUGHTER], [SFX] tags where applicable
- Reading speed should not exceed 20 characters per second

