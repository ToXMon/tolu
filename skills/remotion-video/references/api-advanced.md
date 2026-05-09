# Remotion Advanced API Reference

## calculateMetadata — Dynamic Duration & Dimensions

When composition metadata (duration, dimensions) depends on fetched data or props:

```tsx
import {Composition} from 'remotion';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="dynamic-video"
      component={DynamicVideo}
      calculateMetadata={async ({props}) => {
        const data = await fetch(`https://api.example.com/video/${props.id}`).then(r => r.json());
        return {
          durationInFrames: data.scenes.length * 90,
          width: data.widescreen ? 1920 : 1080,
          height: data.widescreen ? 1080 : 1920,
          props: {...props, fetchedData: data},
        };
      }}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{id: 'default'}}
    />
  );
};
```

## `<Composition>` Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Unique identifier for rendering |
| component | React.FC | Yes | Video component |
| durationInFrames | number | Yes* | Total frames (*overridable by calculateMetadata) |
| fps | number | Yes | Frames per second |
| width | number | Yes* | Width in px |
| height | number | Yes* | Height in px |
| defaultProps | object | No | Default prop values |
| schema | ZodSchema | No | Zod schema for props validation |
| calculateMetadata | function | No | Async function to compute metadata dynamically |
| lazyComponent | () => Promise | No | Code-split component loader |

## interpolate Options

```tsx
interpolate(frame, inputRange, outputRange, options?)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| extrapolateLeft | 'extend' \| 'clamp' \| 'identity' | 'extend' | Behavior below input range |
| extrapolateRight | 'extend' \| 'clamp' \| 'identity' | 'extend' | Behavior above input range |
| easing | (t: number) => number | (t) => t | Easing function |

## spring Options

```tsx
spring({fps, frame, config?})
```

| Config | Type | Default | Description |
|--------|------|---------|-------------|
| damping | number | 14 | Higher = less bouncy |
| stiffness | number | 80 | Higher = faster |
| mass | number | 1 | Higher = heavier/slower |
| overshootClamping | boolean | false | Clamp to never exceed 1.0 |

## Sequence Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| from | number | Yes | Start frame |
| durationInFrames | number | Yes | Length in frames |
| name | string | No | Label for timeline |
| layout | 'absolute-fill' \| 'none' | 'absolute-fill' | Positioning |

## `<Audio>` Component

```tsx
import {Audio} from 'remotion';

// From static file
<Audio src={staticFile('bgm.mp3')} volume={0.5} />

// From URL
<Audio src="https://example.com/audio.mp3" startFrom={30} endAt={120} />

// Volume animation
const volume = interpolate(frame, [0, 30], [0, 0.5], {extrapolateRight: 'clamp'});
<Audio src={staticFile('music.mp3')} volume={volume} />
```

## `<Video>` vs `<OffthreadVideo>`

- `<Video>` — Renders in main thread. Simpler but can block.
- `<OffthreadVideo>` — Renders in separate thread. Preferred for production.

Both accept `src`, `startAt`, `endAt`, `volume`, `playbackRate`, `muted`.

## `<Loop>` Component

```tsx
import {Loop} from 'remotion';

<Loop durationInFrames={60} times={Infinity}>
  <SpinningLogo />
</Loop>
```

## `<Freeze>` Component

```tsx
import {Freeze} from 'remotion';

<Freeze frame={30}>
  <AnimatedScene />
</Freeze>
```

## Easing Functions

```tsx
import {Easing} from 'remotion';

// Available easings for interpolate
Easing.linear(t)
Easing.quad(t)         // quadratic
Easing.cubic(t)        // cubic
Easing.bezier(0.25, 0.1, 0.25, 1)(t)
Easing.in(Easing.cubic)(t)
Easing.out(Easing.cubic)(t)
Easing.inOut(Easing.cubic)(t)
```

## CLI Flags Reference

### render
```
npx remotion render <entry> <comp-id> <output> [flags]
```

| Flag | Description |
|------|-------------|
| --props '<json>' | Input props as JSON |
| --frames=<start>-<end> | Render frame range |
| --codec=h264\|vp8\|gif\|prores | Output codec |
| --crf=<number> | Quality (lower = better, 0-51, default 18 for h264) |
| --concurrency=<n> | Parallel render threads |
| --scale=<n> | Resolution scale factor |
| --frames-per-lambda=<n> | For Lambda rendering |
| --log=verbose\|info\|warn\|quiet | Log level |

### still
```
npx remotion still <entry> <comp-id> <output> [flags]
```

| Flag | Description |
|------|-------------|
| --frame=<n> | Frame to capture |
| --scale=<n> | Resolution scale |
| --props '<json>' | Input props |

## Programmatic API (@remotion/renderer)

### selectComposition
```tsx
const composition = await selectComposition({
  serveUrl: bundleLocation,  // URL or local path from bundle()
  id: 'my-video',
  inputProps: {title: 'Hello'},
  browserInstance: puppeteerInstance,  // optional
});
// Returns: {id, durationInFrames, fps, width, height, defaultProps}
```

### renderMedia
```tsx
await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  inputProps: {title: 'Hello'},
  onProgress: ({progress}) => console.log(progress),
  onBrowserLog: (log) => console.log(log),
  crf: 18,
  concurrency: 1,
  imageFormat: 'jpeg',  // 'png' for quality, 'jpeg' for speed
});
```

### renderStill
```tsx
await renderStill({
  composition,
  serveUrl: bundleLocation,
  output: 'out/frame.png',
  frame: 30,
  inputProps: {title: 'Hello'},
  imageFormat: 'png',
});
```

### stitchFramesToVideo
```tsx
import {stitchFramesToVideo} from '@remotion/renderer';

await stitchFramesToVideo({
  dir: 'frames/',
  fps: 30,
  outputLocation: 'out/video.mp4',
  codec: 'h264',
});
```
