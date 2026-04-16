# BrowserPod Comprehensive Research Report

Date: 2026-04-15
Sources: browserpod.io docs, pricing page, local repo analysis, CheerpX documentation, Leaning Technologies ecosystem

---

## 1. Documentation Pages — Full Summary

### Architecture Overview

Source: https://browserpod.io/docs/overview

BrowserPod is a universal execution layer for browser-based compute. It provides a sandboxed runtime API for running full-stack workloads directly inside the browser tab.

**How it works (4 layers):**

1. **Runtime Loading** — Complete language runtimes (Node.js v22) compiled to WebAssembly, targeting a Linux-compliant syscall interface
2. **Execution** — Browser's JS engine executes Wasm-compiled runtime using WebWorkers for multi-threading and process isolation
3. **Resource Virtualization** — Block-based streaming virtual filesystem with full POSIX compatibility. Disk images streamed on-demand, file changes stay local
4. **Networking via Portals** — When a service inside the pod listens on a port, BrowserPod creates a Portal (secure URL routing external traffic to the browser process)

**Roadmap:**

- Currently: Node.js v22 support
- 2026: CLI tools (bash, git, coreutils), Python, Ruby, Go, Rust engines
- Future: Linux-class workloads via CheerpX

**Company:** Leaning Technologies (leaningtech.com), also builds Cheerp, CheerpJ, CheerpX

---

### Quickstart Guide

Source: https://browserpod.io/docs/getting-started/quickstart

1. Register at console.browserpod.io (GitHub auth)
2. Create API key in console
3. Run `npm create browserpod-quickstart`
4. Enter project name and API key
5. `cd <project> && npm install && npm run dev`
6. Open localhost (e.g., http://localhost:5173/)
7. Modify `src/main.js` with hot reloading

---

### Express.js Tutorial

Source: https://browserpod.io/docs/getting-started/expressjs

Two NPM projects in one repo: top-level Vite project serves the web page with BrowserPod; inner project in `public/project/` runs inside BrowserPod.

Critical requirement — vite.config.js must set COEP/COOP headers:

~~~js
import { defineConfig } from "vite";
export default defineConfig({
  server: {
    headers: {
      "Cross-Origin-Embedder-Policy": "require-corp",
      "Cross-Origin-Opener-Policy": "same-origin",
    },
  },
});
~~~

Core integration pattern:

~~~js
import { BrowserPod } from "@leaningtech/browserpod";

const pod = await BrowserPod.boot({ apiKey: import.meta.env.VITE_BP_APIKEY });
const terminal = await pod.createDefaultTerminal(document.querySelector("#console"));

pod.onPortal(({ url, port }) => {
  document.getElementById("portal").src = url;
});

await pod.createDirectory("/project");
// copy files into pod filesystem...
await pod.run("npm", ["install"], { echo: true, terminal, cwd: "/project" });
await pod.run("node", ["main.js"], { echo: true, terminal, cwd: "/project" });
~~~

---

### API Reference

Source: https://browserpod.io/docs/reference/BrowserPod

**BrowserPod.boot()**

~~~
static async boot(opts: {
  apiKey: string;
  nodeVersion?: string;     // Currently only "22" allowed
  storageKey?: string;      // For multiple independent disks
}): Promise<BrowserPod>
~~~

Deducts 10 tokens from account balance on each call. `storageKey` enables multiple independent virtual disks.

**pod.run()**

~~~
async run(
  executable: string,
  args: Array<string>,
  opts: { terminal: Terminal; env?: Array<string>; cwd?: string; echo?: boolean }
): Promise<Process>
~~~

**pod.onPortal()**

~~~
onPortal(cb: ({ url: string, port: number }) => void): void
~~~

Callback invoked when a Portal is created (service binds to a port inside the pod).

**Filesystem API:**

- `createDirectory(path, { recursive? })` — create directories
- `createFile(path, mode)` — returns BinaryFile or TextFile depending on mode ("binary" | "utf-8")
- `openFile(path, mode)` — open existing file, rejects if not found
- BinaryFile: `write(ArrayBuffer)`, `read(length)`, `getSize()`, `close()`
- TextFile: `write(string)`, `read(length)`, `getSize()`, `close()`

**Terminal:**

~~~
createDefaultTerminal(consoleDiv: HTMLElement): Promise<Terminal>
~~~

Creates Xterm.js-based terminal emulator. REQUIRES a DOM element — browser-only, not headless-capable.

**Full TypeScript type definitions (from local repo `/browserpod/src/index.d.ts`):**

~~~typescript
export class Terminal {}
export class Process {}

export class BinaryFile {
  write(data: ArrayBuffer): Promise<number>;
  read(length: number): Promise<ArrayBuffer>;
  getSize(): Promise<number>;
  close(): Promise<void>;
}

export class TextFile {
  write(data: string): Promise<number>;
  read(length: number): Promise<string>;
  getSize(): Promise<number>;
  close(): Promise<void>;
}

export class BrowserPod {
  static boot(opts: {
    nodeVersion?: string;
    apiKey: string;
  }): Promise<BrowserPod>;

  run(
    executable: string,
    args: Array<string>,
    opts: {
      terminal: Terminal,
      env?: Array<string>;
      cwd?: string,
      echo?: boolean
    }
  ): Promise<Process>;

  onPortal(cb: (args: { url: string, port: number }) => void): void;

  createDirectory(
    path: string,
    opts?: { recursive?: boolean }
  ): Promise<void>;

  createFile(path: string, mode: string): Promise<BinaryFile | TextFile>;
  openFile(path: string, mode: string): Promise<BinaryFile | TextFile>;

  createDefaultTerminal(consoleDiv: HTMLElement): Promise<Terminal>;
}
~~~

---

### Filesystem

Source: https://browserpod.io/docs/understanding-browserpod/filesystem

- Virtual Linux-like filesystem with POSIX-style paths
- Lives inside Pod runtime, NOT the host machine's filesystem
- Persistence via IndexedDB in browser, scoped to origin
- Data persists across page reloads for same origin; different origin = separate state
- File modes: "binary" (ArrayBuffer) or "utf-8" (text strings)
- File handles must be explicitly closed (not garbage collected)
- Processes launched with `pod.run()` see filesystem as local disk
- v2.0.0: 2GB available at `/home` mount point

---

### Portals

Source: https://browserpod.io/docs/understanding-browserpod/portals

- Controlled networking feature exposing services inside Pod through secure, shareable URLs
- NOT a separate server — routing layer connecting public URL to browser process
- Created automatically when process binds to a port inside the Pod
- Multiple ports = multiple Portals
- Use cases: live previews, interactive demos, collaborative workflows, shareable environments

---

### Cross-Origin Isolation

Source: https://browserpod.io/docs/understanding-browserpod/cross-origin-isolation

BrowserPod requires SharedArrayBuffer, which needs:

~~~
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
~~~

Without these headers, the browser blocks SharedArrayBuffer and the pod fails to start. Localhost exception: works over HTTP without headers. Production requires HTTPS.

---

### Demos

Source: https://browserpod.io/docs/demos

- **PackagePod**: Live BrowserPod demo running in browser
- **SaySomething**: Ephemeral flash surveys running entirely in browser

---

## 2. Pricing — Exact Terms

Source: https://browserpod.io/browserpod-pricing-policy

### Token Model

- 10 tokens/hour per sandbox
- Charged only while sandbox is live, billed in hourly blocks
- Token top-ups: $10 per 10,000 tokens

### Free Plan ($0/mo)

- Personal projects and non-commercial use ONLY
- 10,000 API tokens/month (~1,000 hours)
- Up to 5 API keys
- Up to 5 origin domains
- Portals for live demos
- NO commercial usage, NO overage, NO outbound networking, NO self-hosting, NO SSO
- MUST display BrowserPod attribution (visible link + logo)

### Pro Plan ($20/mo)

- Commercial usage allowed
- 20,000 API tokens/month (~2,000 hours)
- Overage: $0.01/hour
- Unlimited API keys, unlimited origin domains
- Portals for live demos
- NO outbound networking, NO self-hosting, NO SSO

### Enterprise Plan (Custom pricing)

- Custom token allocation and overage terms
- Outbound networking whitelists
- Self-hosting available
- SSO integration
- Dedicated solutions engineer
- Administration & analytics API

### Token Grants

- Open-source projects: Up to 100,000 tokens/month (apply online)
- Startups: Up to 10M tokens ($10k value, apply online)

### Billing

- Processed via Paddle

---

## 3. CheerpX by Leaning Technologies

### What is CheerpX?

Sources: https://cheerpx.io, https://leaningtech.com/cheerpx, https://labs.leaningtech.com/blog/cx-10

CheerpX is a WebAssembly-based x86 virtualization engine by Leaning Technologies. It runs unmodified x86 Linux binaries entirely in the browser using a two-tier emulation approach (interpreter + JIT compiler). v1.0 stable released December 2024.

**Technical Architecture:**

~~~
+------------------------------------------+
|           Application Layer              |
|   (Node.js, Python, bash, gcc, etc.)     |
+------------------------------------------+
|         Linux Syscall Emulator           |
+------------------------------------------+
|      Virtual Block-based Filesystem      |
|   (CloudDevice, HttpBytesDevice,         |
|    GitHubDevice, IDBDevice, Overlay)     |
+------------------------------------------+
|    x86-to-WebAssembly JIT Compiler       |
|   (Interpreter + JIT tiers)              |
+------------------------------------------+
|           WebAssembly Sandbox            |
+------------------------------------------+
~~~

**Key capabilities:**

- Runs unmodified x86 Linux binaries in browser (no recompilation)
- Supports dynamically generated code (V8 JIT output)
- Handles self-modifying code
- 100% client-side, zero server-side computation
- Works offline after initial load
- Streams disk images on-demand from CDN

**Block Device Types:**

| Device | Purpose |
|--------|----------|
| CloudDevice | Stream disk images from CDN |
| HttpBytesDevice | HTTP byte-range access |
| GitHubDevice | Load content from GitHub |
| IDBDevice | IndexedDB persistent storage |
| OverlayDevice | Writable cache over read-only base |

### How BrowserPod Relates to CheerpX

Hierarchical relationship:

~~~
BrowserPod (product — in-browser sandboxes)
    |
    +-- CheerpOS (runtime — Linux-like syscall layer)
            |
            +-- CheerpX (engine — x86 virtualization)
~~~

When Node.js code runs in BrowserPod:

1. Node.js binary loaded as x86 code
2. CheerpX JIT compiles and executes it
3. Node.js makes syscalls (fs.open, net.connect, etc.)
4. CheerpOS intercepts those syscalls
5. CheerpOS fulfills them using CheerpX's virtual filesystem/networking
6. All within the browser sandbox

### Leaning Technologies Ecosystem

| Product | Purpose | Layer |
|---------|---------|-------|
| Cheerp | C/C++ to WebAssembly compiler | Compiler toolchain |
| CheerpJ | Java apps in browser | Runtime |
| CheerpX | x86 virtualization in browser | Virtualization engine |
| BrowserPod | In-browser sandboxes | Product/SaaS |
| WebVM | Complete Linux VM in browser | Demo/Platform |
| CheerpOS | Linux-like syscall runtime | OS layer |

### GitHub Check: niclas-nick

The GitHub user `niclas-nick` does NOT exist (HTTP 404). No CheerpX-related repositories found there.

Official Leaning Technologies repos:

- https://github.com/leaningtech/cheerpx-meta (main CheerpX repo)
- https://github.com/leaningtech/webvm (WebVM powered by CheerpX)
- https://github.com/leaningtech/browserpod-meta (BrowserPod issues)
- https://github.com/leaningtech/svelte-browserpod-editor (Svelte component library)

---

## 4. Headless / Programmatic API

**No, BrowserPod cannot run headless.**

Evidence from multiple sources:

- `createDefaultTerminal(consoleDiv: HTMLElement)` requires a DOM element
- The entire runtime depends on SharedArrayBuffer (browser-only API)
- The SDK is loaded from CDN via browser `import()` — no Node.js runtime
- The npm package (`index.js`) contains explicit SSR fallback returning `null`: `// Be robust to spurious SSR of this import`
- The npm package source (from local repo):

~~~js
const version = "2.0.2";
const dynImport = new Function("x", "return import(x)");
async function loadLibrary() {
  try {
    return await dynImport(`https://rt.browserpod.io/${version}/browserpod.js`);
  } catch(e) {
    return { BrowserPod: null }; // SSR fallback
  }
}
const Library = await loadLibrary();
export const BrowserPod = Library.BrowserPod;
~~~

There is NO Node.js programmatic API for server-side use. BrowserPod is fundamentally a browser-only product.

---

## 5. Screenshots

**No native screenshot capability exists in BrowserPod.**

BrowserPod provides:

- Terminal output (via Xterm.js)
- Portal URLs (for services running inside the pod)
- File I/O (read/write files)

To capture screenshots, you would need to:

1. Open the Portal URL in a separate browser tab/window
2. Use external tools (Puppeteer, Playwright) to screenshot that URL
3. Or use the browser's native `html2canvas` / canvas APIs on the page containing the Portal iframe

---

## 6. Testing in a Real Browser Environment

**Partially, with significant caveats.**

BrowserPod CAN run Node.js test frameworks (Jest, Mocha, etc.) inside the pod since it executes Node.js v22. However:

- Tests run inside a WebAssembly virtualized environment, not a "real" browser environment
- The test code runs in Node.js context (server-side), not browser DOM context
- There is no built-in test runner or test discovery mechanism
- Test output would appear in the Xterm.js terminal
- You would need to manually copy test files into the pod filesystem and run them

For browser testing (testing actual DOM interactions), BrowserPod is NOT suitable. It runs Node.js, not a browser rendering engine. For browser testing, use Playwright, Puppeteer, or Cypress instead.

---

## 7. Portal Capabilities — Technical Deep Dive

### How Portals Work

1. Code inside the Pod starts an HTTP server and binds to a port (e.g., `app.listen(3000)`)
2. BrowserPod detects the port binding
3. BrowserPod automatically creates a Portal — a secure, shareable public URL
4. The `onPortal` callback fires with `{ url, port }`
5. The URL can be loaded in an iframe, new tab, or shared externally
6. Traffic to the Portal URL is routed to the service running inside the browser

### Can External Services Access Portals?

**Yes.** Portal URLs are public and shareable. Anyone with the URL can access the service running inside the browser pod. This means:

- External users can interact with a demo running in YOUR browser
- The URL routes traffic from the internet through BrowserPod's infrastructure to your browser tab
- This works even though the server runs client-side

### Technical Constraints

- Portal URLs are ephemeral — tied to the browser session
- If the browser tab closes, the Portal becomes unreachable
- Performance depends on the browser's resources and network connection
- Portal routing adds latency compared to direct server access

---

## 8. Language Runtime Support — Currently Available

### Currently Supported (v2.0.2)

- **Node.js v22** — the ONLY language runtime currently available
- **CLI tools** (added in v2.0.0): bash, git, curl, grep, openssl, vi

### Planned / Roadmap (NOT currently available)

- Python
- Ruby
- Go
- Rust
- Linux-class workloads via CheerpX

**Important:** The docs and README mention Python, Ruby, Go as future additions. As of v2.0.2, only Node.js v22 is available as a language runtime.

---

## 9. Known Limitations, Performance, and Security

### Known Limitations

1. **Browser-only** — Requires DOM, cannot run headless or server-side
2. **COOP/COEP headers required** — SharedArrayBuffer needs cross-origin isolation headers (except localhost over HTTP)
3. **API key required** — From console.browserpod.io, metered by tokens
4. **Node.js v22 only** — Single runtime currently available
5. **32-bit x86 only** — CheerpX currently supports only 32-bit x86 binaries
6. **Syscall coverage** — Extended subset, not 100% Linux syscall compatibility
7. **User mode only** — No kernel mode support
8. **Browser memory limits** — Bounded by browser tab constraints
9. **No outbound networking** — On free and pro tiers; enterprise only with whitelists
10. **2GB filesystem** — `/home` mount point limited to 2GB in v2.0.0
11. **File handles must be closed explicitly** — Not garbage collected
12. **Attribution required on free tier** — Visible BrowserPod link + logo

### Performance Characteristics

- **Two compilation layers**: x86 -> WebAssembly -> native code (browser JIT handles second step)
- **Two-tier execution**: Interpreter for cold code, JIT for hot paths
- **Streaming filesystem**: Disk images loaded progressively, not upfront
- **No server roundtrips**: Zero network latency for computation
- **Client-side scaling**: Compute scales with number of users (no server bottleneck)
- **Not suitable for compute-heavy workloads**: Gaming, video encoding, etc.
- **Startup time**: Initial image streaming may cause slow first load

### No Published Benchmarks

BrowserPod/CheerpX do not publish quantitative performance benchmarks. They use a "native instruction multiplier" metric internally but do not share specific numbers.

### Security Model

1. **WebAssembly sandbox**: All x86 code runs within Wasm sandbox — cannot escape to host
2. **Browser isolation**: Leverages browser's existing security model
3. **No server exposure**: Untrusted code never runs on external servers
4. **Data privacy**: User data never leaves the browser (client-side only)
5. **No server attack surface**: Eliminates risk of malicious code on external servers
6. **IndexedDB scoping**: Filesystem state scoped to origin

### Security Concerns

- Portal URLs are publicly accessible once created — could expose services unintentionally
- API keys stored in client-side code (environment variables) — could be extracted from browser
- CDN dependency on rt.browserpod.io — runtime loaded from external server
- Browser sandbox is the only security boundary — if Wasm sandbox breaks, browser is the fallback

---

## 10. Management Console (console.browserpod.io)

Source: https://console.browserpod.io

### What It Provides

- **Account registration** via GitHub OAuth
- **API key management**: Create, view, and manage API keys
- **Dashboard**: Overview of token usage and account status
- **Key management** at /keys endpoint

### Limitations

- No usage analytics visible on free/pro tiers (enterprise only has admin & analytics API)
- No team management on free/pro tiers
- No detailed billing dashboard mentioned

---

## Appendix A: Local Source Code Analysis

### npm package structure (browserpod v2.0.2)

The npm package is a thin wrapper (16 lines of JavaScript):

~~~js
const version = "2.0.2";
const dynImport = new Function("x", "return import(x)");
async function loadLibrary() {
  try {
    return await dynImport(`https://rt.browserpod.io/${version}/browserpod.js`);
  } catch(e) {
    return { BrowserPod: null }; // SSR fallback
  }
}
const Library = await loadLibrary();
export const BrowserPod = Library.BrowserPod;
~~~

The actual runtime is loaded from CDN (`rt.browserpod.io`). The npm package provides TypeScript types and a loader.

### Monorepo structure

- `packages/browserpod` — core npm package (index.js + index.d.ts)
- `packages/browserpod-lt` — Leaning Technologies internal package
- `packages/browserpod-quickstart` — `npm create browserpod-quickstart` scaffolding with templates (vite-basic, vite-web)

### License

Source: /browserpod/LICENSE.txt

Proprietary. Copyright (c) 2025 Leaning Technologies. Free for personal/open-source only. Commercial use requires paid plan. No rights granted except as permitted by TOS, Pricing Policy, and Privacy Policy.

---

## Appendix B: Changelog Summary

- **v2.0.2**: Current version
- **v2.0.0**: CLI tools (git, bash, curl, grep, openssl, vi), disk performance improvements, 2GB /home mount, storageKey for multiple independent disks
- **v1.3.0**: Syscalls improvements, network performance, initial Wasm program support
- **v1.2.0**: /dev and /proc support, larger disk images, npx support, fork/execve improvements
- **v1.1.0**: Major framework support (Next.js, Nuxt, Express, Svelte, React), HTTP compression via portals, worker improvements
- **v1.0.0**: Faster BrowserPod.boot()
- **v0.9.2**: Node.js REPL support, TypeScript types, first public beta

---

## Appendix C: Key URLs

| Resource | URL |
|----------|-----|
| Main site | https://browserpod.io |
| Documentation | https://browserpod.io/docs |
| Architecture Overview | https://browserpod.io/docs/overview |
| Quickstart | https://browserpod.io/docs/getting-started/quickstart |
| Express.js Tutorial | https://browserpod.io/docs/getting-started/expressjs |
| API Reference | https://browserpod.io/docs/reference/BrowserPod |
| Filesystem Docs | https://browserpod.io/docs/understanding-browserpod/filesystem |
| Portals Docs | https://browserpod.io/docs/understanding-browserpod/portals |
| Cross-Origin Isolation | https://browserpod.io/docs/understanding-browserpod/cross-origin-isolation |
| Demos | https://browserpod.io/docs/demos |
| Console/API Keys | https://console.browserpod.io |
| Pricing | https://browserpod.io/browserpod-pricing-policy |
| Terms of Service | https://browserpod.io/browserpod-tos |
| Privacy Policy | https://browserpod.io/browserpod-privacy-policy |
| GitHub Issues | https://github.com/leaningtech/browserpod-meta/issues |
| Svelte Components | https://github.com/leaningtech/svelte-browserpod-editor |
| npm package | https://npm.im/browserpod |
| CheerpX | https://cheerpx.io |
| CheerpX Blog | https://labs.leaningtech.com/blog/cx-10 |
| Leaning Technologies | https://leaningtech.com |
| WebVM Demo | https://webvm.io |
| Discord | https://discord.leaningtech.com |
| Runtime CDN | https://rt.browserpod.io |
| Enterprise Contact | https://forms.leaningtech.com/leaningforms/form/BookaDemo/formperma/2zFTrXkIeE0kW_6tyq1wbmbWM0Jf8s6Tft4ot0waF0Q |

---

## Supplementary Research Files

- `/a0/tmp/browserpod-comprehensive-report.md` (519 lines) — full subordinate research output
- `/a0/tmp/browserpod-docs-research.md` (420 lines) — raw docs/pricing research
- `/a0/tmp/cheerpx-research.md` (473 lines) — detailed CheerpX/Leaning Technologies research
- Local repo: `/a0/usr/workdir/browserpod/` — npm package source with types, license, examples
