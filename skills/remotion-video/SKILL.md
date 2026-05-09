---
name: remotion-video
description: >
  Create, develop, and render programmatic videos using Remotion (React-based video framework).
  Use this skill when the user wants to create a video, make an animation, render MP4/GIF,
  build a React video, generate video content programmatically, create motion graphics with code,
  render still frames, or mentions Remotion, programmatic video, react video, video generation,
  video rendering, motion graphics, video automation, create-video, remotion render, video from code,
  automated video creation, batch video rendering, or generate MP4.
  Covers: project scaffolding, composition creation, animation with interpolate/spring,
  timeline with Sequence/Series, media embedding, data fetching, CLI and programmatic rendering,
  still images, and GIF output.
---

# Remotion Video Skill

Create and render programmatic videos using React components with Remotion.

## Workflow

1. **Scaffold** — Create project with `create-video`
2. **Develop** — Write compositions in React with hooks and animations
3. **Preview** — Run Studio for live preview
4. **Render** — Output MP4, GIF, or still images

---

## Phase 1: Scaffold Project

```bash
# Via code_execution_tool (terminal)
cd /path/to/parent/dir
npx create-video@latest my-video --template=blank
cd my-video
npm install
```

Templates: `blank`, `tailwind`, `three`

### Project Structure

```
my-video/
├── src/
│   ├── index.ts       # registerRoot(RemotionRoot)
│   ├── Root.tsx        # <Composition> definitions
│   └── Composition.tsx # Video component
├── public/            # Static assets (use staticFile())
├── remotion.config.ts # Optional config
└── package.json
```

### Entry Point (src/index.ts)

```tsx
import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';
registerRoot(RemotionRoot);
```

---

## Phase 2: Develop Compositions

### Root Component (src/Root.tsx)

Define each video as a `<Composition>` with id, component, dimensions, fps, and duration:

```tsx
import {Composition} from 'remotion';
import {MyVideo} from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="my-video"
        component={MyVideo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{title: 'Hello', subtitle: 'World'}}
      />
    </>
  );
};
```

### Schema Validation (Zod)

Add typed props with Zod schemas:

```tsx
import {z} from 'zod';

export const videoSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
});

// In Root.tsx, add schema prop:
// schema={videoSchema}

// Component gets typed props:
export const MyVideo: React.FC<z.infer<typeof videoSchema>> = ({title, subtitle}) => {
  // ...
};
```

---

## Phase 3: Animation & Hooks

### Core Hooks

```tsx
import {useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();           // Current frame number
const {fps, width, height, durationInFrames} = useVideoConfig();
```

### interpolate — Map frame ranges to values

```tsx
import {interpolate} from 'remotion';

const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Works with any numeric CSS property
const translateX = interpolate(frame, [0, 60], [-500, 0], {
  extrapolateRight: 'clamp',
});
```

### spring — Physics-based animation

```tsx
import {spring} from 'remotion';

const scale = spring({
  fps,
  frame: frame - 15,  // delay by 15 frames
  config: {damping: 100},
});
```

### AbsoluteFill — Full-frame container

```tsx
import {AbsoluteFill} from 'remotion';

<AbsoluteFill style={{backgroundColor: '#0b84f3', justifyContent: 'center', alignItems: 'center'}}>
  <h1 style={{fontSize: 80, color: 'white'}}>Hello</h1>
</AbsoluteFill>
```

### Full Animation Template

```tsx
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const AnimatedTitle: React.FC<{title: string}> = ({title}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1], {extrapolateRight: 'clamp'});
  const scale = spring({fps, frame: frame - 10, config: {damping: 100}});
  const translateY = interpolate(frame, [0, 30], [50, 0], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: 'white', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{opacity, transform: `scale(${scale}) translateY(${translateY}px)`, fontSize: 80}}>
        {title}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Phase 4: Timeline with Sequence & Series

### Sequence — Show component for a time range

```tsx
import {Sequence} from 'remotion';

<Sequence from={0} durationInFrames={60}>
  <TitleCard />
</Sequence>
<Sequence from={60} durationInFrames={90}>
  <MainContent />
</Sequence>
```

### Series — Play clips back-to-back

```tsx
import {Series} from 'remotion';

<Series>
  <Series.Sequence durationInFrames={90}>
    <Scene1 />
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <Scene2 />
  </Series.Sequence>
  <Series.Sequence durationInFrames={30}>
    <Outro />
  </Series.Sequence>
</Series>
```

---

## Phase 5: Media & Assets

### Embed Video

```tsx
import {OffthreadVideo} from 'remotion';

<OffthreadVideo src="https://example.com/video.mp4" />
```

### Static Files (from public/ folder)

```tsx
import {staticFile} from 'remotion';
import {Img} from 'remotion';

<Img src={staticFile('logo.png')} />
<OffthreadVideo src={staticFile('intro.mp4')} />
```

Place files in `public/` directory, reference with `staticFile('filename.ext')`.

---

## Phase 6: Data Fetching

Use `delayRender` / `continueRender` to pause rendering until data loads:

```tsx
import {delayRender, continueRender, cancelRender} from 'remotion';

const DataVideo: React.FC = () => {
  const [data, setData] = useState(null);
  const [handle] = useState(() => delayRender());

  useEffect(() => {
    fetch('https://api.example.com/data')
      .then(r => r.json())
      .then(json => { setData(json); continueRender(handle); })
      .catch(err => cancelRender(err));
  }, [handle]);

  if (!data) return null;
  return <div>{/* render with data */}</div>;
};
```

For dynamic duration from fetched data, see `references/api-advanced.md`.

---

## Phase 7: Render Output

### Preview in Studio

```bash
npx remotion studio src/index.ts
```

### CLI Rendering

```bash
# MP4 (default codec)
npx remotion render src/index.ts my-video out/video.mp4

# Custom props
npx remotion render src/index.ts my-video out/video.mp4 --props='{"title":"Hello"}'

# Specific frame range
npx remotion render src/index.ts my-video out/video.mp4 --frames=0-100

# GIF
npx remotion render src/index.ts my-video out/animation.gif --codec=gif

# Still image
npx remotion still src/index.ts my-video out/frame.png --frame=30

# Quality control
npx remotion render src/index.ts my-video out/video.mp4 --crf=18 --codec=h264
```

### Programmatic Rendering (Node.js)

Write a render script (e.g., `render.ts`):

```tsx
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import path from 'path';

const render = async () => {
  const bundleLocation = await bundle({
    entryPoint: path.join(process.cwd(), './src/index.ts'),
  });

  const inputProps = {title: 'My Video'};
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: 'my-video',
    inputProps,
  });

  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: 'out/video.mp4',
    inputProps,
    onProgress: ({progress}) => console.log(`${(progress * 100).toFixed(1)}%`),
  });
};

render();
```

Run with: `npx tsx render.ts`

### Common Codec Options

| Output | codec flag |
|--------|-----------|
| MP4 | `--codec=h264` (default) |
| WebM | `--codec=vp8` |
| GIF | `--codec=gif` |
| ProRes | `--codec=prores` |

---

## Quick Reference: File Templates

### Minimal Component

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: 'white'}}>
      <div style={{fontSize: 60}}>Frame {frame}</div>
    </AbsoluteFill>
  );
};
```

### Multi-Scene Video

```tsx
import {AbsoluteFill, Sequence, Series, interpolate, useCurrentFrame} from 'remotion';

const Scene: React.FC<{color: string; text: string; length: number}> =
  ({color, text, length}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, length], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: color, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontSize: 80, color: 'white', opacity: progress}}>{text}</div>
    </AbsoluteFill>
  );
};

export const MultiScene: React.FC = () => (
  <Series>
    <Series.Sequence durationInFrames={90}>
      <Scene color="#0b84f3" text="Intro" length={90} />
    </Series.Sequence>
    <Series.Sequence durationInFrames={120}>
      <Scene color="#e84393" text="Content" length={120} />
    </Series.Sequence>
    <Series.Sequence durationInFrames={60}>
      <Scene color="#00b894" text="Outro" length={60} />
    </Series.Sequence>
  </Series>
);
```

---

## Agent Zero Tool Mapping

| Action | Tool | Command/Operation |
|--------|------|-------------------|
| Scaffold project | `code_execution_tool` (terminal) | `npx create-video@latest ...` |
| Install packages | `code_execution_tool` (terminal) | `npm install ...` |
| Create/edit files | `text_editor:write` / `text_editor:patch` | Write `.tsx` / `.ts` files |
| Read existing files | `text_editor:read` | Inspect components |
| Preview studio | `code_execution_tool` (terminal) | `npx remotion studio src/index.ts` |
| Render video | `code_execution_tool` (terminal) | `npx remotion render ...` |
| Run render script | `code_execution_tool` (terminal) | `npx tsx render.ts` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `registerRoot` not found | Ensure `src/index.ts` calls `registerRoot(RemotionRoot)` |
| Component not showing | Check `id` in `<Composition>` matches render command argument |
| Animation not smooth | Verify `fps` matches between Composition and animation math |
| Static file 404 | Place files in `public/`, use `staticFile('name')` not paths |
| Render OOM | Lower resolution or use `--concurrency=1` flag |
| Bundle errors | Run `npx remotion browser ensure` to download Chrome |
