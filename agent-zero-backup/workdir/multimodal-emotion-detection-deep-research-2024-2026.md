# Multimodal Emotion Detection — Deep Research Report (2024–2026)

Generated: 2026-04-15 | Sources: 30+ | Focus: Product-Market Fit Analysis

---

## 1. Benchmark Accuracy Matrix — SOTA Results by Dataset

| Benchmark | Best Model | Best Score | Runner-Up | Source |
|-----------|-----------|------------|----------|--------|
| **RAVDESS** | AVT-CA (2024) | **96.11% Acc**, 93.78% F1 | LSTM-AV: 89.25% | [arXiv:2407.18552](https://arxiv.org/abs/2407.18552) |
| **CMU-MOSEI** | AVT-CA (2024) | **95.84% Acc**, 94.13% F1 | — | [arXiv:2407.18552](https://arxiv.org/abs/2407.18552) |
| **CREMA-D** | AVT-CA (2024) | **94.13% Acc**, 94.67% F1 | LSTM-AV: 84.57% | [arXiv:2407.18552](https://arxiv.org/abs/2407.18552) |
| **ESD** | MemoCMT (2025) | **91.84% W-Acc**, 91.93% UW-Acc | — | [Nature](https://www.nature.com/articles/s41598-025-89202-x) |
| **MELD** (M2FNet) | M2FNet (2024) | **91.2%** (audio+text) | — | [MDPI](https://www.mdpi.com/2078-2489/16/7/518) |
| **MOSI** | MiSTER-E (2026) | **87.90% WF1** | — | [arXiv:2602.23300](https://arxiv.org/html/2602.23300v1) |
| **IEMOCAP** | TACFN (2025) | **85.7%** (class-level max) | MemoCMT: 81.85% W-Acc | [arXiv:2505.06536](https://arxiv.org/abs/2505.06536) |
| **IEMOCAP** (overall) | MemoCMT (2025) | **81.85% W-Acc**, 81.33% UW-Acc | TACFN class-level | [Nature](https://www.nature.com/articles/s41598-025-89202-x) |
| **MELD** (SOTA dialog) | MiSTER-E (2026) | **69.50% WF1** | WavFusion: 66.93% Acc | [arXiv:2602.23300](https://arxiv.org/html/2602.23300v1) |
| **MER2023** | Emotion-LLaMA (2024) | **F1 0.9036** | — | [arXiv:2406.11161](https://arxiv.org/abs/2406.11161) |
| **DEAP** (on-device) | OMER-NPU (2025) | **99.68% Acc** | — | [Springer](https://link.springer.com/article/10.1007/s00521-025-11368-2) |
| **DFEW** (zero-shot) | Emotion-LLaMA (2024) | WAR 59.37, UAR 45.59 | — | [arXiv:2406.11161](https://arxiv.org/abs/2406.11161) |

### IEMOCAP AUC-ROC per Emotion (MemoCMT 2025)
- Anger: 0.9738 | Happiness: 0.9426 | Sadness: 0.9611 | Neutral: 0.9043

### Historical IEMOCAP Progression
| Year | Model | Accuracy | Modality |
|------|-------|----------|----------|
| 2024 (May) | SpeechEmoRec (audio-only) | 78.97% | Audio |
| 2024 | WavFusion | 70.53% Acc, 70.60% WF1 | Audio+Text+Video |
| 2025 | MemoCMT | 81.85% W-Acc | Audio+Text (HuBERT+BERT) |
| 2025 | TACFN | 85.7% (per-class max) | Audio+Video |
| 2025 (mid) | SOTA reference | 83.1% | Multimodal |
| 2026 | MiSTER-E | 70.90% WF1 | Audio+Text (LLM MoE) |

---

## 2. Company Landscape & Product Capabilities

### Hume AI
- **Funding**: $72.8M total ($50M Series B Mar 2024, EQT Ventures; $12.7M Series A Jan 2023, Union Square Ventures)
- **Products**:
  - **EVI (Empathetic Voice Interface)** — speech-to-speech emotionally aware voice agents
  - **Octave** — expressive TTS for narration, podcasts, audiobooks, game avatars
  - **Expression Measurement API** — 100+ dimensions of expression from audio, video, images, text
- **Accuracy**: Internal benchmarks favorable vs ElevenLabs; public Expressive TTS Arena for testing. No public benchmark %.
- **Client Results**: Vonova: 40% lower costs, 20% higher resolution; hpy: 70% increase in therapeutic follow-through
- **Training**: Multimodal datasets from 10+ years affective science research
- **Source**: [Contrary Research](https://research.contrary.com/company/hume-ai), [Hume API](https://dev.hume.ai/docs/expression-measurement/overview)

### Affectiva (Smart Eye) — Acquired 2021
- **Technology**: Facial expression Emotion AI; automotive safety-grade (DMS); now in Smart Eye Interior Sensing
- **Recent**: Dec 2024 finished integrating into driver-monitoring suite; CES 2024 FORVIA partnership for in-vehicle Emotion AI
- **Accuracy**: "Top choice for accuracy and depth of emotional insights" (Smart Eye 2024 Annual Report). No specific public benchmarks.
- **Source**: [Smart Eye Annual Report](https://smarteye.se/wp-content/uploads/2025/04/Smart-Eye-Annual-Report-2024.pdf)

### iMotions (Smart Eye subsidiary)
- **Product**: **iMotions Lab** — multimodal biometric research platform
- **Capabilities**: Real-time 7 core emotions (Joy, Anger, Fear, Surprise, Sadness, Contempt, Disgust), eye tracking, GSR, EEG, ECG, EMG
- **Use Cases**: Academic research (100s of publications), UX research, product testing
- **Source**: [iMotions](https://imotions.com/products/imotions-lab/)

### Noldus (FaceReader)
- **Product**: **FaceReader v10** — automated facial expression analysis + voice analysis
- **Capabilities**: 6 basic emotions + neutral, Action Unit coding, valence/arousal, gaze, head orientation. v10 adds voice tone matching facial expressions
- **Accuracy**: Validated on Standardized and Motivated Facial Expression datasets; FairFace validation for bias (v9)
- **Source**: [Noldus](https://noldus.com/facereader)

### Realeyes
- **Product**: Attention & Emotion Measurement via webcam — facial coding for digital advertising
- **Capabilities**: Real-time attention + emotion (joy, surprise, disgust, fear, sadness, anger, contempt, confusion, engagement)
- **Major Deal**: **Nielsen ONE** partnership (Jul 2025) — attention data in Outcomes Marketplace
- **Source**: [Realeyes](https://realeyes.ai/resources/attention-emotion-measurement-app/), [Nielsen](https://www.nielsen.com/news-center/2025/nielsen-launches-outcomes-marketplace-debuts-ad-attention-metrics-realeyes-to-expand-beyond-reach-and-frequency/)

### Cogito (Verint) — Acquired Oct 2024
- **Product**: **Cogito Dialog** — real-time voice emotion for contact centers
- **Capabilities**: Streaming analysis of mimicry, consistency, turn taking, harmonicity, tone, tenseness; real-time agent coaching
- **Clients**: Humana, Metlife — thousands of agents
- **Integration**: AWS Marketplace, Five9; real-time transcription with emotion AI markup
- **Source**: [Verint/Cogito](https://www.verint.com/cogito/)

### Beyond Verbal → Merged into Cogito (now Verint)
- Voice-only emotion analysis; health-focused vocal intonation analytics

### Emotient → Acquired by Apple (2016)
- FACET technology integrated into Apple face analysis (Face ID, Animoji); set foundation for commercial facial expression market

### CrowdEmotion
- UK-based; crowd-sourced facial emotion analysis for media testing; less prominent in 2024-2026 vs Hume AI, Smart Eye, Realeyes

---

## 3. Fusion Architecture Deep Dive

### Fusion Paradigm Comparison

| Paradigm | How It Works | Pros | Cons | Example Models |
|----------|-------------|------|------|---------------|
| **Early Fusion** | Concatenate raw features before model | Captures cross-modal correlations early | High dimensionality, missing modality sensitivity | Feature concatenation baselines |
| **Late Fusion** | Independent modality processing, combine predictions | Robust to missing modalities, modular | Misses cross-modal interactions | Average ensemble baselines |
| **Hybrid Fusion** | Multi-stage early + late | Leverages both advantages | Complex architecture | MemoCMT, MCTAF, HyFusER |
| **Cross-Attention** | Multi-head attention across modalities | Dominant 2024-2026 paradigm | Computationally expensive | MemoCMT, AVT-CA, TACFN, CAMS |
| **Graph Neural** | Model inter-modality as graph | Structural relationships | Lower accuracy than transformers | GNN-MER (69.1% IEMOCAP) |
| **MoE (LLM)** | Mixture of experts with LLM backbone | Powerful contextual understanding | Very heavy compute | MiSTER-E (14B params) |

### Key Cross-Attention Fusion Models

**1. MemoCMT — Cross-Modal Transformer (Nature 2025)**
- Architecture: HuBERT (speech, frozen) + BERT (text) → Cross-Modal Transformer with multi-head cross-attention → MIN aggregation → classifier
- Key finding: MIN aggregation outperforms CLS/MEAN/MAX for fusion vectors
- IEMOCAP: 81.85% W-Acc, 81.33% UW-Acc
- Source: [Nature Scientific Reports](https://www.nature.com/articles/s41598-025-89202-x)

**2. AVT-CA — Audio-Visual Transformer Cross-Attention (2024)**
- Architecture: Cross-attention + hierarchical feature representations + depthwise separable convolutions
- Results: RAVDESS 96.11%, CMU-MOSEI 95.84%, CREMA-D 94.13%
- Training: 72 hours, 128 epochs, 128-core server
- Source: [arXiv:2407.18552](https://arxiv.org/abs/2407.18552)

**3. TACFN — Transformer Adaptive Cross-modal Fusion (May 2025)**
- Architecture: 1D CNN (audio) + visual encoders → adaptive fusion that doesn't require full modality info
- Key innovation: Addresses redundant features in standard cross-modal attention
- **Only 0.34M parameters** — runs on single RTX 8000
- RAVDESS: 76.76%; IEMOCAP class-level: 85.7/82.5/79.4/75.6/76.0/71.7/63.6/60.5
- Source: [arXiv:2505.06536](https://arxiv.org/abs/2505.06536)

**4. CAMS — Cross-attention + Auxiliary + Multi-head + Shared Transformer (2026)**
- Shared transformer backbone for audio-visual with cross-attention fusion
- Source: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S016763932600004X)

**5. MCTAF — Contextual Transformer Augmented Fusion (2025)**
- Lightweight: Bi-GRUs encode speech + transcripts, transformer handles context
- Designed for conversational/dialogue emotion recognition
- Source: [Springer](https://link.springer.com/article/10.1007/s10489-025-07027-7)

**6. MiSTER-E — Mixture-of-Experts (Feb 2026)**
- Architecture: LLaMA-3.1-8B + SALMONN-7B, LoRA fine-tuned, 97M trainable / ~14B total
- No speaker identity at any stage
- IEMOCAP: 70.90% WF1, MELD: 69.50% WF1, MOSI: 87.90% WF1
- Source: [arXiv:2602.23300](https://arxiv.org/html/2602.23300v1)

---

## 4. Breakthrough Papers — Full Details

### Tier 1: Highest Impact

| # | Paper | Date | Key Result | Params | Innovation |
|---|-------|------|------------|--------|------------|
| 1 | AVT-CA | Jul 2024 | RAVDESS 96.11%, MOSEI 95.84%, CREMA-D 94.13% | Not stated | Hierarchical cross-attention + depthwise separable conv |
| 2 | MemoCMT | Feb 2025 | IEMOCAP 81.85%, ESD 91.84% | Not stated | HuBERT+BERT, MIN aggregation |
| 3 | TACFN | May 2025 | IEMOCAP class 85.7%, RAVDESS 76.76% | **0.34M** | Most efficient SOTA, single GPU |
| 4 | MiSTER-E | Feb 2026 | MELD 69.50%, MOSI 87.90% | 97M trainable / 14B | LLM MoE, no speaker ID |
| 5 | Emotion-LLaMA | Jun 2024 | MER2023 F1 0.9036 | 34M trainable / 7B | Explainable emotion reasoning |
| 6 | WavFusion | Dec 2024 | IEMOCAP 70.53%, MELD 66.93% | Not stated | wav2vec 2.0 + RoBERTa + EfficientNet |

### Tier 2: Notable

| # | Paper | Result | Key Feature |
|---|-------|--------|------------|
| 7 | M2FNet (2024) | MELD 91.2% | Audio+Text transformer fusion |
| 8 | OMER-NPU (2025) | DEAP 99.68% | On-device NPU, 1.47x faster, 3.12x less power |
| 9 | LSTM-AV (2024) | RAVDESS 88.11%, SAVEE 86.75%, CREMA-D 80.27% | LSTM temporal modeling |
| 10 | MCTAF (2025) | Dialog emotion | Lightweight contextual transformer |

---

## 5. New Benchmarks: CA-MER & MoSEAR

### CA-MER (Conflict-Aware MER) — Aug 2025, ACM MM 2025
- **Purpose**: First benchmark testing emotion conflicts (inconsistent audio/video cues, e.g., smiling while angry)
- **Structure**: Three subsets: Video-aligned, Audio-aligned, Consistent (control)
- **Paper**: [arXiv:2508.01181](https://arxiv.org/abs/2508.01181)

### MoSEAR — Parameter-Efficient Emotion Reasoning
- Balanced modality integration framework
- SOTA on CA-MER, MER2023, EMER, DFEW
- Key insight: Existing MLLMs fail when modalities conflict
- **GitHub**: [ZhiyuanHan-Aaron/MoSEAR](https://github.com/ZhiyuanHan-Aaron/MoSEAR)

---

## 6. Latency & Deployment Data

| Model/System | Metric | Value | Notes |
|-------------|--------|-------|-------|
| OMER-NPU | Latency reduction | 1.47x faster than GPU | Mobilint MLA100 NPU |
| OMER-NPU | Power reduction | 3.12x less than GPU | Compressed model |
| FedMultiEmo | Memory footprint | <200 MB per client | Federated learning |
| FedMultiEmo | Convergence | 18 rounds, ~120s/round | Automotive setting |
| TACFN | Hardware | Single RTX 8000 | 0.34M params |
| MiSTER-E | Overhead | "Non-trivial compute+memory" | 14B params, server-only |
| AVT-CA | Training time | 72h, 128 epochs | 128-core server |
| Cogito/Verint | Real-time | Streaming during live calls | Voice-only, contact center |
| Hume AI EVI | Real-time | Speech-to-speech with emotion | Cloud API |
| Realeyes | Real-time | Webcam attention/emotion | Browser-based |

**Critical Gap**: None of the top 6 academic papers report inference latency in milliseconds.

---

## 7. Product-Market Fit Signals

1. **Accuracy Leader**: AVT-CA (94-96% on AV benchmarks) — audio+video only, no text, no published latency
2. **Edge Deployment King**: TACFN at 0.34M params on single GPU — best for embedded/mobile
3. **Best Speech+Text**: MemoCMT 81.85% IEMOCAP with HuBERT+BERT — practical for call centers
4. **Best Conversational**: MiSTER-E leads MELD (69.5%) — best for chat/voice assistant products
5. **Explainability**: Only Emotion-LLaMA provides interpretable reasoning — critical for regulated industries
6. **Commercial Leaders**: Hume AI ($72.8M raised), Smart Eye/Affectiva (automotive), Cogito/Verint (contact center)
7. **Gap in Market**: No model combines highest accuracy + low latency + explainability

### Market Size
- Emotion AI: $2.56B (2023) → $19.44B (2032) at 25.4% CAGR (SNS Insider)
- EDR market: $65.42B by 2030 at 15.9% CAGR (Business Research Company)

---

## 8. Source Index (30 Sources)

1. MemoCMT — https://www.nature.com/articles/s41598-025-89202-x
2. AVT-CA — https://arxiv.org/abs/2407.18552
3. TACFN — https://arxiv.org/abs/2505.06536
4. MiSTER-E — https://arxiv.org/html/2602.23300v1
5. Emotion-LLaMA — https://arxiv.org/abs/2406.11161
6. WavFusion — https://arxiv.org/html/2412.05558v1
7. OMER-NPU — https://link.springer.com/article/10.1007/s00521-025-11368-2
8. MoSEAR/CA-MER — https://arxiv.org/abs/2508.01181
9. Hume AI — https://research.contrary.com/company/hume-ai
10. Hume API — https://dev.hume.ai/docs/expression-measurement/overview
11. Smart Eye Annual Report — https://smarteye.se/wp-content/uploads/2025/04/Smart-Eye-Annual-Report-2024.pdf
12. Affectiva CES — https://www.smarteye.se/wp-content/uploads/2024/12/CES-2025-Collateral_EmotionAI.pdf
13. Smart Eye CES 2024 — https://www.businesswire.com/news/home/20240104295374/en/
14. iMotions Lab — https://imotions.com/products/imotions-lab/
15. Noldus FaceReader — https://noldus.com/facereader
16. Noldus Validation — https://noldus.com/blog/how-facereader-is-validated-in-research
17. Realeyes — https://realeyes.ai/resources/attention-emotion-measurement-app/
18. Nielsen+Realeyes — https://www.nielsen.com/news-center/2025/nielsen-launches-outcomes-marketplace-debuts-ad-attention-metrics-realeyes-to-expand-beyond-reach-and-frequency/
19. Verint/Cogito — https://www.verint.com/cogito/
20. Cogito Acquisition — https://www.cxtoday.com/contact-center/verint-acquires-cogito-develops-a-bot-that-scores-live-customer-conversations/
21. LSTM-AV — https://link.springer.com/article/10.1007/s11042-024-20227-6
22. M2FNet — https://www.mdpi.com/2078-2489/16/7/518
23. MCTAF — https://link.springer.com/article/10.1007/s10489-025-07027-7
24. CAMS — https://www.sciencedirect.com/science/article/pii/S016763932600004X
25. SNS Market — https://www.snsinsider.com/reports/emotion-ai-market-6779
26. SOTA Review — https://www.sciencedirect.com/science/article/pii/S2667305326000177
27. PMC Review — https://pmc.ncbi.nlm.nih.gov/articles/PMC12292624/
28. GNN-MER — https://www.mdpi.com/2076-3417/15/17/9622
29. FedMultiEmo — https://arxiv.org/abs/2507.15470
30. FORVIA+Smart Eye — https://www.forvia.com/en/press/forvia-and-smart-eye-join-forces-groundbreaking-emotion-ai-demo-ces-2024
