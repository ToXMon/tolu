# Neuromorphic Processors for Emotion AI: Innatera & GrAI Matter Labs

**Research Date**: 2026-04-15
**Purpose**: Evaluate Innatera and GrAI Matter Labs neuromorphic processors for emotion recognition / affective computing applications

---

## EXECUTIVE SUMMARY

Neither Innatera nor GrAI Matter Labs has publicly demonstrated emotion recognition or affective computing on their hardware. Both target general sensor-edge inference (vision, audio, radar, wearables). However, their ultra-low-power, ultra-low-latency architectures make them theoretically well-suited for always-on emotion sensing at the edge. A Springer 2026 paper proposes a neuromorphic engine for affective analysis, confirming the conceptual viability.

---

## 1. INNATERA — Company Overview

- **Founded**: 2018, spun from TU Delft
- **HQ**: Rijswijk, Netherlands | Design center: Bangalore, India
- **Funding**: Undisclosed (backed by EU and Dutch innovation grants)
- **Products**: T1 (1st gen), PULSAR (2nd gen, launched May 21, 2025 at Computex)

### 1.1 Innatera T1 (1st Generation)

| Spec | Value | Source |
|------|-------|--------|
| Architecture | Analog-mixed signal SNN accelerator + CNN accelerator + RISC-V CPU | [NeuromorphicCore.ai](https://neuromorphiccore.ai/insights/innatera/) |
| Power (inference) | < 1 mW | [NeuromorphicCore.ai](https://neuromorphiccore.ai/insights/innatera/) |
| Latency | < 1 ms (real-time audio/radar/vision) | [NeuromorphicCore.ai](https://neuromorphiccore.ai/insights/innatera/) |
| Process node | ~22-28nm (not officially confirmed) | [NeuromorphicCore.ai](https://neuromorphiccore.ai/insights/innatera/) |
| Workloads | Keyword spotting, gesture recognition, presence detection, ECG analysis | [NeuromorphicCore.ai](https://neuromorphiccore.ai/insights/innatera/) |
| Interfaces | Standard sensor interfaces with on-chip encoders | [Heidelberg HBP](https://flagship.kip.uni-heidelberg.de/jss/HBPm?m=displayPresentation&mI=263&mEID=9649) |

### 1.2 Innatera PULSAR (2nd Generation — Flagship)

| Spec | Value | Source |
|------|-------|--------|
| Launch date | May 21, 2025 (Computex) | [Innatera press release](https://www.innatera.com/newsroom/innatera-unveils-pulsar-the-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| Process node | 28nm TSMC (standard) | [eeNews Europe](https://www.eenewseurope.com/en/innatera-claims-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| Die size | 2.6 x 2.8 mm, 36-pin package | [eeNews Europe](https://www.eenewseurope.com/en/innatera-claims-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| Architecture | 12 digital cores + 4 analog cores (SNN fabric) + CNN accelerator + RISC-V core | [IEEE Spectrum](https://spectrum.ieee.org/innatera-neuromorphic-chip) |
| Power — radar presence detection | 600 uW (0.6 mW) | [IEEE Spectrum](https://spectrum.ieee.org/innatera-neuromorphic-chip); [EE Times](https://www.eetimes.com/innatera-adds-more-accelerators-to-spiking-microcontroller/) |
| Power — audio scene classification | 400 uW (0.4 mW) | [IEEE Spectrum](https://spectrum.ieee.org/innatera-neuromorphic-chip); [EE Times](https://www.eetimes.com/innatera-adds-more-accelerators-to-spiking-microcontroller/) |
| Power — general range | Sub-milliwatt to microwatt | [EE World Online](https://www.eeworldonline.com/risc-v-based-neuromorphic-processor-operates-at-sub-milliwatt-power/) |
| Energy vs conventional AI | 500x lower | [Innatera press release](https://www.innatera.com/newsroom/innatera-unveils-pulsar-the-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| Latency vs conventional AI | 100x lower | [Innatera press release](https://www.innatera.com/newsroom/innatera-unveils-pulsar-the-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| Latency (absolute) | Sub-millisecond (~1/100th of conventional) | [IEEE Spectrum](https://spectrum.ieee.org/innatera-neuromorphic-chip) |
| Volume price | Under $5 | [eeNews Europe](https://www.eenewseurope.com/en/innatera-claims-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| Target applications | Always-on wearables, real-time sensor intelligence | [Innatera press release](https://www.innatera.com/newsroom/innatera-unveils-pulsar-the-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/) |
| CES 2026 showcase | Real-world neuromorphic edge AI demos | [Innatera CES 2026](https://innatera.com/press-releases/redefining-the-cutting-edge-innatera-debuts-real-world-neuromorphic-edge-ai-at-ces-2026) |

### 1.3 Innatera — Emotion AI Relevance

- No direct emotion recognition or affective computing demos found
- Theoretically strong fit: sub-mW power enables always-on sensing in wearables/earbuds/glasses
- Audio processing at 400 uW could support voice emotion analysis (prosody, stress detection)
- ECG analysis capability suggests potential for physiological emotion sensing
- Sub-ms latency critical for real-time emotion feedback loops

---

## 2. GrAI Matter Labs (GML) — Company Overview

- **Founded**: 2016, spun from Vision Institute (UPMC) Paris
- **Offices**: France, Netherlands, USA
- **Funding**: $14M raised + DARPA seed funding
- **Status**: Acquired by Snap Inc. (~October 2024/2025 per French media)
- **Products**: GrAI One, GrAI VIP (Vision Inference Processor)
- **Note**: No product named 'GrAIONTaps' exists for this company

### 2.1 GrAI VIP (Vision Inference Processor)

| Spec | Value | Source |
|------|-------|--------|
| Architecture | GrAICore neuron engine + 2x ARM processors + on-chip memory | [Cambrian AI PDF](https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf) |
| Paradigm | NeuronFlow — dynamic dataflow + neuromorphic, sparsity-native | [Cambrian AI PDF](https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf) |
| Data precision | FP16 (pivoted from native INT16) | [TechInsights](https://www.techinsights.com/blog/grai-matter-pivots-floating-point) |
| GrAICore clock | 1 GHz | [Swapcard databrief](https://cdn-api.swapcard.com/public/files/980c3757b3a84c9491def10533885b3f.pdf) |
| Core voltage (typ) | 0.80 V (range 0.72-0.99 V) | [Swapcard databrief](https://cdn-api.swapcard.com/public/files/980c3757b3a84c9491def10533885b3f.pdf) |
| Core current (max theoretical) | 6.5 A (short-duration theoretical limit) | [Swapcard databrief](https://cdn-api.swapcard.com/public/files/980c3757b3a84c9491def10533885b3f.pdf) |
| Implied max core power | ~5.2 W (0.80V x 6.5A theoretical max) | Calculated from Swapcard specs |
| I/O voltage 1 | 1.8 V (range 1.62-1.98 V), max 688 mA | [Swapcard databrief](https://cdn-api.swapcard.com/public/files/980c3757b3a84c9491def10533885b3f.pdf) |
| I/O voltage 2 | 3.3 V (range 3.10-3.60 V) | [Swapcard databrief](https://cdn-api.swapcard.com/public/files/980c3757b3a84c9491def10533885b3f.pdf) |
| Power vs Jetson Nano | >10x lower power for ResNet50 | [Cambrian AI PDF](https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf) |
| Competitor power reference | Typical inference devices use 5-10 W | [Cambrian AI PDF](https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf) |
| Latency vs competitors | 1/10th response time | [Cambrian AI PDF](https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf) |
| Response time | Few milliseconds (general); microseconds for PilotNet on GrAI One | [GML LinkedIn](https://www.linkedin.com/posts/graimatterlabs_grai-matter-labs-fastest-edge-ai-processor-activity-6770808263463206912-ppuR); [EE Times](https://www.eetimes.com/grai-matter-labs-raises-14m-to-foster-edge-ai/) |
| Form factor | PCIe M.2 dev board; near-sensor VIP board | [eeNews Europe](https://www.eenewseurope.com/en/grai-matter-labs-samples-neuromorphic-chip-on-board/) |
| Pre-orders | $1M from consumer Tier-1s, module makers (ADLink, Framos, ERM), gov/automotive | [EE Times](https://www.eetimes.com/neuromorphic-chip-gets-1-million-in-pre-orders/) |
| Process node | Not disclosed | N/A |
| TOPS/throughput | Not disclosed (only relative: 10x vs Jetson Nano for ResNet50) | N/A |
| Model sizes supported | Not explicitly stated; ResNet50 demonstrated | [Cambrian AI PDF](https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf) |

### 2.2 NeuronFlow Architecture (GML's foundational IP)

| Spec | NeuronFlow I | NeuronFlow II | Source |
|------|-------------|--------------|--------|
| Process node | 28nm digital | 14nm digital | [DATE 2020 paper](https://www.date-conference.com/proceedings-archive/2020/pdf/1022.pdf) |
| Energy per synaptic op | 20 pJ | 10 pJ | [DATE 2020 paper](https://www.date-conference.com/proceedings-archive/2020/pdf/1022.pdf) |
| Throughput model | 1 incoming event per clock cycle per Neuron Core | Same | [DATE 2020 paper](https://www.date-conference.com/proceedings-archive/2020/pdf/1022.pdf) |
| Absolute latency / total power | Not specified | Not specified | N/A |

### 2.3 GrAI Matter Labs — Emotion AI Relevance

- No direct emotion recognition or affective computing demos found
- FP16 precision is beneficial for emotion models requiring dynamic range (audio features, facial action units)
- Multi-modal sensor interfaces (audio + video + pressure) align with multimodal emotion detection
- Human-machine interaction listed as target market — could encompass emotion-aware interfaces
- Snap Inc. acquisition suggests potential integration into AR glasses (emotion-reactive filters/experiences)

---

## 3. COMPARATIVE ANALYSIS

| Dimension | Innatera PULSAR | GrAI VIP |
|-----------|-----------------|----------|
| **Status** | Commercially available (May 2025) | Engineering samples; acquired by Snap |
| **Process** | 28nm TSMC | Not disclosed (NeuronFlow IP: 28nm/14nm) |
| **Power (typical)** | 0.4-0.6 mW (application-level) | ~5.2W theoretical max; typical likely 0.5-2W estimated |
| **Power (claim)** | 500x lower than conventional | >10x lower than Jetson Nano |
| **Latency (absolute)** | Sub-millisecond | Microseconds to few ms |
| **Latency (claim)** | 100x lower | 10x better than competitors |
| **Architecture** | SNN + CNN + RISC-V (12 digital + 4 analog cores) | GrAICore + 2x ARM + NeuronFlow |
| **Precision** | Spike-based (not explicitly stated) | FP16 |
| **Price** | <$5 volume | Not disclosed |
| **Die size** | 2.6 x 2.8 mm | Not disclosed |
| **Clock** | Not disclosed | 1 GHz |
| **Emotion AI demos** | None | None |
| **Market focus** | Wearables, always-on sensors | Vision, audio, industrial, automotive |

---

## 4. NEUROMORPHIC EMOTION AI — BROADER LANDSCAPE

| Finding | Detail | Source |
|---------|--------|--------|
| Springer 2026 paper | Proposes neuromorphic engine for emotional/affective analysis; software-only, references Loihi and SpiNNaker | [Springer](https://link.springer.com/article/10.1007/s11042-026-21288-5) |
| Quantum-inspired encoding | Discusses human emotion identification in neuromorphic context | [PMC/NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC12845882/) |
| Intel/IBM/MythWorx | Shrinking neuromorphic AI to 20 watts (human brain equivalent) | [Forbes](https://www.forbes.com/sites/sandycarter/2026/04/13/intel-ibm-and-mythworx-are-shrinking-neuromorphic-ai-to-20-watts/) |
| Market CAGR | 108% projected for neuromorphic computing | [DevTechInsights](https://devtechinsights.com/neuromorphic-chips-2025/) |

---

## 5. DATA GAPS

| Gap | Chip | Notes |
|-----|------|-------|
| Typical operating power (mW) | GrAI VIP | Only theoretical max (5.2W) and relative claims exist |
| Process node | GrAI VIP | Not disclosed in any public document |
| TOPS / throughput | GrAI VIP | Only relative: 10x vs Jetson Nano for ResNet50 |
| Absolute latency (ms) | GrAI VIP | Only qualitative: microseconds to few ms |
| Neuron count / model capacity | Innatera PULSAR | Not disclosed |
| Exact process node | Innatera T1 | Only rumored (22-28nm) |
| Emotion AI demos | Both | Zero public demonstrations for either chip |

---

## 6. FEASIBILITY ASSESSMENT: EMOTION AI ON THESE CHIPS

### Innatera PULSAR — High Fit
- Sub-mW power enables always-on emotion sensing in wearables
- Audio processing at 400 uW supports voice prosody analysis
- ECG capability enables physiological emotion detection
- Sub-ms latency critical for real-time emotion feedback
- Limitation: Small model capacity (unknown neuron count), likely limited to lightweight SNN models

### GrAI VIP — Moderate Fit
- FP16 precision supports emotion models with dynamic range
- Multi-modal sensor interfaces (audio+video) align with multimodal emotion detection
- Snap acquisition may lead to AR glasses emotion applications
- Higher power budget (likely watts, not microwatts) limits always-on wearable use
- Limitation: Unknown typical power, process node, and absolute latency

---

## ALL SOURCE URLs

### Innatera
1. https://www.innatera.com/newsroom/innatera-unveils-pulsar-the-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/
2. https://spectrum.ieee.org/innatera-neuromorphic-chip
3. https://www.eenewseurope.com/en/innatera-claims-worlds-first-mass-market-neuromorphic-microcontroller-for-the-sensor-edge/
4. https://www.eeworldonline.com/risc-v-based-neuromorphic-processor-operates-at-sub-milliwatt-power/
5. https://sp-edge.com/updates/43662
6. https://circuitcellar.com/newsletter/innatera-neuromorphic-microcontroller-for-the-sensor-edge/
7. https://audioxpress.com/news/innatera-unveils-pulsar-neuromorphic-processor-at-computex-2025
8. https://open-neuromorphic.org/neuromorphic-computing/hardware/pulsar-by-innatera/
9. https://www.financialcontent.com/article/tokenring-2026-1-27-the-brain-on-a-chip-revolution-innateras-2026-push-to-democratize-neuromorphic-ai-for-the-edge
10. https://www.eetimes.com/innatera-adds-more-accelerators-to-spiking-microcontroller/
11. https://neuromorphiccore.ai/insights/innatera/
12. https://innatera.com/press-releases/redefining-the-cutting-edge-innatera-debuts-real-world-neuromorphic-edge-ai-at-ces-2026

### GrAI Matter Labs
1. https://cambrian-ai.com/wp-content/uploads/edd/2022/05/GrAI-Matter-Labs-FINAL.pdf
2. https://cdn-api.swapcard.com/public/files/980c3757b3a84c9491def10533885b3f.pdf
3. https://www.techinsights.com/blog/grai-matter-pivots-floating-point
4. https://www.eetimes.com/neuromorphic-chip-gets-1-million-in-pre-orders/
5. https://www.eetimes.com/grai-matter-labs-raises-14m-to-foster-edge-ai/
6. https://www.eenewseurope.com/en/grai-matter-labs-samples-neuromorphic-chip-on-board/
7. https://www.neuromorphiccore.ai/insights/grai-matter-labs/
8. https://www.date-conference.com/proceedings-archive/2020/pdf/1022.pdf
9. https://ieeexplore.ieee.org/document/9116352
10. https://www.techpowerup.com/294904/grai-matter-labs-unveils-sparsity-native-ai-soc
11. https://www.edgeir.com/grai-matter-labs-launches-edge-ai-chip-solution-for-industrial-automation-applications-20220523
12. https://hk.marketscreener.com/quote/stock/SNAP-INC-34091150/news/French-Media-Snap-Inc-snaps-up-French-Dutch-AI-trailblazer-GrAI-Matter-Labs-46019330/
13. https://ibionext.com/en/grai-matter-labs-raises-14m-to-bring-fastest-ai-per-watt-to-every-device-on-the-edge/
14. https://www.linkedin.com/posts/graimatterlabs_grai-matter-labs-fastest-edge-ai-processor-activity-6770808263463206912-ppuR

### Emotion AI / Neuromorphic General
1. https://link.springer.com/article/10.1007/s11042-026-21288-5
2. https://pmc.ncbi.nlm.nih.gov/articles/PMC12845882/
3. https://www.forbes.com/sites/sandycarter/2026/04/13/intel-ibm-and-mythworx-are-shrinking-neuromorphic-ai-to-20-watts/
4. https://devtechinsights.com/neuromorphic-chips-2025/
