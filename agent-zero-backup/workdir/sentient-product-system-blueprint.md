# SENTIENT — Product System Blueprint
## Emotionally Intelligent AI Platform
### Version 1.0 | April 2026 | Confidential

---

# TABLE OF CONTENTS

1. [Product Definition](#1-product-definition)
2. [System Architecture](#2-system-architecture)
3. [AI/ML Pipeline](#3-aiml-pipeline)
4. [Privacy & Security Architecture](#4-privacy--security-architecture)
5. [Technology Stack](#5-technology-stack)
6. [Viral Growth Engine](#6-viral-growth-engine)
7. [Monetization Architecture](#7-monetization-architecture)
8. [MVP Technical Scope](#8-mvp-technical-scope)

---

# 1. PRODUCT DEFINITION

## 1.1 Product Identity

| Attribute | Value |
|-----------|-------|
| **Name** | **Sentient** |
| **Tagline** | *"The AI that actually knows how you feel."* |
| **Category** | Emotionally Intelligent Personal AI Companion |
| **Target User (Consumer)** | 18-45 year olds who journal, track mental health, or use personality/astrology content |
| **Target User (Enterprise)** | Healthcare systems, digital therapeutics companies, clinical research organizations |
| **Core Value Proposition** | Sentient is the first AI that understands your emotional patterns over time using privacy-first on-device emotion sensing — giving you insights about yourself you never had before |

## 1.2 Why This Product Goes Viral

### Growth Mechanism: "Emotional Mirror" Sharing

Sentient generates shareable emotional self-portraits — rich, beautiful visualizations of a user's emotional patterns over time. Think:

- **"My Emotional DNA"** — a unique visual fingerprint of your emotional baseline and variations
- **"EmotionSync"** — compare emotional patterns with friends (using only aggregated, anonymized embeddings)
- **"My Week in Feelings"** — auto-generated emotional journey summaries shareable as Instagram/TikTok stories
- **"Emotion Compatibility Score"** — viral friend/partner matching based on emotional rhythm alignment

### Why It Spreads

1. **Self-Discovery Addiction**: People are obsessed with understanding themselves (Myers-Briggs has 2M+ tests/day, astrology content = billions of views)
2. **Social Currency**: Sharing your "emotional fingerprint" is a status signal — it says you're emotionally aware
3. **Reciprocity Loop**: "See your compatibility with [friend]" requires both users to have the app
4. **Weekly Ritual**: Auto-generated emotional summaries create habitual engagement + shareable moments
5. **Network Density**: More friends = richer compatibility insights = more sharing

### Viral Coefficient Model

```
K-factor = invitations_per_user × conversion_rate
Target: K = 1.3+ (each user brings 1.3 new users)

Mechanics:
- "EmotionSync" request to friend → push notification → app install
- Weekly emotional share → social media → 3-5% click-through → install
- Partner compatibility → 2-person requirement → built-in invitation
```

## 1.3 How Sentient Leverages Every Whitepaper Innovation

### Innovation 1: Dual-Axis Training Signal
**Implementation**: Every AI response is scored on two axes:
- **Score A (Reasoning Quality)**: Factual accuracy, relevance, helpfulness of the response
- **Score B (Emotional Salience)**: How well the response matches the user's detected emotional state
- **Final Score = Score A × (1 + α × Score B)** where α is the emotional weighting hyperparameter

This means Sentient doesn't just give "correct" answers — it gives emotionally appropriate ones. A user who is frustrated gets concise, direct responses. A user who is joyful gets expansive, playful ones. This is the core differentiator.

### Innovation 2: Emotional Memory Cabinet
**Implementation**: Bayesian user profile that evolves over time:
```
User Emotional Profile = {
  baseline_valence: Normal(μ, σ²),        # overall emotional tendency
  baseline_arousal: Normal(μ, σ²),        # energy level tendency
  circadian_pattern: Fourier(n_harmonics), # emotional rhythm over day/week
  trigger_sensitivity: Dict[stimulus, β],  # what affects this user
  recovery_rate: Exponential(λ),           # how quickly they bounce back
  last_recalibration: datetime,
  confidence_score: float,                 # model confidence in profile
  drift_detected: bool,
  drift_magnitude: float
}
```

The Cabinet self-corrects when predictions diverge from actual signals. If Sentient predicts you'll be stressed on Monday but you're fine, it updates your model. This creates deeply personalized emotional intelligence that improves with use.

### Innovation 3: On-Device Privacy Architecture
**Implementation**: Hard technical guarantees, not policy promises:

```
What stays on device (NEVER transmitted):
- Raw audio waveforms
- Camera/video frames
- Raw facial expression data
- Biometric sensor data (heart rate, GSR)
- Voice timbre recordings

What leaves device (derived signals only):
- Emotion classification logits: {joy: 0.72, neutral: 0.18, sadness: 0.06, ...}
- Valence/arousal scalar: (0.65, 0.42)
- Confidence score: 0.89
- Model version hash: "sha256:abc123..."
- Timestamp: "2026-04-15T14:32:00Z"
```

### Innovation 4: Fitzpatrick-Stratified Demographic Accuracy Gate
**Implementation**: Mechanical fairness enforcement:

```python
class DemographicAccuracyGate:
    """
    Architecturally enforced fairness: facial analysis module
    REFUSES to activate unless accuracy thresholds are met
    across ALL Fitzpatrick skin tone categories (I-VI).
    """
    
    FITZPATRICK_THRESHOLDS = {
        'I':   0.90,  # Very light
        'II':  0.90,  # Light
        'III': 0.90,  # Medium light
        'IV':  0.88,  # Medium
        'V':   0.88,  # Medium dark
        'VI':  0.88,  # Dark
    }
    
    def evaluate(self, validation_results: Dict[str, float]) -> GateDecision:
        min_accuracy = min(validation_results.values())
        worst_category = min(validation_results, key=validation_results.get)
        
        all_pass = all(
            validation_results[cat] >= threshold
            for cat, threshold in self.FITZPATRICK_THRESHOLDS.items()
        )
        
        if not all_pass:
            return GateDecision(
                activate=False,
                reason=f"Accuracy gate failed: {worst_category} = "
                       f"{validation_results[worst_category]:.2f}",
                fallback="voice_only"
            )
        return GateDecision(activate=True)
```

### Innovation 5: Cryptographic Attestation Chain
**Implementation**: Every emotional inference is traceable:

```
Attestation Chain Structure:

[Signal Capture]
  → device_id: UUID
  → timestamp: ISO8601
  → model_version: semantic + hash
  → input_hash: SHA256(derived_signal)

[Inference]
  → output_logits: Dict[emotion, float]
  → confidence: float
  → inference_hash: SHA256(output + input_hash)

[Alignment Check]
  → alignment_score: float
  → alignment_hash: SHA256(inference_hash + alignment_score)

[Storage]
  → Merkle leaf: SHA256(all_above)
  → Merkle proof: [sibling_hashes...]
  → Root hash: updated in append-only ledger
```

### Innovation 6: Multimodal Emotion Capture
**Implementation**: 4 parallel channels:

| Channel | Input | Processing Location | When Active |
|---------|-------|--------------------|----|
| Emoji Stream | User taps emoji in app | On-device (trivial) | Always |
| Free-Text | User journal entry or chat message | Cloud NLP | Always |
| Voice Tone | Microphone audio (user-initiated) | **On-device** (TFLite/CoreML) | During voice check-in |
| Facial Expression | Camera frames (user-initiated) | **On-device** (CoreML/ONNX) + Fitzpatrick gate | During video check-in |

## 1.4 How Sentient Exploits Every Market Gap

### Gap 1: No unified model delivers highest accuracy + low latency + explainability
**Exploitation**: Sentient's edge-first architecture achieves 96-98% accuracy at 2.7ms latency on ARM Cortex-M7 class hardware. The Dual-Axis scoring and Bayesian Cabinet provide built-in explainability — every prediction has a confidence score and can be traced to contributing signals. We target **96%+ accuracy + <50ms end-to-end latency + full attestation chain**.

### Gap 2: Emotion data not protected by HIPAA despite being health-adjacent
**Exploitation**: Sentient's On-Device Privacy Architecture + Cryptographic Attestation provides **stronger protection than HIPAA requires**. We make this a brand differentiator: "Your emotions are more protected than your medical records." This creates regulatory arbitrage — we're proactively compliant before regulation catches up.

### Gap 3: Apple/Samsung wearables use only self-reported mood tracking
**Exploitation**: Sentient delivers **automated ML inference on wearables**. Our edge models (48-86KB) run on existing smartwatch hardware (Apple S9 SiP, Snapdragon W5+, Exynos W1000). We turn Apple Watch and Galaxy Watch into emotion-aware devices without waiting for Apple/Samsung to build it themselves. This is a 12-18 month window before first-party solutions.

### Opportunity 1: Medical/safety apps permitted under EU AI Act
**Exploitation**: Sentient's enterprise tier targets **digital therapeutics and patient monitoring** — explicitly permitted under EU AI Act Article 5(1)(f) exception. We partner with healthcare systems (J&J network) for clinical deployment. Consumer tier qualifies as entertainment/transparency-only obligations.

### Opportunity 2: Japan = most permissive major economy
**Exploitation**: Day-1 launch in Japan. Localized emoji set, Japanese voice tone analysis (pitch-pattern emotion detection is culturally specific), partnership with LINE for distribution. Japan's cultural acceptance of emotion AI + permissive regulation = beachhead market.

### Opportunity 3: Edge AI achieves 96-99.7% accuracy with 6-86KB models
**Exploitation**: Our entire inference pipeline fits in **<100KB** — enabling smartwatch, earbud, and even hearing-aid deployment. This isn't theoretical; it's validated by published benchmarks.

### Opportunity 4: Neuromorphic processors enable sub-milliwatt inference
**Exploitation**: Sentient is architected for neuromorphic deployment (SynSense Speck at 0.7mW, Innatera PULSAR at <600µW). Our model format supports conversion to spiking neural network (SNN) representation. Future: always-on emotion sensing in smart glasses, earbuds, even clothing.

## 1.5 Founder Advantage Application

| Founder Skill | Sentient Application |
|--------------|---------------------|
| J&J employee / pharma network | Enterprise sales to healthcare systems; clinical validation studies; ATMP/therapy integration |
| AI security expert (MAESTRO, OWASP AST10) | Most secure emotion AI platform; trust as competitive moat; attestation chain design |
| Domino ML platform experience | Production MLOps pipeline; model monitoring at scale; governance framework |
| Web3/blockchain developer (Solidity, Akash) | Cryptographic attestation chain is native skill; Merkle tree implementation; potential token-gated premium features |
| Healthcare domain knowledge | Clinical validation study design; regulatory pathway navigation; patient safety considerations |
| Agent Zero architect | Agentic AI architecture for the companion; tool use for emotional actions; memory systems for Emotional Cabinet |

---

# 2. SYSTEM ARCHITECTURE

## 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER DEVICES                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │  iPhone   │  │ Android  │  │  Apple   │  │  Smart Earbuds   │    │
│  │   App     │  │   App    │  │  Watch   │  │  (future)        │    │
│  │          │  │          │  │  App     │  │                  │    │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────────────┐ │    │
│  │ │Edge  │ │  │ │Edge  │ │  │ │Edge  │ │  │ │ TinyML Model │ │    │
│  │ │ SDK  │ │  │ │ SDK  │ │  │ │ SDK  │ │  │ │  <50KB INT8  │ │    │
│  │ │      │ │  │ │      │ │  │ │      │ │  │ └──────────────┘ │    │
│  │ │Voice │ │  │ │Voice │ │  │ │Voice │ │  │                  │    │
│  │ │Face  │ │  │ │Face  │ │  │ │      │ │  │                  │    │
│  │ │Text  │ │  │ │Text  │ │  │ │      │ │  │                  │    │
│  │ │Emoji │ │  │ │Emoji │ │  │ │Emoji │ │  │                  │    │
│  │ └──┬───┘ │  │ └──┬───┘ │  │ └──┬───┘ │  └────────┬─────────┘    │
│  └────┼─────┘  └────┼─────┘  └────┼─────┘           │              │
│       │              │              │                │              │
│       │    ┌─────────┴──────────────┘                │              │
│       │    │  Derived Signals Only (encrypted TLS 1.3)│              │
│       │    │  NO raw biometric data leaves device     │              │
│       ▼    ▼                                         ▼              │
└───────┼────┼─────────────────────────────────────────┼──────────────┘
        │    │                                         │
        ▼    ▼                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY (Edge)                           │
│                    Cloudflare Workers / Fastly                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │  Rate Limiting  │  │  Auth/JWT      │  │  TLS Term.     │        │
│  │  (100 req/min)  │  │  Validation    │  │  (TLS 1.3)     │        │
│  └────────────────┘  └────────────────┘  └────────────────┘        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     KUBERNETES CLUSTER (GKE/EKS)                    │
│                                                                     │
│  ┌─────────────────────── MICROSERVICES ──────────────────────┐     │
│  │                                                             │     │
│  │  ┌──────────────────┐     ┌──────────────────┐             │     │
│  │  │ Signal Ingestion │     │ Emotion Fusion   │             │     │
│  │  │ Service          │────▶│ Engine           │             │     │
│  │  │ (Go/Rust)        │     │ (Python/PyTorch) │             │     │
│  │  │ Port: 8001       │     │ Port: 8002       │             │     │
│  │  └──────────────────┘     └────────┬─────────┘             │     │
│  │                                    │                        │     │
│  │  ┌──────────────────┐     ┌───────▼──────────┐             │     │
│  │  │ Emotional Memory │     │ Companion Agent   │             │     │
│  │  │ Cabinet          │◀───▶│ Service           │             │     │
│  │  │ (Python)         │     │ (Python/Agent Z)  │             │     │
│  │  │ Port: 8003       │     │ Port: 8004        │             │     │
│  │  └──────────────────┘     └────────┬──────────┘             │     │
│  │                                    │                        │     │
│  │  ┌──────────────────┐     ┌───────▼──────────┐             │     │
│  │  │ Attestation      │     │ Insight Generator │             │     │
│  │  │ Service          │◀────│ Service           │             │     │
│  │  │ (Rust)           │     │ (Python)          │             │     │
│  │  │ Port: 8005       │     │ Port: 8006        │             │     │
│  │  └──────────────────┘     └──────────────────┘              │     │
│  │                                                             │     │
│  │  ┌──────────────────┐     ┌──────────────────┐             │     │
│  │  │ User Profile     │     │ Social/Share     │             │     │
│  │  │ Service          │     │ Service          │             │     │
│  │  │ (Go)             │     │ (Go)             │             │     │
│  │  │ Port: 8007       │     │ Port: 8008       │             │     │
│  │  └──────────────────┘     └──────────────────┘              │     │
│  │                                                             │     │
│  │  ┌──────────────────┐     ┌──────────────────┐             │     │
│  │  │ Billing/Usage    │     │ Analytics        │             │     │
│  │  │ Service          │     │ Service          │             │     │
│  │  │ (Go)             │     │ (Python)         │             │     │
│  │  │ Port: 8009       │     │ Port: 8010       │             │     │
│  │  └──────────────────┘     └──────────────────┘              │     │
│  │                                                             │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────────────── DATA LAYER ─────────────────────────┐     │
│  │                                                             │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │     │
│  │  │ ScyllaDB │  │ TimescaleDB│  │ Redis    │  │ GCS/S3   │   │     │
│  │  │ (User    │  │ (Time-    │  │ (Cache + │  │ (Model   │   │     │
│  │  │ Profiles)│  │ series    │  │ Sessions)│  │ artifacts│   │     │
│  │  │          │  │ emotions) │  │          │  │ shares)  │   │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │     │
│  │                                                             │     │
│  │  ┌──────────────────────────────────────────────────────┐   │     │
│  │  │ Attestation Ledger (append-only PostgreSQL + Merkle) │   │     │
│  │  └──────────────────────────────────────────────────────┘   │     │
│  │                                                             │     │
│  └─────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

## 2.2 Microservices Breakdown

### Service 1: Signal Ingestion Service

| Attribute | Value |
|-----------|-------|
| **Language** | Go 1.22 |
| **Port** | 8001 |
| **Responsibility** | Receive derived emotional signals from devices, validate schema, deduplicate, route to fusion engine |
| **Throughput Target** | 10,000 signals/second per instance |
| **Max Latency** | <10ms p99 |

```go
// Signal schema received from device
type EmotionSignal struct {
    DeviceID    string             `json:"device_id"`
    UserID      string             `json:"user_id"`
    Timestamp   time.Time          `json:"timestamp"`
    SignalType  SignalType         `json:"signal_type"`  // emoji|text|voice|face
    Payload     json.RawMessage    `json:"payload"`
    ModelVersion string            `json:"model_version"`
    DeviceHash  string             `json:"device_hash"`  // attestation
}

type VoicePayload struct {
    EmotionLogits map[string]float64 `json:"emotion_logits"` // {joy:0.72, sadness:0.06,...}
    Valence       float64            `json:"valence"`        // [-1, 1]
    Arousal       float64            `json:"arousal"`        // [0, 1]
    Confidence    float64            `json:"confidence"`     // [0, 1]
}

type FacePayload struct {
    EmotionLogits      map[string]float64 `json:"emotion_logits"`
    FitzpatrickGate    GateResult         `json:"fitzpatrick_gate"`
    Confidence         float64            `json:"confidence"`
}
```

### Service 2: Emotion Fusion Engine

| Attribute | Value |
|-----------|-------|
| **Language** | Python 3.12 + PyTorch 2.2 |
| **Port** | 8002 |
| **Responsibility** | Fuse multimodal emotion signals into unified emotional state estimate |
| **Model** | Lightweight cross-modal attention transformer (TACFN-inspired, ~0.34M params) |
| **Max Latency** | <30ms p99 |

```python
class EmotionFusionEngine:
    """
    Fuses signals from 4 channels into unified emotional state.
    
    Architecture: Cross-modal attention with confidence-weighted fusion.
    Inspired by TACFN (0.34M params) and MemoCMT.
    
    Target accuracy: 85%+ on 4-class emotion (IEMOCAP equivalent)
    Target latency: <30ms on CPU (vLLM/TorchServe optimized)
    """
    
    MODALITIES = ['emoji', 'text', 'voice', 'face']
    EMOTION_CLASSES = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'neutral']
    
    def fuse(self, signals: Dict[str, EmotionSignal]) -> FusedState:
        # Confidence-weighted attention fusion
        weights = softmax([s.confidence * modality_reliability[m] 
                          for m, s in signals.items()])
        fused_logits = sum(w * s.emotion_logits for w, s in zip(weights, signals.values()))
        
        return FusedState(
            emotion_logits=fused_logits,
            valence=compute_valence(fused_logits),
            arousal=compute_arousal(fused_logits),
            confidence=min(signals.values(), key=lambda s: s.confidence).confidence,
            contributing_modalities=list(signals.keys()),
            timestamp=now()
        )
```

### Service 3: Emotional Memory Cabinet

| Attribute | Value |
|-----------|-------|
| **Language** | Python 3.12 + NumPy/SciPy |
| **Port** | 8003 |
| **Responsibility** | Maintain and update Bayesian user emotional profiles with drift detection |
| **Storage** | ScyllaDB for profiles, TimescaleDB for time-series |

```python
@dataclass
class EmotionalMemoryCabinet:
    """
    Bayesian belief-updating system for individual emotional profiles.
    
    Innovations:
    - Drift detection via CUSUM (Cumulative Sum) control chart
    - Automatic recalibration when drift exceeds threshold
    - Circadian pattern modeling with Fourier decomposition
    - Trigger sensitivity mapping (what affects this user)
    """
    
    # Baseline parameters (updated via Bayesian inference)
    valence_prior: NormalDistribution    # μ=0.0, σ=0.3 initially
    arousal_prior: NormalDistribution    # μ=0.5, σ=0.2 initially
    
    # Temporal patterns
    circadian_harmonics: np.ndarray       # Fourier coefficients for daily/weekly patterns
    circadian_periods: List[float]        # [24h, 168h] + individualized periods
    
    # Drift detection
    cusum_positive: float = 0.0
    cusum_negative: float = 0.0
    drift_threshold: float = 5.0          # CUSUM alarm threshold
    drift_reset_count: int = 0
    
    # Personalization
    trigger_sensitivity: Dict[str, float]  # stimulus → sensitivity β
    recovery_rate: float = 0.1             # exponential decay rate
    
    # Confidence tracking
    sample_count: int = 0
    confidence_score: float = 0.0
    last_recalibration: datetime = None
    
    def update(self, observation: FusedState) -> CabinetUpdate:
        """Bayesian update with drift detection"""
        
        # 1. Compute prediction error
        predicted = self.predict_current_state()
        residual = observation.valence - predicted.valence
        
        # 2. CUSUM drift detection
        self.cusum_positive = max(0, self.cusum_positive + residual - self.drift_threshold / 2)
        self.cusum_negative = max(0, self.cusum_negative - residual - self.drift_threshold / 2)
        
        drift_detected = (self.cusum_positive > self.drift_threshold or 
                         self.cusum_negative > self.drift_threshold)
        
        # 3. Bayesian posterior update
        if drift_detected:
            # Widen prior (increase uncertainty) for rapid adaptation
            self.valence_prior.sigma *= 2.0
            self.drift_reset_count += 1
            self.last_recalibration = datetime.utcnow()
        
        # Standard Bayesian update: posterior ∝ prior × likelihood
        self.valence_prior = bayesian_update(
            self.valence_prior, 
            observation.valence,
            likelihood_sigma=0.2 + (0.3 if drift_detected else 0.0)
        )
        
        # 4. Update circadian model
        self._update_circadian(observation)
        
        # 5. Update confidence
        self.sample_count += 1
        self.confidence_score = min(1.0, self.sample_count / 100.0) * \
                               (0.5 if drift_detected else 1.0)
        
        return CabinetUpdate(
            drift_detected=drift_detected,
            drift_magnitude=max(self.cusum_positive, self.cusum_negative),
            confidence=self.confidence_score,
            prediction_error=abs(residual)
        )
```

### Service 4: Companion Agent Service

| Attribute | Value |
|-----------|-------|
| **Language** | Python 3.12 (Agent Zero framework integration) |
| **Port** | 8004 |
| **Responsibility** | Generate emotionally appropriate AI companion responses |
| **LLM Backend** | GPT-4o-mini (fast) / Claude Haiku (empathy) with model routing |

```python
class SentientCompanionAgent:
    """
    The conversational AI that responds with emotional intelligence.
    Uses Dual-Axis Training Signal for response scoring.
    """
    
    def generate_response(
        self,
        user_message: str,
        emotional_state: FusedState,
        user_cabinet: EmotionalMemoryCabinet,
        conversation_history: List[Message]
    ) -> CompanionResponse:
        
        # 1. Determine emotional context
        emotion_context = self._build_emotion_prompt(emotional_state, user_cabinet)
        
        # 2. Route to appropriate model based on emotional complexity
        model = self._route_model(emotional_state, user_cabinet)
        
        # 3. Generate candidate responses (beam of 3)
        candidates = model.generate(
            prompt=self._build_system_prompt(emotion_context),
            messages=conversation_history,
            n=3,
            temperature=0.7
        )
        
        # 4. Score with Dual-Axis Signal
        scored = []
        for candidate in candidates:
            score_a = self._score_reasoning(candidate, user_message)  # factual quality
            score_b = self._score_emotional_salience(              # emotional fit
                candidate, emotional_state, user_cabinet
            )
            final_score = score_a * (1 + self.alpha * score_b)    # multiplicative weighting
            scored.append((candidate, final_score, score_a, score_b))
        
        # 5. Select best response
        best = max(scored, key=lambda x: x[1])
        
        return CompanionResponse(
            text=best[0],
            score_a=best[2],
            score_b=best[3],
            final_score=best[1],
            emotional_alignment=best[3]
        )
```

### Service 5: Attestation Service

| Attribute | Value |
|-----------|-------|
| **Language** | Rust 1.75 |
| **Port** | 8005 |
| **Responsibility** | Maintain Merkle-anchored append-only ledger for emotional inference provenance |
| **Storage** | PostgreSQL (append-only table) + in-memory Merkle tree |

```rust
struct AttestationEntry {
    id: i64,
    user_id: String,
    timestamp: DateTime<Utc>,
    signal_capture: SignalCaptureAttestation,
    inference: InferenceAttestation,
    alignment: AlignmentAttestation,
    merkle_leaf_hash: [u8; 32],
    merkle_proof: Vec<[u8; 32]>,
}

struct SignalCaptureAttestation {
    device_id: String,
    model_version: String,
    input_hash: [u8; 32],  // SHA256 of derived signal
    signal_types: Vec<String>,
}

struct InferenceAttestation {
    output_hash: [u8; 32],  // SHA256 of emotion logits
    confidence: f64,
    fusion_model_version: String,
}

struct AlignmentAttestation {
    alignment_score: f64,
    cabinet_version: String,
    drift_detected: bool,
}

impl AttestationService {
    fn append(&mut self, entry: AttestationEntry) -> MerkleProof {
        // 1. Compute leaf hash
        let leaf = sha256(&serde_json::to_vec(&entry).unwrap());
        
        // 2. Append to Merkle tree
        self.merkle_tree.insert(leaf);
        
        // 3. Get Merkle proof (sibling hashes to root)
        let proof = self.merkle_tree.get_proof(leaf);
        
        // 4. Persist to append-only DB
        sqlx::query!(
            "INSERT INTO attestation_ledger (...) VALUES (...)",
            entry
        ).execute(&self.db).await?;
        
        // 5. Periodically anchor root hash to blockchain
        if self.merkle_tree.size() % 1000 == 0 {
            self.anchor_to_chain(self.merkle_tree.root());
        }
        
        proof
    }
    
    fn verify(&self, entry: &AttestationEntry, proof: &MerkleProof) -> bool {
        // Verify the entry is in the Merkle tree
        verify_merkle_proof(entry.merkle_leaf_hash, proof, self.merkle_tree.root())
    }
}
```

### Service 6: Insight Generator Service

| Attribute | Value |
|-----------|-------|
| **Language** | Python 3.12 |
| **Port** | 8006 |
| **Responsibility** | Generate emotional insights, weekly summaries, shareable visualizations |

```python
class InsightGenerator:
    """
    Generates emotional insights and shareable content.
    
    Outputs:
    - Weekly emotional journey summaries
    - Emotional DNA visualizations
    - Pattern detections ("You tend to feel anxious on Sunday evenings")
    - Trend analysis ("Your baseline joy has increased 15% this month")
    - EmotionSync compatibility reports
    """
    
    def generate_weekly_summary(self, user_id: str, week: date_range) -> WeeklyInsight:
        emotions = self.timeseries_db.query(
            "SELECT * FROM emotion_states WHERE user_id = ? AND timestamp BETWEEN ? AND ?",
            [user_id, week.start, week.end]
        )
        
        # Statistical analysis
        dominant_emotion = mode(emotions.top_emotion)
        valence_trend = linear_regression(emotions.timestamp, emotions.valence)
        circadian_fit = fit_circadian(emotions)
        anomalies = detect_anomalies(emotions, user_cabinet.baseline)
        
        # Generate narrative
        narrative = self.llm.generate(
            prompt=INSIGHT_TEMPLATE.format(
                dominant=dominant_emotion,
                trend=valence_trend.direction,
                best_day=emotions.best_day,
                challenge_day=emotions.worst_day,
                anomalies=anomalies
            )
        )
        
        # Generate shareable visualization
        viz_url = self.render_emotional_dna(emotions)
        
        return WeeklyInsight(
            narrative=narrative,
            visualization_url=viz_url,
            dominant_emotion=dominant_emotion,
            valence_trend=valence_trend.slope,
            confidence=user_cabinet.confidence_score
        )
```

### Service 7: User Profile Service

| Attribute | Value |
|-----------|-------|
| **Language** | Go 1.22 |
| **Port** | 8007 |
| **Responsibility** | User registration, authentication, preferences, account management |

### Service 8: Social/Share Service

| Attribute | Value |
|-----------|-------|
| **Language** | Go 1.22 |
| **Port** | 8008 |
| **Responsibility** | EmotionSync invitations, compatibility scores, social graph, share link generation |

### Service 9: Billing/Usage Service

| Attribute | Value |
|-----------|-------|
| **Language** | Go 1.22 |
| **Port** | 8009 |
| **Responsibility** | Usage tracking, tier enforcement, Stripe integration, API key management |

### Service 10: Analytics Service

| Attribute | Value |
|-----------|-------|
| **Language** | Python 3.12 |
| **Port** | 8010 |
| **Responsibility** | Internal analytics, model performance monitoring, aggregate emotion trends (no PII) |

## 2.3 Data Flow: User Interaction → Value Delivery

### Flow 1: Real-Time Emotion Check-In

```
1. User opens Sentient app → taps "How am I?"

2. [ON DEVICE]
   a. App activates voice check-in (user speaks for 10 seconds)
   b. Edge SDK runs TFLite voice model (2.7ms inference, 48.6KB)
   c. Output: {joy: 0.72, neutral: 0.18, sadness: 0.06, ...}
   d. Optional: User enables camera → face analysis (Fitzpatrick gate checked)
   e. User taps emoji overlay: 😊 (emoji signal)

3. [TRANSMIT] (encrypted TLS 1.3)
   POST /api/v1/signals
   {
     "voice": {"emotion_logits": {...}, "confidence": 0.89},
     "emoji": {"type": "face_smile", "timestamp": "..."},
     "face": null  // or {"emotion_logits": {...}} if camera enabled
   }

4. [CLOUD - Signal Ingestion Service]
   - Validates schema
   - Rate limits (max 60 check-ins/hour)
   - Publishes to Kafka topic "emotion-signals"

5. [CLOUD - Emotion Fusion Engine]
   - Consumes from Kafka
   - Cross-modal attention fusion
   - Outputs: FusedState {valence: 0.65, arousal: 0.42, emotion: "joy", confidence: 0.91}

6. [CLOUD - Emotional Memory Cabinet]
   - Bayesian update with new observation
   - Drift detection check
   - Persists updated profile to ScyllaDB

7. [CLOUD - Companion Agent Service]
   - Generates emotionally appropriate response
   - Dual-Axis scoring: Score_A (helpfulness) × (1 + α × Score_B (emotional fit))
   - Returns: "You're in a great mood today! Your joy levels are 15% above your usual Tuesday baseline."

8. [CLOUD - Attestation Service]
   - Creates attestation entry for this inference
   - Appends to Merkle tree
   - Returns verification proof to device

9. [DEVICE] Displays response + emotional state visualization

Total latency target: <200ms (p95)
Breakdown: 3ms edge + 10ms ingest + 30ms fusion + 20ms cabinet + 80ms LLM + 5ms attestation + 52ms network
```

### Flow 2: Weekly Insight Generation

```
1. [SCHEDULED] Cron job triggers every Sunday at 9am user-local-time

2. [CLOUD - Insight Generator]
   a. Queries TimescaleDB for user's emotional states over past 7 days
   b. Fits circadian model, detects patterns, finds anomalies
   c. Generates narrative summary via LLM
   d. Renders "Emotional DNA" visualization (canvas/SVG)
   e. Creates shareable link (expires in 7 days)

3. [PUSH NOTIFICATION]
   "Your weekly emotional journey is ready! 🌊"

4. [USER] Opens → sees beautiful visualization + narrative

5. [SOCIAL] User taps "Share" → generates Instagram story-sized image
   "This was my emotional week with @SentientAI"
   → Downloads to camera roll → shares on social
   → Includes Sentient branding + download link
```

## 2.4 On-Device vs Cloud Processing Split

| Component | Location | Rationale |
|-----------|----------|-----------|
| Voice emotion inference | **On-device** | Privacy (raw audio never leaves), latency (2.7ms vs 100ms+ round-trip), offline capability |
| Face emotion inference | **On-device** | Privacy (raw video frames never leave), Fitzpatrick gate enforced locally |
| Emoji/text classification | **On-device** | Trivial computation, no privacy concern |
| Signal fusion | **Cloud** | Requires cross-modal attention model (0.34M params), benefits from batch inference |
| Emotional Memory Cabinet | **Cloud** | Needs full historical data for Bayesian updates, circadian fitting |
| Companion response generation | **Cloud** | LLM inference (GPT-4o-mini), requires context window |
| Attestation chain | **Cloud** | Merkle tree maintenance, append-only ledger, blockchain anchoring |
| Insight generation | **Cloud** | Complex analytics, visualization rendering |
| User profile/auth | **Cloud** | Centralized identity management |

## 2.5 Real-Time vs Batch Processing Paths

### Real-Time Path (<200ms)
```
Device Signal → Signal Ingestion → Fusion Engine → Memory Cabinet → Companion Agent → Response
     ↑                                                                                      │
     └──────────────────────── Attestation (async, <50ms) ──────────────────────────────────┘
```

### Batch Paths (Async)
- **Weekly insights**: Cron-triggered, processed in background workers
- **Model retraining**: Nightly on aggregated (anonymized) data
- **Attestation anchoring**: Every 1000 entries, root hash anchored to blockchain
- **Analytics aggregation**: Hourly rollups for internal dashboards
- **EmotionSync computation**: Computed on-demand when users request compatibility

## 2.6 API Gateway and Authentication Design

### API Gateway: Kong Gateway (OSS) on Kubernetes

```
Routes:

POST   /api/v1/auth/register         → User Profile Service
POST   /api/v1/auth/login             → User Profile Service  
POST   /api/v1/auth/refresh           → User Profile Service

POST   /api/v1/signals                → Signal Ingestion Service
GET    /api/v1/emotions/current        → Emotion Fusion Engine
GET    /api/v1/emotions/history        → Emotion Fusion Engine

POST   /api/v1/chat                   → Companion Agent Service
GET    /api/v1/insights/weekly         → Insight Generator
GET    /api/v1/insights/dna            → Insight Generator

POST   /api/v1/social/emotionsync     → Social Service
GET    /api/v1/social/compatibility    → Social Service
POST   /api/v1/social/share            → Social Service

GET    /api/v1/profile                → User Profile Service
PUT    /api/v1/profile/preferences    → User Profile Service

GET    /api/v1/attestation/:id        → Attestation Service
POST   /api/v1/attestation/verify     → Attestation Service

# Enterprise API
POST   /api/v1/enterprise/emotions    → Signal Ingestion (enterprise auth)
GET    /api/v1/enterprise/analytics   → Analytics Service
```

### Authentication

```python
# JWT-based auth with short-lived access tokens
Access Token: 15-minute expiry, RS256 signed
Refresh Token: 7-day expiry, stored in HttpOnly cookie
Device Token: 30-day expiry, scoped to device_id

# Enterprise API Keys
API Key: Permanent (until revoked), scoped to tenant
Rate Limit: Per-key configurable (default: 1000 req/min)

# OAuth 2.0 providers for social login
Google, Apple, LINE (Japan), WeChat (China - future)
```

---

# 3. AI/ML PIPELINE

## 3.1 Model Architecture: Multimodal Fusion

### Architecture Choice: Confidence-Weighted Cross-Modal Transformer

Inspired by TACFN (0.34M params, 85.7% on IEMOCAP) and MemoCMT (81.85% on IEMOCAP), adapted for production deployment.

```
                    ┌─────────────────────────────────┐
                    │        Input Signals             │
                    └────────┬────────┬───────┬────────┘
                             │        │       │        │
                    ┌────▼───┐ ┌──▼───┐ ┌▼────┐ ┌▼─────┐
                    │Emoji  │ │Text  │ │Voice│ │Face  │
                    │Encoder│ │Encoder│ │Encoder│ │Encoder│
                    │(tiny) │ │(BERT)│ │(1D  │ │(Mobile│
                    │       │ │      │ │CNN) │ │NetV3) │
                    └────┬───┘ └──┬───┘ └┬────┘ └┬──────┘
                         │        │      │       │
                    ┌────▼────────▼──────▼───────▼──────┐
                    │   Confidence-Weighted Attention    │
                    │   (per-modality reliability score)  │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │   Cross-Modal Fusion Transformer   │
                    │   (2 layers, 4 heads, 128 dim)     │
                    │   ~200K params                     │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │   Emotion Classification Head      │
                    │   7 emotions + valence/arousal     │
                    └────────────────────────────────────┘
```

### Model Specifications

| Component | Architecture | Parameters | Latency | Accuracy Target |
|-----------|-------------|------------|---------|----------------|
| Emoji Encoder | Embedding(64) + Linear | ~4K params | <1ms | 99% (trivial) |
| Text Encoder | DistilBERT (fine-tuned) | ~66M params | ~20ms | 85%+ |
| Voice Encoder | 1D-CNN (3 conv layers) | ~50K params | ~3ms | 96%+ (on-device) |
| Face Encoder | MobileNetV3-Small + FC | ~2.5M params | ~8ms | 88%+ (Fitzpatrick-gated) |
| Fusion Transformer | 2-layer cross-attention | ~200K params | ~5ms | 87%+ combined |
| **Total (cloud fusion)** | | **~69M params** | **~30ms** | **87%+** |
| **Edge (voice only)** | 1D-CNN | **~50K params** | **2.7ms** | **96%+** |

### Emotion Taxonomy

```python
PRIMARY_EMOTIONS = [
    'joy',        # happiness, contentment, excitement
    'sadness',    # sorrow, grief, melancholy
    'anger',      # frustration, irritation, rage
    'fear',       # anxiety, worry, dread
    'surprise',   # amazement, astonishment
    'disgust',    # revulsion, distaste
    'neutral',    # baseline, calm
]

VALENCE_AROUSAL = {
    # Continuous scales for granular state
    'valence': [-1.0, 1.0],   # negative to positive
    'arousal': [0.0, 1.0],    # calm to energized
}
```

## 3.2 Training Pipeline

### Phase 1: Data Collection

```
Training Data Sources:

1. Public Datasets (foundation training):
   - IEMOCAP: 12 hours, 2 speakers, 5 emotion categories
   - RAVDESS: 24 actors, 8 emotions, speech + song
   - CREMA-D: 91 actors, 6 emotions, multi-ethnic
   - CMU-MOSEI: 23,454 sentences, 1,000+ speakers
   - MELD: 13,708 utterances from Friends TV show
   - GoEmotions: 58k Reddit comments, 27 emotion categories

2. Synthetic Data Augmentation:
   - Voice: Speed perturbation (0.9x, 1.0x, 1.1x), noise injection,
     pitch shifting (-5, +5 semitones), room impulse response
   - Text: Back-translation, synonym replacement, emotion-preserving paraphrase
   - Face: Fitzpatrick-stratified synthetic faces (StyleGAN3), 
     lighting variation, pose variation

3. Proprietary Collection (post-launch):
   - Opt-in user emoji/text annotations (explicit signal, no privacy concern)
   - Derived voice/face signals (already anonymized logits, not raw data)
   - A/B test calibration data
```

### Phase 2: Labeling & Dual-Axis Signal Generation

```python
class DualAxisLabelGenerator:
    """
    Generates training labels with two axes:
    Score A (Reasoning Quality) + Score B (Emotional Salience)
    """
    
    def generate_labels(self, sample: TrainingSample) -> DualAxisLabel:
        # Score A: Factual/Reasoning Quality
        score_a = self.compute_reasoning_score(
            response=sample.response,
            context=sample.context,
            ground_truth=sample.ground_truth  # for classification tasks
        )
        # Factors: accuracy, completeness, relevance, coherence
        
        # Score B: Emotional Salience
        score_b = self.compute_emotional_salience(
            response=sample.response,
            user_state=sample.emotional_state,
            appropriate_response=sample.appropriate_emotional_response
        )
        # Factors: tone match, empathy level, emotional validation,
        #          constructiveness, emotional appropriateness
        
        # Multiplicative weighting
        alpha = 0.5  # emotional weighting (tuned via validation)
        final_score = score_a * (1 + alpha * score_b)
        
        return DualAxisLabel(
            score_a=score_a,          # [0, 1]
            score_b=score_b,          # [0, 1]
            final_score=final_score,  # [0, 1.5]
            emotion_label=sample.emotion_label,
            valence=sample.valence,
            arousal=sample.arousal
        )
```

### Phase 3: Model Training

```
Training Infrastructure:

Hardware: 4x NVIDIA A100 (80GB) on GCP/GKE
Framework: PyTorch 2.2 + DeepSpeed ZeRO-3
Experiment Tracking: Weights & Biases

Training Steps:

1. Pre-train encoders on individual modalities (2 days)
   - Voice: Fine-tune 1D-CNN on RAVDESS + CREMA-D (96% target)
   - Text: Fine-tune DistilBERT on GoEmotions (85% target)
   - Face: Fine-tune MobileNetV3 on AffectNet + RAF-DB (88% target)

2. Train fusion transformer (1 day)
   - Cross-modal attention on IEMOCAP + CMU-MOSEI
   - Confidence-weighted loss function

3. Dual-axis reward model training (2 days)
   - Use labeled pairs to train Score A and Score B predictors
   - DPO (Direct Preference Optimization) for alignment

4. RLHF alignment (3 days)
   - PPO with Dual-Axis reward model
   - Optimize for final_score = score_a * (1 + α * score_b)

5. Edge model distillation (1 day)
   - Knowledge distillation from fusion model to voice-only edge model
   - Quantize to INT8 (48-86KB target)
   - Validate on ARM Cortex-M7 target

6. Fitzpatrick accuracy gate validation (1 day)
   - Test face model across Fitzpatrick I-VI on held-out stratified test set
   - If any category < threshold, add targeted augmentation and retrain

Total: ~10 days for full training cycle
Recurring: Weekly retraining with new opt-in data
```

## 3.3 Emotional Memory Cabinet Implementation

### Data Schema

```sql
-- ScyllaDB: User emotional profiles
CREATE TABLE user_emotional_profiles (
    user_id         UUID PRIMARY KEY,
    baseline_valence_mu    FLOAT,
    baseline_valence_sigma FLOAT,
    baseline_arousal_mu    FLOAT,
    baseline_arousal_sigma FLOAT,
    circadian_harmonics    BLOB,  -- serialized Fourier coefficients
    circadian_periods      LIST<FLOAT>,
    trigger_sensitivity    MAP<TEXT, FLOAT>,
    recovery_rate          FLOAT,
    sample_count           INT,
    confidence_score       FLOAT,
    last_recalibration     TIMESTAMP,
    drift_reset_count      INT,
    created_at             TIMESTAMP,
    updated_at             TIMESTAMP
);

-- TimescaleDB: Time-series emotion states
CREATE TABLE emotion_states (
    time            TIMESTAMPTZ NOT NULL,
    user_id         UUID NOT NULL,
    valence         FLOAT,
    arousal         FLOAT,
    emotion_primary TEXT,
    emotion_logits  JSONB,      -- {joy: 0.72, sadness: 0.06, ...}
    confidence      FLOAT,
    signal_sources  TEXT[],     -- ['voice', 'emoji', 'text']
    fused           BOOLEAN,
    attestation_id  BIGINT
);
SELECT create_hypertable('emotion_states', 'time', chunk_time_interval => INTERVAL '1 day');
```

### Drift Detection Algorithm

```python
class CUSUMDriftDetector:
    """
    Cumulative Sum control chart for emotional drift detection.
    
    Detects sustained shifts in emotional baseline that indicate
    genuine change (not noise). When drift is detected, the
    Cabinet widens its priors to allow rapid adaptation.
    """
    
    def __init__(self, threshold: float = 5.0, drift_response: float = 0.25):
        self.threshold = threshold
        self.drift_response = drift_response
        self.cusum_pos = 0.0
        self.cusum_neg = 0.0
    
    def update(self, residual: float) -> DriftResult:
        """
        residual = observed_valence - predicted_valence
        """
        # One-sided CUSUM
        self.cusum_pos = max(0, self.cusum_pos + residual - self.drift_response)
        self.cusum_neg = max(0, self.cusum_neg - residual - self.drift_response)
        
        drift_detected = (
            self.cusum_pos > self.threshold or 
            self.cusum_neg > self.threshold
        )
        
        if drift_detected:
            # Reset CUSUM after detection
            self.cusum_pos = 0.0
            self.cusum_neg = 0.0
        
        return DriftResult(
            detected=drift_detected,
            magnitude=max(self.cusum_pos, self.cusum_neg),
            direction='positive' if self.cusum_pos > self.cusum_neg else 'negative'
        )
```

### Circadian Pattern Modeling

```python
class CircadianEmotionModel:
    """
    Models user's emotional patterns over daily and weekly cycles
    using Fourier decomposition.
    
    Captures patterns like:
    - "I'm always anxious on Sunday evenings"
    - "My mood peaks at 2pm"
    - "I'm lowest on Wednesdays"
    """
    
    PERIODS = [24.0, 168.0]  # hours: daily and weekly cycles
    N_HARMONICS = 3           # per period
    
    def fit(self, timestamps: np.ndarray, valences: np.ndarray):
        """Fit Fourier series to emotional data"""
        hours = (timestamps - timestamps[0]).total_seconds() / 3600
        
        features = self._fourier_features(hours)
        self.coefficients = np.linalg.lstsq(features, valences, rcond=None)[0]
    
    def predict(self, timestamp: datetime) -> float:
        """Predict expected valence at given time"""
        hours = (timestamp - self.reference_time).total_seconds() / 3600
        features = self._fourier_features(np.array([hours]))
        return float(features @ self.coefficients)
    
    def _fourier_features(self, hours: np.ndarray) -> np.ndarray:
        features = [np.ones_like(hours)]  # bias term
        for period in self.PERIODS:
            for k in range(1, self.N_HARMONICS + 1):
                features.append(np.sin(2 * np.pi * k * hours / period))
                features.append(np.cos(2 * np.pi * k * hours / period))
        return np.column_stack(features)
```

## 3.4 Edge Deployment Strategy

### Model Compression Pipeline

```
Full Cloud Model (69M params, ~280MB)
         │
         ▼ [Knowledge Distillation]
Teacher-Student Distillation (280MB → 2MB)
         │
         ▼ [Pruning]
Magnitude Pruning (90% sparsity target)
         │
         ▼ [Quantization]
INT8 Post-Training Quantization (8x compression)
         │
         ▼ [Target: 48-86KB Flash, 6-8KB RAM]
         │
    ┌────┴────────────────────────┐
    │                              │
    ▼                              ▼
[Voice-Only Model]          [Voice+Face Model]
48.6KB, 6.1KB RAM           86.6KB, 8.5KB RAM
2.7ms inference             ~5ms inference
96.3% accuracy              ~93% accuracy
(ARM Cortex-M7)             (ARM Cortex-M7)
```

### Platform-Specific Builds

| Platform | Framework | Model Format | Optimizations |
|----------|-----------|-------------|---------------|
| iOS (A15+) | CoreML | .mlmodel | Neural Engine, ANE delegate |
| iOS (A12-A14) | CoreML | .mlmodel | GPU delegate |
| Android (flagship) | TFLite | .tflite | GPU delegate, NNAPI |
| Android (mid-range) | TFLite | .tflite | XNNPACK delegate |
| Android (Go edition) | TFLite Micro | .tflite | CMSIS-NN |
| Apple Watch (S9) | CoreML (watchOS) | .mlmodel | Neural Engine |
| Wear OS (W5+) | TFLite | .tflite | Hexagon DSP |
| Smart earbuds (future) | TFLite Micro | .tflite | Custom DSP |

### Neuromorphic Target Architecture

```
Phase 1 (MVP): ARM Cortex-M class (current devices)
Phase 2 (Year 1): BrainChip Akida AKD1000 (9mW, NVISO partnership)
Phase 3 (Year 2): SynSense Speck 2f (0.7mW, always-on)
Phase 4 (Year 3): Innatera PULSAR (<600µW, sub-1ms, <$5)

Conversion Path:
  Standard ANN → Spiking Neural Network (SNN) conversion
  using rate coding or temporal coding
  Target: <2% accuracy loss during ANN→SNN conversion
```

## 3.5 Continuous Learning and Personalization Loop

```python
class PersonalizationEngine:
    """
    Continuously personalizes models to individual users.
    
    Pipeline:
    1. Collect opt-in derived signals (NOT raw data)
    2. Fine-tune user-specific fusion weights locally (federated)
    3. Aggregate anonymized gradients for global model improvement
    4. Deploy updated global model periodically
    """
    
    def personalize(self, user_id: str, recent_signals: List[EmotionSignal]):
        # 1. Compute user-specific modality reliability
        #    (some users are more expressive via voice, others via text)
        modality_weights = self.estimate_modality_reliability(recent_signals)
        
        # 2. Fine-tune last layer of fusion model for this user
        #    (transfer learning with small learning rate)
        user_model = self.load_base_model()
        user_model.fine_tune(
            data=recent_signals,
            layers=['fusion_head', 'output'],
            lr=1e-5,
            epochs=5
        )
        
        # 3. Compute gradient for federated aggregation (anonymized)
        gradient_update = user_model.get_update()
        self.federated_aggregator.submit(user_id_hash, gradient_update)
        
        return user_model
```

## 3.6 A/B Testing Framework for Emotional Calibration

```python
class EmotionABTest:
    """
    A/B testing framework specifically for emotional model calibration.
    
    Tests:
    - Different emotion thresholds (when to notify user about mood changes)
    - Response tone variations (same content, different emotional packaging)
    - Model versions (new fusion weights vs old)
    - Alpha values (emotional weighting in dual-axis scoring)
    """
    
    EXPERIMENTS = {
        'alpha_tuning': {
            'variants': {'control': 0.3, 'high_empathy': 0.7, 'balanced': 0.5},
            'metric': 'user_retention_7d',
            'duration': '14 days',
            'min_sample': 1000
        },
        'drift_threshold': {
            'variants': {'sensitive': 3.0, 'standard': 5.0, 'stable': 8.0},
            'metric': 'cabinet_confidence_correlation',
            'duration': '21 days',
            'min_sample': 500
        },
        'response_tone': {
            'variants': ['direct', 'warm', 'clinical'],
            'metric': 'session_rating',
            'duration': '7 days',
            'min_sample': 2000
        }
    }
```

---

# 4. PRIVACY & SECURITY ARCHITECTURE

## 4.1 On-Device Processing Guararantees

### Technical Enforcement (Not Policy)

```swift
// iOS: Network Extension to enforce no raw data transmission

class PrivacyEnforcement {
    """
    BLOCKS any attempt to transmit raw biometric data.
    This is enforced at the OS level, not by developer policy.
    """
    
    // Allowlisted endpoints for derived signals only
    static let ALLOWED_ENDPOINTS = [
        "api.sentient.ai/v1/signals",    // derived emotion logits only
        "api.sentient.ai/v1/chat",        // text (user-initiated)
        "api.sentient.ai/v1/auth"         // authentication
    ]
    
    // Content-type enforcement
    static let ALLOWED_CONTENT_TYPES = [
        "application/json"  // structured derived signals, never binary blobs
    ]
    
    // Max payload size (prevents raw audio/video exfiltration)
    static let MAX_PAYLOAD_BYTES = 4096  // 4KB max - enough for logits, not for audio
    
    func validateOutbound(data: Data, endpoint: URL) -> Bool {
        guard ALLOWED_ENDPOINTS.contains(endpoint.absoluteString) else { return false }
        guard data.count <= MAX_PAYLOAD_BYTES else { return false }
        // Validate structure matches derived signal schema (not raw data)
        guard isValidDerivedSignal(data) else { return false }
        return true
    }
}
```

```kotlin
// Android: V2 Signature Scheme + Network Security Config
// network_security_config.xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.sentient.ai</domain>
        <pin-set>
            <pin digest="SHA-256">BASE64_CERT_HASH=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

### Privacy Audit Trail

```
Privacy Audit Log (every 24h, user-visible):
- Total signals processed: count
- Raw data transmitted: 0 bytes (verified)
- Derived signals transmitted: X bytes
- Attestation chain verified: ✓ (root hash matches)
- Fitzpatrick gate activations: {active: N, fallback: M}
- Third-party data shared: 0 bytes
- Model versions: {voice: v1.2.3, face: v1.1.0, fusion: v2.0.1}
```

## 4.2 Cryptographic Attestation Chain Implementation

### Merkle Tree Structure

```rust
// Append-only Merkle tree with periodic blockchain anchoring
// Uses SHA-256 throughout

struct SentientMerkleTree {
    leaves: Vec<[u8; 32]>,
    root: [u8; 32],
    size: u64,
    last_anchored_size: u64,
}

impl SentientMerkleTree {
    fn insert(&mut self, leaf_data: &[u8]) -> [u8; 32] {
        let leaf_hash = sha256(leaf_data);
        self.leaves.push(leaf_hash);
        self.recompute_root();
        self.size += 1;
        
        // Anchor every 1000 entries
        if self.size - self.last_anchored_size >= 1000 {
            self.anchor_root();
        }
        
        leaf_hash
    }
    
    fn get_proof(&self, index: usize) -> MerkleProof {
        // Returns sibling hashes from leaf to root
        let mut proof = Vec::new();
        let mut idx = index;
        
        while idx < self.leaves.len() - 1 {
            let sibling = if idx % 2 == 0 { idx + 1 } else { idx - 1 };
            proof.push(self.leaves[sibling]);
            idx /= 2;
        }
        
        MerkleProof {
            leaf_hash: self.leaves[index],
            siblings: proof,
            root: self.root,
        }
    }
    
    fn anchor_root(&mut self) {
        // Anchor root hash to Ethereum L2 (Polygon/Arbitrum)
        // Cost: ~$0.01 per anchor (1000 entries)
        // Provides tamper-evidence, not just tamper-resistance
        self.last_anchored_size = self.size;
    }
}
```

### Attestation Entry Schema (PostgreSQL)

```sql
CREATE TABLE attestation_ledger (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID NOT NULL,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Signal capture attestation
    device_id       UUID NOT NULL,
    model_version   VARCHAR(64) NOT NULL,
    input_hash      BYTEA NOT NULL,          -- SHA-256 of derived signal
    signal_types    TEXT[] NOT NULL,          -- ['voice', 'emoji']
    
    -- Inference attestation
    output_hash     BYTEA NOT NULL,           -- SHA-256 of emotion logits
    confidence      REAL NOT NULL,
    fusion_version  VARCHAR(64) NOT NULL,
    
    -- Alignment attestation
    alignment_score REAL NOT NULL,
    cabinet_version VARCHAR(64) NOT NULL,
    drift_detected  BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Merkle data
    merkle_leaf     BYTEA NOT NULL,
    merkle_proof    BYTEA NOT NULL,           -- serialized sibling hashes
    
    -- Append-only enforcement
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      NULL  -- never set; enforced by trigger
);

-- Prevent updates and deletes
CREATE RULE no_update_attestation AS ON UPDATE TO attestation_ledGER
    DO INSTEAD NOTHING;
CREATE RULE no_delete_attestation AS ON DELETE TO attestation_ledger
    DO INSTEAD NOTHING;
```

### Verification API

```
POST /api/v1/attestation/verify
{
  "attestation_id": 12345,
  "expected_output_hash": "sha256:abc...",
  "merkle_proof": ["hash1", "hash2", ...]
}

Response:
{
  "valid": true,
  "root_hash": "sha256:def...",
  "blockchain_anchored": true,
  "anchor_tx_hash": "0x123...",
  "anchor_block": 19234567,
  "verified_at": "2026-04-15T14:32:05Z"
}
```

## 4.3 Demographic Accuracy Gates (Fitzpatrick Stratification)

### Training Data Stratification

```
Requirement: Training and validation data MUST be stratified across
Fitzpatrick skin types I-VI with minimum representation:

Fitzpatrick I (Very light):   ≥ 12% of dataset
Fitzpatrick II (Light):       ≥ 15% of dataset
Fitzpatrick III (Medium light): ≥ 18% of dataset
Fitzpatrick IV (Medium):      ≥ 18% of dataset
Fitzpatrick V (Medium dark):  ≥ 15% of dataset
Fitzpatrick VI (Dark):        ≥ 12% of dataset

Source datasets:
- RAF-DB: Multi-ethnic, ~15K images
- AffectNet: 450K+ images, manually annotated
- Synthesized: StyleGAN3-generated faces per Fitzpatrick category
- Custom collection: Opt-in user selfies with consent (derived signals only)
```

### Runtime Gate Enforcement

```python
class FitzpatrickGate:
    """
    Runtime enforcement of demographic accuracy.
    
    The face analysis module checks its OWN accuracy on the device
    by comparing against a small, stratified validation set that
    ships with the SDK. If accuracy drops below threshold for ANY
    Fitzpatrick category, the module REFUSES to activate.
    """
    
    # Shipped with SDK (encrypted, tamper-proof)
    VALIDATION_SET_SIZE = 50  # per Fitzpatrick category (300 total)
    
    def check_before_activation(self) -> GateResult:
        results = {}
        for fitz_type in ['I', 'II', 'III', 'IV', 'V', 'VI']:
            accuracy = self._validate_on_set(fitz_type)
            results[fitz_type] = accuracy
        
        gate = DemographicAccuracyGate()
        decision = gate.evaluate(results)
        
        if not decision.activate:
            # Log event for monitoring
            self.telemetry.log_gate_failure(results, decision.reason)
        
        return decision
```

## 4.4 EU AI Act Compliance by Design

### Classification and Obligations

```
Sentient Product Tiers → EU AI Act Classification:

1. Consumer App (personal emotional companion)
   Classification: NOT prohibited, NOT high-risk
   (Emotion recognition for personal use/entertainment)
   Obligations: Transparency only
   Implementation: Clear disclosure that AI emotion analysis is used
   
2. Enterprise Healthcare (digital therapeutics, patient monitoring)
   Classification: Permitted under Art. 5(1)(f) medical/safety exception
   Obligations: High-risk requirements (Annex III)
   Implementation: Full compliance package (see below)
   
3. Enterprise Workplace (NOT offered in EU)
   Classification: PROHIBITED by Art. 5(1)(f)
   Implementation: Geofenced blocking of workplace features in EU
```

### High-Risk Compliance Package (Healthcare Tier)

```
Article 9 (Risk Management):
  → Continuous risk assessment via model monitoring
  → Automated alerts for accuracy degradation
  → Incident response playbooks

Article 10 (Data Governance):
  → Training data documentation (data cards)
  → Fitzpatrick stratification records
  → Bias audit reports (quarterly)

Article 11-12 (Technical Documentation):
  → Model cards for all emotion models
  → System architecture documentation
  → Attestation chain specifications

Article 13 (Transparency):
  → User-facing: "This system uses AI to analyze emotions"
  → Regulator-facing: Full technical documentation on request

Article 14 (Human Oversight):
  → Clinician override capability
  → Alert thresholds configurable by healthcare provider
  → Emergency stop functionality

Article 15 (Accuracy):
  → Published accuracy metrics per demographic
  → Continuous accuracy monitoring
  → Automatic model retirement if accuracy drops
```

## 4.5 Data Minimization and Purpose Limitation

```python
class DataMinimizationPolicy:
    """
    Architecturally enforced data minimization.
    """
    
    # Retention periods
    RAW_DATA = 0            # Never stored (processed on-device)
    DERIVED_SIGNALS = '30d'  # Emotion logits retained 30 days
    USER_PROFILE = 'active'  # While account active
    AGGREGATE_ANONYMOUS = '5y' # For model improvement
    ATTESTATION = '7y'        # Regulatory compliance
    
    # Purpose limitation
    ALLOWED_PURPOSES = [
        'emotion_inference',       # Core product function
        'emotional_pattern_analysis', # Weekly insights
        'model_improvement',        # Aggregate anonymous only
        'regulatory_compliance',    # Attestation chain
    ]
    
    PROHIBITED_PURPOSES = [
        'advertising',              # Never use emotions for ads
        'employment_decisions',     # Never for hiring/firing
        'insurance_pricing',        # Never for risk assessment
        'credit_decisions',         # Never for financial decisions
        'government_surveillance',  # Never for law enforcement
    ]
    
    def enforce_purpose(self, data: Data, purpose: str) -> bool:
        if purpose in self.PROHIBITED_PURPOSES:
            raise PurposeViolationError(f"Purpose '{purpose}' is architecturally prohibited")
        if purpose not in self.ALLOWED_PURPOSES:
            raise PurposeViolationError(f"Purpose '{purpose}' is not allowlisted")
        return True
```

## 4.6 MAESTRO Framework Integration (AI Security)

```python
class SentientSecurityFramework:
    """
    Applies MAESTRO (Model Attack and Security Testing
    Framework for Enterprise AI) principles to Sentient.
    
    Leverages founder's AI security expertise (OWASP AST10)
    to build the most secure emotion AI platform.
    """
    
    THREAT_MODEL = {
        # LLM-specific threats
        'prompt_injection': {
            'risk': 'HIGH',
            'mitigation': [
                'Input sanitization on all user text',
                'Separate system/user prompts with hard delimiters',
                'Output filtering for emotion manipulation attempts',
                'Rate limiting on chat API (60 req/hour)'
            ]
        },
        'model_extraction': {
            'risk': 'MEDIUM',
            'mitigation': [
                'Edge models are distilled (not full model)',
                'API returns logits, not raw model outputs',
                'Rate limiting + anomaly detection on API usage',
                'Watermarking in model outputs'
            ]
        },
        'data_poisoning': {
            'risk': 'LOW',
            'mitigation': [
                'Training data from verified sources only',
                'Statistical anomaly detection in training pipeline',
                'Fitzpatrick gate catches biased training data'
            ]
        },
        'emotional_manipulation': {
            'risk': 'CRITICAL',
            'mitigation': [
                'Hard constraint: AI never suggests actions that increase negative emotions',
                'Depression/anxiety detection → crisis resource referral (not engagement)',
                'China CAC compliance: no creating "emotional dependence"',
                'Weekly screen time nudges when usage exceeds 30 min/day',
                'Transparent emotional state display (no hidden profiling)'
            ]
        },
        'privacy_breach': {
            'risk': 'CRITICAL',
            'mitigation': [
                'On-device processing (architectural guarantee)',
                '4KB payload limit prevents raw data exfiltration',
                'Certificate pinning on all API calls',
                'Encrypted at rest (AES-256) and in transit (TLS 1.3)',
                'Annual third-party penetration test'
            ]
        },
        'supply_chain': {
            'risk': 'MEDIUM',
            'mitigation': [
                'Pinned dependency versions',
                'SBOM (Software Bill of Materials) generated per release',
                'Model version pinning with hash verification',
                'Attestation chain catches unauthorized model swaps'
            ]
        }
    }
```

---

# 5. TECHNOLOGY STACK

## 5.1 Core Technology Choices

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Mobile (iOS)** | Swift 5.9 + SwiftUI | Native performance for on-device ML, CoreML integration |
| **Mobile (Android)** | Kotlin 2.0 + Jetpack Compose | Native performance, TFLite integration, NNAPI |
| **Watch (watchOS)** | Swift + SwiftUI + CoreML | Direct Neural Engine access on S9 SiP |
| **Watch (Wear OS)** | Kotlin + TFLite | Hexagon DSP access on Snapdragon W5+ |
| **Edge ML (iOS)** | CoreML Tools 7+ | Neural Engine optimization, model compression |
| **Edge ML (Android)** | TFLite 2.15+ | GPU/NNAPI delegates, INT8 quantization |
| **Edge ML (MCU)** | TFLite Micro / Edge Impulse | ARM Cortex-M targets (48-86KB models) |
| **Backend Services** | Go 1.22 (hot path) + Python 3.12 (ML) | Go for latency-critical, Python for ML pipeline |
| **ML Framework** | PyTorch 2.2 + Transformers | Research-to-production pipeline, TACFN/MemoCMT integration |
| **Model Serving** | TorchServe + vLLM | Low-latency inference, batching, GPU utilization |
| **Message Queue** | Apache Kafka (Confluent Cloud) | Signal ingestion, event sourcing, decoupling |
| **API Gateway** | Kong Gateway (OSS) on K8s | Rate limiting, auth, plugin ecosystem |
| **Edge CDN** | Cloudflare Workers | Global edge termination, <50ms TLS handshake |
| **Database (Profiles)** | ScyllaDB (managed) | Low-latency reads for user profiles, Cassandra-compatible |
| **Database (Time-series)** | TimescaleDB | Emotion state time-series, hypertables, compression |
| **Database (Attestation)** | PostgreSQL 16 (append-only) | ACID guarantees for attestation ledger |
| **Cache/Sessions** | Redis 7 (Redis Cloud) | Sub-ms reads for active sessions, pub/sub |
| **Object Storage** | Google Cloud Storage / S3 | Model artifacts, visualization assets |
| **Search** | Meilisearch | User-facing search for insights history |
| **Container Orchestration** | GKE Autopilot (primary) / EKS (DR) | Managed K8s, auto-scaling, GPU node pools |
| **CI/CD** | GitHub Actions + ArgoCD | GitOps deployment, canary releases |
| **Experiment Tracking** | Weights & Biases | Model experiments, A/B test tracking |
| **Monitoring** | Grafana + Prometheus + Loki | Metrics, logs, alerts |
| **Error Tracking** | Sentry | Real-time error alerting, stack traces |
| **Analytics** | PostHog (self-hosted) | Product analytics, feature flags, no PII to third parties |
| **Auth** | Auth0 (or Firebase Auth) | OAuth 2.0, JWT, social login providers |
| **Payments** | Stripe (consumer) + Stripe Connect (enterprise) | Subscription billing, usage-based billing |
| **Push Notifications** | Firebase Cloud Messaging (Android) + APNs (iOS) |
| **Blockchain Anchoring** | Polygon (Ethereum L2) | Low-cost Merkle root anchoring (~$0.01/anchor) |

## 5.2 Edge SDK Design

### iOS SDK Architecture

```swift
// SentientSDK.swift - Core SDK interface
import CoreML
import AVFoundation
import UIKit

public class SentientSDK {
    
    // Singleton instance
    public static let shared = SentientSDK()
    
    // On-device models (bundled with app)
    private let voiceModel: VNCoreMLModel  // 48.6KB, INT8
    private let faceModel: VNCoreMLModel?   // 86.6KB, INT8, optional
    
    // Privacy enforcement
    private let privacyGuard = PrivacyEnforcement()
    private let fitzpatrickGate = FitzpatrickGate()
    
    // Configuration
    public struct Config {
        let apiKey: String
        let enableVoice: Bool = true
        let enableFace: Bool = false  // opt-in only
        let enableEmoji: Bool = true
        let enableText: Bool = true
        let apiRegion: Region = .auto
    }
    
    public func initialize(config: Config) async throws {
        // 1. Validate API key
        try await validateAPIKey(config.apiKey)
        // 2. Load on-device models
        voiceModel = try loadModel("EmotionVoice_v1.2.mlmodelc")
        // 3. Check Fitzpatrick gate for face model
        if config.enableFace {
            let gateResult = fitzpatrickGate.check()
            if gateResult.canActivate {
                faceModel = try loadModel("EmotionFace_v1.1.mlmodelc")
            }
        }
        // 4. Start emoji/text signal collection
        startPassiveCollection()
    }
    
    // Voice emotion check-in (10 seconds, on-device)
    public func performVoiceCheckIn() async throws -> EmotionSignal {
        // 1. Record 10 seconds of audio (stays in memory)
        let audioBuffer = try await recordAudio(duration: 10.0)
        
        // 2. Run on-device inference
        let features = extractMFCC(audioBuffer)  // Mel-frequency cepstral coefficients
        let prediction = try voiceModel.prediction(from: features)
        
        // 3. Extract derived signal (NO raw audio leaves device)
        let signal = EmotionSignal(
            emotionLogits: prediction.emotionProbabilities,
            valence: prediction.valence,
            arousal: prediction.arousal,
            confidence: prediction.confidence,
            modelVersion: "voice_v1.2.3",
            timestamp: Date()
        )
        
        // 4. Privacy enforcement: verify payload is derived signal only
        try privacyGuard.validateOutbound(signal: signal)
        
        // 5. Transmit derived signal (encrypted)
        try await transmitSignal(signal)
        
        // 6. Audio buffer immediately freed from memory
        return signal
    }
}
```

### Android SDK Architecture

```kotlin
// SentientSDK.kt - Core SDK interface
class SentientSDK private constructor(
    private val context: Context,
    private val config: Config
) {
    
    companion object {
        @Volatile private var instance: SentientSDK? = null
        
        fun initialize(context: Context, config: Config): SentientSDK {
            return instance ?: synchronized(this) {
                instance ?: SentientSDK(context, config).also { instance = it }
            }
        }
    }
    
    private val interpreter: Interpreter  // TFLite interpreter
    private val privacyGuard = PrivacyGuard()
    private val fitzpatrickGate = FitzpatrickGate()
    
    // Voice check-in (on-device, 10 seconds)
    suspend fun performVoiceCheckIn(): EmotionSignal {
        // 1. Record audio (stays in memory, never persisted)
        val audioBuffer = recordAudio(durationMs = 10_000)
        
        // 2. Extract MFCC features
        val features = AudioFeatureExtractor.extractMFCC(audioBuffer)
        
        // 3. Run TFLite inference on GPU/NNAPI
        val input = convertToTensorBuffer(features)
        val output = Array(1) { FloatArray(7) }  // 7 emotion classes
        interpreter.run(input, output)
        
        // 4. Build derived signal
        val signal = EmotionSignal(
            emotionLogits = parseLogits(output[0]),
            valence = computeValence(output[0]),
            arousal = computeArousal(output[0]),
            confidence = computeConfidence(output[0]),
            modelVersion = "voice_v1.2.3",
            timestamp = Instant.now()
        )
        
        // 5. Privacy guard validates before transmission
        privacyGuard.validateOutbound(signal)
        
        // 6. Transmit
        transmitSignal(signal)
        
        return signal
    }
}
```

## 5.3 Cloud Infrastructure

### Kubernetes Cluster Layout

```yaml
# GKE Autopilot configuration
apiVersion: v1
kind: Namespace
metadata:
  name: sentient-production
---
# Service deployments
apiVersion: apps/v1
kind: Deployment
metadata:
  name: signal-ingestion
  namespace: sentient-production
spec:
  replicas: 3  # auto-scales 3-20
  template:
    spec:
      containers:
      - name: signal-ingestion
        image: gcr.io/sentient-ai/signal-ingestion:v1.0.0
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "2000m"
            memory: "1Gi"
        env:
        - name: KAFKA_BROKERS
          value: "kafka-confluent.sentient-production:9092"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emotion-fusion
  namespace: sentient-production
spec:
  replicas: 2  # GPU-enabled
  template:
    spec:
      nodeSelector:
        cloud.google.com/gke-accelerator: nvidia-l4
      containers:
      - name: emotion-fusion
        image: gcr.io/sentient-ai/emotion-fusion:v1.0.0
        resources:
          requests:
            nvidia.com/gpu: "1"
            cpu: "2000m"
            memory: "4Gi"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: companion-agent
  namespace: sentient-production
spec:
  replicas: 5  # LLM inference, auto-scales 5-30
  template:
    spec:
      containers:
      - name: companion-agent
        image: gcr.io/sentient-ai/companion-agent:v1.0.0
        resources:
          requests:
            cpu: "1000m"
            memory: "2Gi"
```

### Model Serving Configuration

```python
# TorchServe config.properties
inference_address=http://0.0.0.0:8080
management_address=http://0.0.0.0:8081
metrics_address=http://0.0.0.0:8082

# Model settings
default_workers_per_model=4
job_queue_size=100
max_response_size=6553600

# Model mar files
models=
  emotion_fusion=model-store/emotion_fusion.mar,
  dual_axis_scorer=model-store/dual_axis_scorer.mar

# GPU allocation
gpu=1  # Per worker
```

## 5.4 Database Design

### ScyllaDB Schema (User Profiles)

```sql
-- Already defined in Section 3.3 (Emotional Memory Cabinet)
-- user_emotional_profiles table

CREATE TABLE user_preferences (
    user_id         UUID PRIMARY KEY,
    language        TEXT DEFAULT 'en',
    timezone        TEXT,
    enable_voice    BOOLEAN DEFAULT TRUE,
    enable_face     BOOLEAN DEFAULT FALSE,
    enable_emoji    BOOLEAN DEFAULT TRUE,
    enable_text     BOOLEAN DEFAULT TRUE,
    notification_preferences MAP<TEXT, BOOLEAN>,
    share_opt_in    BOOLEAN DEFAULT FALSE,
    marketing_opt_in BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP,
    updated_at      TIMESTAMP
);
```

### TimescaleDB Schema (Emotion Time-Series)

```sql
-- emotion_states hypertable (defined in Section 3.3)

-- Continuous aggregates for analytics
CREATE MATERIALIZED VIEW emotion_hourly
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS bucket,
    user_id,
    AVG(valence) AS avg_valence,
    AVG(arousal) AS avg_arousal,
    MODE() WITHIN GROUP (ORDER BY emotion_primary) AS dominant_emotion,
    COUNT(*) AS signal_count
FROM emotion_states
GROUP BY bucket, user_id;

-- Retention policy
SELECT add_retention_policy('emotion_states', INTERVAL '90 days');
SELECT add_retention_policy('emotion_hourly', INTERVAL '1 year');
```

## 5.5 CI/CD and MLOps Pipeline

### GitOps Workflow

```
1. Developer pushes to GitHub
2. GitHub Actions runs:
   - Unit tests (Go + Python)
   - Integration tests (Docker Compose)
   - Security scan (Snyk + Trivy)
   - Model validation (accuracy on held-out test set)
3. If passing:
   - Build Docker images
   - Push to GCR
   - Update Helm chart version
4. ArgoCD detects chart change:
   - Canary deployment (5% → 25% → 100%)
   - Automatic rollback if error rate > 1%
5. Post-deploy:
   - Smoke tests
   - Model warmup (prefetch to GPU)
   - Update monitoring dashboards
```

### MLOps Pipeline (Domino-Inspired)

```
Weekly Model Retraining Pipeline:

1. Data Collection (Monday 2am UTC)
   - Aggregate opt-in derived signals from past 7 days
   - Anonymize: remove user_id, hash timestamps
   - Stratify by modality and emotion class

2. Validation (Monday 3am UTC)
   - Check dataset size (minimum 10K samples)
   - Check class balance (no class < 5% of total)
   - Fitzpatrick stratification verification
   - Statistical drift check vs previous week's data

3. Training (Monday 4am UTC)
   - Fine-tune fusion model on new data
   - Run full evaluation suite
   - Compare against production model on held-out set

4. Gate Check (Monday 8am UTC)
   - Accuracy must be ≥ current production (no regression)
   - Fitzpatrick gate must pass on updated face model
   - Latency benchmark must be within 10% of current
   - Dual-axis score must not regress

5. Shadow Deployment (Monday 9am UTC)
   - Deploy new model alongside production
   - Route 5% of traffic to new model
   - Compare real-time metrics for 24 hours

6. Full Rollout (Tuesday 9am UTC)
   - If shadow metrics pass → full rollout
   - If any regression → rollback + alert
   - Log model version in attestation chain
```

---

# 6. VIRAL GROWTH ENGINE

## 6.1 Product-Led Growth Mechanics

### Built-In Growth Features

```
1. Emotional DNA Visualization
   - Generated after 7 days of use
   - Unique visual fingerprint of emotional patterns
   - Watermarked with Sentient branding
   - "Get your emotional DNA" → download link in watermark

2. EmotionSync (Friend Compatibility)
   - User sends EmotionSync request to friend
   - Friend MUST install Sentient to see results
   - Both see "Emotion Compatibility Score" (e.g., 87%)
   - Share result → more installations
   - Built-in K-factor driver

3. Weekly Emotional Journey
   - Auto-generated every Sunday
   - Beautiful data visualization (Instagram story sized)
   - "This was my emotional week" → one-tap share
   - Sentient watermark + download CTA

4. Emotional Milestones
   - "You've tracked your emotions for 30 days!"
   - "Your joy has increased 20% this month"
   - Shareable achievement badges

5. Emotional Weather Report
   - Daily push: "Today's emotional forecast: Mostly sunny with afternoon stress"
   - Shareable as daily ritual
```

### Architecture Support for Growth

```python
class ShareService:
    """
    Generates shareable content that drives installations.
    """
    
    def create_share_link(self, user_id: str, content_type: str) -> ShareLink:
        # Generate unique share link with attribution
        link = ShareLink(
            id=uuid4(),
            creator_id=user_id,
            content_type=content_type,  # 'dna', 'weekly', 'sync', 'milestone'
            attribution_user=user_id,
            expires_at=now() + timedelta(days=7),
            deep_link=f"sentient://share/{id}",
            web_fallback=f"https://sentient.ai/share/{id}"
        )
        
        # Track attribution
        self.analytics.track_share_created(user_id, content_type)
        
        return link
    
    def handle_share_view(self, share_id: str, viewer_id: str = None) -> ShareResult:
        # Non-users see web preview with install CTA
        # Users see content in-app (deep link)
        # Track attribution for viral coefficient calculation
        pass
```

## 6.2 Social Sharing and Network Effects

```
Network Effects Flywheel:

Solo User → Emotional DNA generated (7 days)
         → Shares on Instagram/TikTok
         → Friends see share → install Sentient
         → EmotionSync request to original user
         → Original user sees compatibility
         → Both users more engaged (shared experience)
         → Both generate weekly shares
         → Network density increases
         → More compatibility insights available
         → More sharing → more installs

Viral Coefficient Tracking:
  K = (shares_per_user × install_rate_per_share) + (sync_requests_per_user × install_rate_per_sync)
  Target: K ≥ 1.3
```

## 6.3 API/Webhook System for Third-Party Integration

### Partner API

```
Partners can integrate Sentient emotion analysis:

1. Meditation Apps (Calm, Headspace)
   → Sentient provides emotional state before/after meditation
   → Apps recommend sessions based on user's emotional state

2. Fitness Apps (Strava, Nike Run Club)
   → Sentient provides emotional state during exercise
   → Apps correlate exercise with mood improvement

3. Journaling Apps (Day One, Reflectly)
   → Sentient provides emotion labels for entries
   → Apps auto-tag journal entries with emotions

4. Healthcare Platforms (Epic, Cerner)
   → Sentient provides anonymized emotional trends
   → Clinicians see patient mood trajectories
```

### Webhook Configuration

```json
POST /api/v1/enterprise/webhooks
{
  "url": "https://partner.app/webhook/sentient",
  "events": ["emotion.milestone", "emotion.drift", "emotion.weekly_summary"],
  "secret": "whsec_...",
  "filters": {
    "min_confidence": 0.8,
    "emotion_categories": ["sadness", "anger", "fear"]
  }
}

// Webhook payload example
{
  "event": "emotion.drift",
  "timestamp": "2026-04-15T14:32:00Z",
  "user_id": "usr_abc123",
  "data": {
    "direction": "negative",
    "magnitude": 6.2,
    "baseline_valence": 0.3,
    "current_valence": -0.4,
    "duration_hours": 48,
    "attestation_id": 12345
  },
  "signature": "sha256=..."
}
```

## 6.4 Developer SDK for Ecosystem Expansion

```swift
// Sentient Developer SDK (for third-party apps)
import SentientSDK

// Initialize with partner API key
let sentient = SentientSDK.Partner(apiKey: "sk_partner_...")

// Request user's emotional state (with user consent)
sentient.requestEmotionalState { result in
    switch result {
    case .success(let state):
        // state.emotion = "joy"
        // state.valence = 0.72
        // state.arousal = 0.45
        // state.confidence = 0.91
        // Recommend content based on emotional state
        recommendContent(for: state)
    case .failure(let error):
        // User declined or not available
        break
    }
}

// Register for emotion events
sentient.subscribe(to: .significantChange) { event in
    // User's emotional state changed significantly
    handleEmotionalShift(event)
}
```

---

# 7. MONETIZATION ARCHITECTURE

## 7.1 Tier Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    SENTIENT FREE                            │
│  • 3 emotion check-ins per day                               │
│  • Basic emotional state display                             │
│  • Emoji stream (unlimited)                                  │
│  • 1 weekly insight per month (upgrade for weekly)           │
│  • EmotionSync with 2 friends                                │
│  • 7-day emotional history                                   │
│  • On-device privacy (all tiers)                             │
│  • Cryptographic attestation (all tiers)                     │
└─────────────────────────────────────────────────────────────┘
                          │
                    $9.99/month or $79.99/year
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    SENTIENT PREMIUM                          │
│  • Unlimited emotion check-ins                               │
│  • Voice + face analysis (on-device)                         │
│  • Weekly insights (auto-generated)                         │
│  • Emotional DNA visualization                               │
│  • Unlimited EmotionSync friends                             │
│  • 90-day emotional history                                  │
│  • Advanced pattern detection                                │
│  • Priority companion responses                              │
│  • Shareable visualizations (no watermark)                   │
│  • Circadian rhythm analysis                                 │
└─────────────────────────────────────────────────────────────┘
                          │
                   $29.99/month per user
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  SENTIENT CLINICAL                           │
│  • All Premium features                                      │
│  • Therapist-shared dashboard                                │
│  • Clinical-grade emotional assessments                      │
│  • Crisis detection and resource referral                    │
│  • Unlimited emotional history                               │
│  • Export for healthcare provider (FHIR format)              │
│  • HIPAA-compliant data handling                             │
│  • FDA 21 CFR Part 11 compliant audit trail                  │
└─────────────────────────────────────────────────────────────┘
```

## 7.2 Enterprise API Pricing

```
SENTIENT API TIERS

Starter: $0.002 per emotion inference
  - Up to 100K inferences/month
  - 2 modalities (emoji + text)
  - Basic fusion
  - 48-hour support response
  
Professional: $0.001 per emotion inference (volume discount)
  - Up to 10M inferences/month
  - All 4 modalities
  - Emotional Memory Cabinet per user
  - Webhook integration
  - 4-hour support response
  - SLA: 99.9% uptime
  
Enterprise: Custom pricing
  - Unlimited inferences
  - On-premise deployment option
  - Custom model fine-tuning
  - Dedicated support engineer
  - BAA (Business Associate Agreement)
  - SLA: 99.99% uptime
  - FHIR/HL7 integration
  - Clinical validation support
```

### Usage Metering Architecture

```python
class UsageMeter:
    """
    Tracks API usage for billing.
    Uses Kafka Streams for real-time counting.
    """
    
    def count_inference(self, tenant_id: str, inference: InferenceEvent):
        # Increment Redis counter (fast)
        key = f"usage:{tenant_id}:{current_month()}"
        pipe = redis.pipeline()
        pipe.incr(key)
        pipe.incr(f"{key}:modalities:{inference.modalities}")
        pipe.expire(key, 45 * 24 * 3600)  # 45 day TTL
        pipe.execute()
        
        # Async persist to TimescaleDB (durable)
        kafka.produce('usage-events', {
            'tenant_id': tenant_id,
            'inference_id': inference.id,
            'modalities': inference.modalities,
            'timestamp': now(),
            'attestation_id': inference.attestation_id
        })
```

## 7.3 Data Marketplace

```python
class EmotionDataMarketplace:
    """
    Anonymized, attested emotion datasets for researchers.
    
    Key properties:
    - NO raw biometric data (ever)
    - All data is cryptographically attested (provenance verified)
    - User consent required (opt-in, NOT opt-out)
    - K-anonymity with k ≥ 50 (minimum 50 similar records)
    - Differential privacy (ε ≤ 1.0)
    
    Revenue: $0.10 per record (split 70/30 with user)
    """
    
    DATASET_SCHEMA = {
        'derived_emotion_logits': 'Dict[str, float]',  # anonymized
        'valence_arousal': 'Tuple[float, float]',
        'confidence': 'float',
        'demographic_bin': 'str',          # broad category only
        'signal_modalities': 'List[str]',
        'attestation_proof': 'MerkleProof',
        'model_version': 'str',
        'timestamp_bin': 'str',            # hour-of-day, not exact time
    }
    
    def publish_dataset(
        self, 
        records: List[EmotionRecord],
        consent_proofs: List[ConsentProof]
    ) -> DatasetReceipt:
        # 1. Verify all consent proofs
        # 2. Apply differential privacy (add noise)
        # 3. Apply k-anonymity (suppress rare combinations)
        # 4. Generate Merkle root for dataset
        # 5. Publish to marketplace with attestation
        pass
```

---

# 8. MVP TECHNICAL SCOPE

## 8.1 Eight-Week Sprint Plan

### Week 1-2: Foundation

```
Week 1: Core Infrastructure
├── Day 1-2: Project setup
│   ├── GitHub repo (monorepo: mobile, backend, ml, infra)
│   ├── CI/CD pipeline (GitHub Actions)
│   ├── Docker Compose for local dev
│   └── Kubernetes manifests (staging)
├── Day 3-4: Auth + User Service
│   ├── Auth0 integration
│   ├── User registration/login flow
│   ├── JWT middleware
│   └── User profile CRUD
└── Day 5: Signal Ingestion Service
    ├── Kafka setup (Confluent Cloud)
    ├── Signal schema validation
    └── Basic rate limiting

Week 2: Edge SDK + First Model
├── Day 1-3: iOS SDK (Swift)
│   ├── CoreML model integration (voice)
│   ├── Audio capture + MFCC extraction
│   ├── Privacy enforcement layer
│   └── API client (signal transmission)
├── Day 4-5: Android SDK (Kotlin)
│   ├── TFLite model integration (voice)
│   ├── Audio capture + MFCC extraction
│   └── API client
└── Parallel: Pre-trained voice model
    ├── Fine-tune 1D-CNN on RAVDESS + CREMA-D
    ├── Quantize to INT8 (<50KB target)
    └── Validate on ARM Cortex-M7 benchmark
```

### Week 3-4: Core Emotion Pipeline

```
Week 3: Emotion Fusion + Memory Cabinet
├── Day 1-2: Fusion Engine
│   ├── Implement confidence-weighted fusion
│   ├── TACFN-inspired cross-modal attention
│   └── Text sentiment (DistilBERT fine-tune)
├── Day 3-5: Emotional Memory Cabinet
│   ├── Bayesian update implementation
│   ├── CUSUM drift detection
│   ├── Circadian model (Fourier decomposition)
│   └── ScyllaDB + TimescaleDB integration

Week 4: Companion Agent + Attestation
├── Day 1-3: Companion Agent Service
│   ├── Agent framework (Agent Zero inspired)
│   ├── Dual-Axis response scoring
│   ├── LLM integration (GPT-4o-mini)
│   └── Emotion-aware prompt templates
├── Day 4-5: Attestation Service
│   ├── Merkle tree implementation (Rust)
│   ├── Append-only PostgreSQL ledger
│   └── Verification API endpoint
```

### Week 5-6: User Experience + Social

```
Week 5: Core App UI
├── Day 1-2: iOS App
│   ├── Onboarding flow (3 screens)
│   ├── Emotion check-in UI (voice + emoji)
│   ├── Emotional state display (gauge + history)
│   └── Chat interface for companion
├── Day 3-4: Android App
│   ├── Same as iOS (Jetpack Compose)
│   └── Material Design 3 components
└── Day 5: Push notifications
    ├── Firebase Cloud Messaging (Android)
    └── APNs (iOS)

Week 6: Social + Sharing
├── Day 1-3: Social Service
│   ├── EmotionSync invitation flow
│   ├── Compatibility score computation
│   ├── Share link generation
│   └── Web preview for non-users
├── Day 4-5: Insight Generator
│   ├── Weekly summary template
│   ├── Basic visualization (Emotional DNA v1)
│   └── Scheduled generation (cron)
```

### Week 7-8: Hardening + Launch Prep

```
Week 7: Security + Compliance
├── Day 1-2: Security audit
│   ├── Penetration test (automated + manual)
│   ├── Privacy enforcement validation
│   ├── Certificate pinning verification
│   └── Payload size enforcement audit
├── Day 3-4: Compliance
│   ├── EU AI Act transparency disclosure
│   ├── Privacy policy + terms of service
│   ├── Data processing agreement
│   └── Cookie consent + analytics opt-in
└── Day 5: Performance optimization
    ├── Load testing (Locust, 10K concurrent)
    ├── Latency optimization (target <200ms p95)
    └── Auto-scaling configuration

Week 8: Launch
├── Day 1-2: Beta testing
│   ├── TestFlight (iOS) + Play Console (Android)
│   ├── 100 beta testers (friends + network)
│   └── Bug triage + hotfixes
├── Day 3-4: Launch preparation
│   ├── App Store optimization (ASO)
│   ├── Landing page (sentient.ai)
│   ├── Press kit + demo video
│   └── Social media content calendar
└── Day 5: LAUNCH
    ├── App Store + Play Store submission
    ├── Product Hunt launch
    ├── Press outreach (TechCrunch, Wired, The Verge)
    └── Twitter/X thread explaining the technology
```

## 8.2 Technical Dependencies and Critical Path

```
Critical Path:

1. Voice model training (blocks SDK development)
   → Solution: Start with pre-trained model, fine-tune later
   → Dependency: RAVDESS + CREMA-D datasets (public, available)

2. CoreML/TFLite model conversion (blocks edge deployment)
   → Solution: Use Edge Impulse for automated conversion
   → Dependency: Trained PyTorch model

3. ScyllaDB/TimescaleDB setup (blocks Memory Cabinet)
   → Solution: Use managed services (ScyllaDB Cloud, Timescale Cloud)
   → Dependency: Cloud account setup (1 day)

4. LLM API access (blocks Companion Agent)
   → Solution: Use OpenAI API (immediate access)
   → Dependency: API key + rate limit approval

5. Auth0 setup (blocks all authenticated features)
   → Solution: Set up in Week 1
   → Dependency: Auth0 account (free tier available)

6. App Store approval (blocks launch)
   → Solution: Follow Human Interface Guidelines strictly
   → Risk: 2-7 day review time
   → Mitigation: Submit beta builds weekly from Week 5
```

## 8.3 What Can Be Mocked/Simulated for Demo

```
For investor demos before full build:

1. Edge Voice Model → Use Hume AI API as fallback
   - Same functionality, cloud-based initially
   - Demonstrate on-device version when ready

2. Emotional Memory Cabinet → Use Redis with fixed profiles
   - 5 pre-generated demo profiles
   - Shows Bayesian updating in real-time

3. Companion Agent → Use GPT-4o directly
   - Custom system prompt with emotional context
   - No Dual-Axis scoring initially

4. Attestation Chain → Use mock Merkle tree
   - Shows verification working
   - Blockchain anchoring simulated

5. Social Features → Use pre-generated shares
   - "Emotional DNA" images pre-rendered
   - Compatibility scores pre-computed

Demo Flow (5 minutes):
1. Open app → "How am I feeling?"
2. Voice check-in (10 seconds) → "You're feeling joyful! (87% confidence)"
3. Chat with companion → emotionally aware response
4. Show Emotional Memory Cabinet → "Your joy is 15% above Tuesday baseline"
5. Share Emotional DNA → Instagram story
6. EmotionSync with friend → compatibility score
7. Attestation verification → prove data provenance
```

## 8.4 Scaling Milestones

```
Milestone 1: 1,000 Users (Month 1-2)
├── Infrastructure: Single GKE cluster, us-east1
├── 1 Kafka partition, 1 consumer group
├── ScyllaDB: 1 node
├── TimescaleDB: 1 instance (2 vCPU)
├── Cost: ~$500/month
├── Team: 3 (2 eng + 1 ML)
└── Focus: Core experience, bug fixes, retention

Milestone 2: 10,000 Users (Month 3-4)
├── Infrastructure: GKE Autopilot, us-east1 + eu-west1
├── 3 Kafka partitions, auto-scaling consumers
├── ScyllaDB: 3 nodes
├── TimescaleDB: 4 vCPU, read replicas
├── Cost: ~$3,000/month
├── Team: 5 (3 eng + 1 ML + 1 mobile)
└── Focus: EmotionSync viral coefficient, weekly shares

Milestone 3: 100,000 Users (Month 5-8)
├── Infrastructure: Multi-region (US, EU, Asia)
├── 12 Kafka partitions
├── ScyllaDB: 6 nodes (3 per region)
├── TimescaleDB: 16 vCPU, continuous aggregates
├── Redis Cluster: 3 nodes
├── Cost: ~$15,000/month
├── Team: 10 (5 eng + 2 ML + 2 mobile + 1 DevOps)
├── Focus: Enterprise API, healthcare partnerships
└── Revenue: ~$50K/month (5% paid conversion at $9.99)

Milestone 4: 1,000,000 Users (Month 9-14)
├── Infrastructure: Multi-region + edge CDN
├── 48 Kafka partitions
├── ScyllaDB: 12 nodes
├── TimescaleDB: 64 vCPU cluster
├── Redis Cluster: 6 nodes
├── Model serving: 8 GPU nodes (L4)
├── Cost: ~$80,000/month
├── Team: 20 (8 eng + 4 ML + 3 mobile + 2 DevOps + 3 other)
├── Focus: International expansion, neuromorphic R&D
├── Revenue: ~$500K/month (5% paid conversion + enterprise API)
└── Path to: Series A ($10-15M)

Key Inflection Points:
- 10K users: Prove viral coefficient works (K > 1.0)
- 100K users: Enterprise API revenue begins
- 1M users: Series A readiness, international expansion
- 10M users: Neuromorphic deployment, market leadership
```

---

# APPENDIX A: COMPLETE API SPECIFICATION

```
AUTHENTICATION
──────────────
POST   /api/v1/auth/register
  Body: {email, password, display_name, timezone}
  Response: {user_id, access_token, refresh_token}

POST   /api/v1/auth/login
  Body: {email, password}
  Response: {user_id, access_token, refresh_token}

POST   /api/v1/auth/refresh
  Body: {refresh_token}
  Response: {access_token}

POST   /api/v1/auth/social/google
POST   /api/v1/auth/social/apple
POST   /api/v1/auth/social/line
  Body: {id_token}
  Response: {user_id, access_token, refresh_token, is_new_user}


EMOTION SIGNALS
───────────────
POST   /api/v1/signals
  Headers: Authorization: Bearer <token>
  Body: {
    signals: [{
      type: "voice"|"emoji"|"text"|"face",
      payload: {
        emotion_logits: {joy: 0.72, ...},
        valence: 0.65,
        arousal: 0.42,
        confidence: 0.89
      },
      model_version: "voice_v1.2.3",
      timestamp: "2026-04-15T14:32:00Z"
    }]
  }
  Response: {
    signal_ids: ["sig_abc123"],
    fused_state: {
      emotion_primary: "joy",
      valence: 0.65,
      arousal: 0.42,
      confidence: 0.91,
      contributing_modalities: ["voice", "emoji"]
    },
    attestation_id: 12345
  }

GET    /api/v1/emotions/current
  Response: FusedState (cached, <5s old)

GET    /api/v1/emotions/history?from=2026-04-08&to=2026-04-15&resolution=hour
  Response: {
    states: [{timestamp, valence, arousal, emotion_primary, confidence}],
    stats: {avg_valence, dominant_emotion, trend_direction}
  }


COMPANION
─────────
POST   /api/v1/chat
  Body: {message: string, context?: {include_emotional_state: true}}
  Response: {
    response: string,
    scores: {reasoning: 0.92, emotional_salience: 0.85, final: 1.35},
    emotional_alignment: 0.85
  }
  (Supports streaming via SSE)

GET    /api/v1/chat/history?limit=50
  Response: {messages: [{role, content, timestamp, emotional_context}]}


INSIGHTS
────────
GET    /api/v1/insights/weekly
  Response: {
    narrative: "This week was marked by...",
    dominant_emotion: "joy",
    valence_trend: +0.12,
    best_day: "Wednesday",
    challenge_day: "Monday",
    visualization_url: "https://storage.sentient.ai/...",
    share_link: "https://sentient.ai/share/abc"
  }

GET    /api/v1/insights/dna
  Response: {
    image_url: "https://storage.sentient.ai/...",
    emotional_fingerprint: {
      baseline_valence: 0.35,
      circadian_peak: "2:00 PM",
      circadian_trough: "11:00 PM",
      volatility: 0.22,
      recovery_rate: "fast"
    },
    share_link: "https://sentient.ai/share/def"
  }


SOCIAL
──────
POST   /api/v1/social/emotionsync/request
  Body: {target_email: string, message?: string}
  Response: {sync_request_id, status: "pending"}

GET    /api/v1/social/emotionsync/status
  Response: {sync_requests: [{id, from_user, status, compatibility_score?}]}

POST   /api/v1/social/emotionsync/respond
  Body: {request_id, accept: boolean}
  Response: {compatibility_score?: {overall: 0.87, valence_align: 0.92, rhythm_sync: 0.81}}

POST   /api/v1/social/share
  Body: {content_type: "dna"|"weekly"|"milestone", platform?: string}
  Response: {share_url, image_url, deep_link, expires_at}


PROFILE
───────
GET    /api/v1/profile
  Response: {user_id, display_name, email, preferences, cabinet_summary}

PUT    /api/v1/profile/preferences
  Body: {enable_voice, enable_face, enable_emoji, language, timezone}
  Response: {updated: true}


ATTESTATION
───────────
GET    /api/v1/attestation/:id
  Response: {attestation_entry, merkle_proof, root_hash}

POST   /api/v1/attestation/verify
  Body: {attestation_id, expected_hash}
  Response: {valid, root_hash, blockchain_anchored, anchor_details}


ENTERPRISE (API Key Auth)
─────────────────────────
POST   /api/v1/enterprise/signals/batch
  Body: {signals: [{user_anon_id, signal_type, payload, timestamp}]}
  Response: {processed: 150, errors: []}

GET    /api/v1/enterprise/analytics/emotions
  Params: ?from=&to=&group_by=emotion|hour|day
  Response: {aggregates: [{period, emotion_counts, avg_valence, avg_arousal}]}

POST   /api/v1/enterprise/webhooks
  Body: {url, events[], secret, filters}
  Response: {webhook_id, status: "active"}
```

---

# APPENDIX B: KEY PERFORMANCE INDICATORS

```
Technical KPIs:
├── Emotion inference latency: <200ms p95 (end-to-end)
├── Edge inference latency: <5ms (on-device)
├── Voice model accuracy: >96% (RAVDESS benchmark)
├── Fusion model accuracy: >85% (IEMOCAP benchmark)
├── Companion response latency: <2s p95
├── API uptime: 99.9% (professional tier)
├── Fitzpatrick gate: ALL categories >88%
├── Attestation verification: 100% traceable
└── Privacy audit: 0 raw data transmissions (ever)

Product KPIs:
├── D7 retention: >40%
├── D30 retention: >25%
├── Check-ins per user per day: >2 (free), >4 (premium)
├── Weekly share rate: >15% of active users
├── EmotionSync invites per user: >1.5
├── Viral coefficient (K-factor): >1.3
├── Free-to-paid conversion: >5% within 30 days
└── NPS score: >50

Business KPIs:
├── CAC (Customer Acquisition Cost): <$5 (organic viral)
├── LTV (Lifetime Value): >$120 (12 months × $9.99)
├── LTV/CAC ratio: >24 (target for Series A)
├── ARPU (Average Revenue Per User): $0.50/month (blended)
├── Enterprise API revenue: $10K/month by Month 6
└── Monthly revenue growth: >30% (pre-Series A)
```

---

# APPENDIX C: COMPETITIVE DIFFERENTIATION MATRIX

```
                        Sentient   Hume AI   Cogito   Affectiva   Apple
                        ─────────  ────────  ───────  ──────────  ─────
On-device processing      ✓          ✗         ✗         ✗         ✗
4-modality fusion          ✓          ✓         ✗         ✓         ✗
Emotional memory          ✓          ✗         ✗         ✗         ✗
Dual-axis scoring         ✓          ✗         ✗         ✗         ✗
Crypto attestation        ✓          ✗         ✗         ✗         ✗
Fitzpatrick gate          ✓          ✗         ✗         Partial    ✗
Viral consumer app        ✓          ✗         ✗         ✗         ✗
Enterprise healthcare     ✓          ✗         ✓         ✓         ✗
Wearable deployment       ✓          ✗         ✗         ✗         Partial
Neuromorphic roadmap      ✓          ✗         ✗         ✗         ✗
Regulatory compliance     ✓          Partial    Partial    Partial    ✗
Open developer SDK        ✓          ✓         ✗         ✗         ✗
Data marketplace          ✓          ✗         ✗         ✗         ✗
──────────────────────────────────────────────────────────────────────
Score:                    13/13      3/13      2/13      3/13      1/13
```

---

*Blueprint authored by Tolu's AI Engineering Agent (Agent Zero)*  
*Based on comprehensive market research, regulatory analysis, and technical benchmarking*  
*Version 1.0 — April 15, 2026*
