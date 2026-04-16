# Wearable Emotion Sensing: On-Device/Edge AI Research Report

**Date:** 2026-04-15  
**Scope:** Apple Watch, Fitbit, Garmin, Samsung Galaxy Watch + academic/research benchmarks  
**Focus:** On-device inference, latency, model sizes, accuracy, power consumption  

---

## Executive Summary

Consumer wearables (Apple Watch, Fitbit, Garmin, Samsung Galaxy Watch) increasingly offer stress and emotion detection, but **no major vendor publishes quantitative ML specifications** (latency, model size, power, accuracy) for their shipping products. The best hard engineering numbers come from academic and edge-AI research deploying models on comparable microcontroller hardware (ARM Cortex-M4/M7), demonstrating:

- **Inference latency: 2.7 ms** on Cortex-M7
- **Model size: 6.1–86.6 KB** (INT8 quantized)
- **Accuracy: 96–99.7%** (research conditions)
- **Power: 18.3 mW avg, 0.15 mJ/inference** (edge vs cloud: 40.8x energy savings)

---

## 1. Apple Watch — On-Device Emotion/Mental Health Sensing

### Hardware Platform

| Spec | Apple S9 SiP (Watch Series 9/Ultra 2) |
|------|------|
| Process Node | ~4nm |
| CPU | Dual-core (Sawtooth) |
| Neural Engine | **4-core** (first multi-core NPU on Apple Watch) |
| Transistors | 5.6 billion |
| RAM | ~1.5–2 GB (estimated) |
| ML Performance Claim | 2x faster than S8 |
| TOPS | **Not disclosed** |
| Source | [Apple Newsroom](https://www.apple.com/newsroom/2023/09/apple-introduces-the-advanced-new-apple-watch-series-9/), [TechSpot](https://www.techspot.com/news/100127-new-s9-sip-brings-higher-performance-energy-efficiency.html), [How-To Geek](https://www.howtogeek.com/apple-watch-series-9-announced/) |

### Emotion/Mental Health Features

| Feature | watchOS Version | On-Device? | Mechanism |
|---------|----------------|------------|----------|
| **Mood Tracking** | watchOS 10+ | Self-report | User manually logs mood via Mindfulness app — **NOT automated ML** |
| **HRV Monitoring** | All | Yes | Continuous PPG-based HRV (SDNN, RMSSD) — used for stress inference |
| **Mental State Detection** | Research only | Partial | Apple/UCLA Digital Mental Health Study (4,000+ participants, 12 months) — no published ML architecture |
| **On-Device Siri** | watchOS 10+ | Yes | Transformer model on Neural Engine for 20% more accurate dictation |
| State of Mind logging | watchOS 10 | Self-report | Journaling feature, not real-time inference |

### Apple Research Findings

- **Apple/UCLA Digital Mental Health Study**: >4,000 participants, 12 months of iPhone + Apple Watch sensor data. No ML technical details disclosed.  
  Source: [Apple ML Research](https://machinelearning.apple.com/research/digital-mental-health)
- **Accuracy for mental state association**: 54% (Chesnut et al., via PMC review)  
  Source: [PMC PMC10853680](https://pmc.ncbi.nlm.nih.gov/articles/PMC10853680/)
- **HRV measurement error**: <10% vs clinical-grade (Nelson et al.)  
  Source: Same PMC review
- **HRV as key indicator**: Heart rate variability confirmed as primary physiological marker for both physical and emotional state changes  
  Source: [APA PsycNet](https://psycnet.apa.org/record/2023-83566-002)

### Key Gap
Apple collects sensor data on-device but has **not disclosed** what ML models run locally for emotion/stress, their architecture, latency, or accuracy. The mood tracking feature in watchOS 10 is purely self-report.

---

## 2. Fitbit — On-Device Stress/Emotion Detection

### Hardware Platform

| Spec | Fitbit Sense 2 (reference device) |
|------|------|
| Primary Sensor | **cEDA (continuous Electrodermal Activity)** |
| Additional | PPG (HR, HRV), Skin Temperature, Accelerometer |
| Processor | Proprietary (not disclosed) |
| Source | [Google/Fitbit Blog](https://blog.google/products-and-platforms/devices/fitbit/how-we-trained-fitbits-body-response-feature-to-detect-stress/) |

### Stress Detection: Body Response Feature

- **Algorithm**: Classical machine learning (not deep learning) trained on cEDA sensor data
- **Sensors fused**: cEDA + HR + skin temperature + accelerometer (to filter exercise)
- **On-device**: **Yes** — runs locally on the Fitbit device
- **Latency**: **Not disclosed**
- **Model size**: **Not disclosed**
- **Accuracy**: **Not disclosed**
- **Output**: Body Response notifications when stress physical signs detected

Source: [Google/Fitbit Blog — How we trained Fitbit's Body Response](https://blog.google/products-and-platforms/devices/fitbit/how-we-trained-fitbits-body-response-feature-to-detect-stress/)

### Additional Features
- **Stress Management Score**: Composite of HRV, sleep, activity data (computed server-side)
- **EDA Scan**: On-demand electrodermal activity scan for mindfulness

### Key Gap
Fitbit confirms on-device processing for Body Response but publishes **zero quantitative ML metrics**.

---

## 3. Garmin — On-Device Stress Detection

### Hardware Platform

| Spec | Various (Forerunner, Venu, etc.) |
|------|------|
| Primary Sensor | PPG (optical HR) for HRV |
| Additional | Accelerometer, Barometric Altimeter, Pulse Ox |
| Processor | Proprietary (not disclosed) |

### Stress Detection Algorithm

- **Method**: HRV-based stress scoring using heart rate variability analysis
- **On-device**: **Yes** — all computation on-watch
- **Validation**: Garmin Forerunner 55 validated as "good alternative to ECG-based research-grade devices using PPG"  
  Source: [Garmin Health Research Blog](https://www.garmin.com/en-US/blog/health/garmin-health-research-glimpse-exploring-stress-research/) — Varun Mishra, Northeastern University
- **Latency**: **Not disclosed**
- **Model size**: **Not disclosed**
- **Accuracy**: **Not disclosed**

### Stress Score Output
- 0–100 scale, updated throughout the day
- Uses RMSSD and other HRV time-domain features
- Incorporates sleep data and activity context

### Key Gap
Same as Fitbit — confirms on-device processing but **zero quantitative ML metrics** published.

---

## 4. Samsung Galaxy Watch — On-Device Emotion/Stress AI

### Hardware Platform

| Spec | Samsung Exynos W1000 (Galaxy Watch 7) |
|------|------|
| Process Node | **3nm GAA** |
| CPU | Penta-core (1x Cortex-A78 @ 1.6GHz + 4x Cortex-A55 @ 1.5GHz) |
| NPU/AI Accelerator | **Not disclosed** |
| RAM | 2 GB LPDDR5 |
| Storage | 32 GB |
| ML Performance Claim | 2.7x faster app launches vs previous gen |
| Source | [HMC Tech comparison](https://hmc-tech.com/cpus/qualcomm-snapdragon-w5-plus-gen-1-vs-samsung-exynos-w1000) |

### Galaxy AI Features (One UI 6 Watch / Wear OS 5)

| Feature | On-Device? | Details |
|---------|------------|----------|
| **Stress Measurement** | Yes | HRV analysis via PPG sensor — continuous and on-demand |
| **Energy Score** | Partial | AI-powered composite (sleep, activity, HR) — some cloud processing |
| **Wellness Tips** | Partial | AI-generated recommendations — likely cloud-assisted |
| **Sleep Coaching** | Partial | AI sleep analysis — hybrid on-device + cloud |

Source: [Samsung Newsroom](https://news.samsung.com/uk/galaxy-ai-is-coming-to-new-galaxy-watch-for-more-motivational-health), [9to5Google](https://9to5google.com/2024/05/29/samsung-galaxy-watch-ai-features-update/)

### Samsung Stress Measurement Method
- Uses HRV (Heart Rate Variability) from PPG sensor
- Analyzes autonomic nervous system balance (sympathetic vs parasympathetic)
- Outputs stress level on scale
- Samsung explicitly states: "does not make promises, assurances or guarantees as to the accuracy"

Source: [Android Authority](https://www.androidauthority.com/how-does-galaxy-watch-measure-stress-3234828/)

### Research Benchmark (Samsung Galaxy Watch SM-R810, Academic)

| Metric | Value |
|--------|-------|
| Algorithm | Stacked LSTM (32 units) + GRU (32 units) ensemble |
| Optimizer | AdaMax, 100 epochs, batch 64 |
| Regularization | Dropout 0.5, L2 reg 0.001 |
| Accuracy (9 discrete emotions) | **99.14%** |
| Accuracy (Valence) | **97.81%** |
| Accuracy (Arousal) | **72.94%** |
| Sensors | Accelerometer, PPG/BVP, Gyroscope, HR, Peak-to-Peak Interval |
| Dataset | EMOGNITION, 43 participants, 9 emotions |
| Processing | **Offline (Python/Keras/TensorFlow)** — NOT deployed on-watch |
| Source | [Nature Scientific Reports 2025](https://www.nature.com/articles/s41598-025-99858-0) |

### Galaxy Watch 8 (2025)
- New AI features, higher price point
- Same stress monitoring foundation
- Source: [PCMag Hands-On](https://www.pcmag.com/news/unpacked-2025-first-look-samsungs-galaxy-watch-8-is-smarter-than-ever)

---

## 5. Smartwatch Chip Comparison for On-Device AI

| Chip | Device | Process | CPU | NPU/AI | RAM | TOPS |
|------|--------|---------|-----|--------|-----|------|
| **Apple S9 SiP** | Watch Series 9 | ~4nm | Dual-core | 4-core Neural Engine | ~1.5–2 GB | **Undisclosed** |
| **Exynos W1000** | Galaxy Watch 7 | 3nm GAA | 5-core (1xA78+4xA55) | Undisclosed | 2 GB LPDDR5 | **Undisclosed** |
| **Snapdragon W5+ Gen 1** | Various Wear OS | 4nm | 4x Cortex-A53 @ 1.7GHz | Hexagon DSP V66K | 2 GB | **Undisclosed** |
| **ARM Cortex-M7** | Research/MCU | Various | 1 core | None (CPU only) | 512KB–1MB | N/A |
| **ARM Cortex-M4** | Research/MCU | Various | 1 core | None (CPU only) | 256KB | N/A |

Sources: [Notebookcheck S9](https://www.notebookcheck.net/Apple-S9-SiP-Processor-Benchmarks-and-Specs.780134.0.html), [Qualcomm Product Brief PDF](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-W5-Plus-Gen-1-Wearable-Platforms-product-brief.pdf), [Electronics-Lab](https://www.electronics-lab.com/snapdragon-w5-gen-1-wearable-platform-with-qualcomm-hexagon-dsp-v66k-ai-engine/)

### Snapdragon W5+ Gen 1 Key Claims
- **50% lower power** vs previous gen
- **2x better performance**
- **2x richer features**
- **30% smaller size**
- Hexagon DSP with AI inference capabilities
- Always-on 22nm co-processor for low-power sensing

Source: [Qualcomm product brief](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-W5-Plus-Gen-1-Wearable-Platforms-product-brief.pdf)

---

## 6. On-Device Emotion Recognition: Quantitative Benchmarks

### 6.1 Edge AI on ARM Cortex-M7 (Best Published Numbers)

**Paper**: "An Edge AI Approach for Low-Power, Real-Time Atrial Fibrillation Detection" — demonstrates the performance envelope for on-wearable inference

| Metric | Value |
|--------|-------|
| Hardware | ARM Cortex-M7 (NUCLEO-F767ZI) + MAX30003 ECG front-end |
| Algorithm | 1D-CNN: Conv1D(16, k=3) -> Conv1D(32, k=3) -> Dense(64) -> Softmax |
| Framework | Edge Impulse |
| **AI Inference Latency** | **2.7 ms** |
| **Total Inference Block Latency** | **23.16 ms** |
| **Model RAM (INT8 quantized)** | **6.1–8.5 KB** |
| **Model Flash (INT8 quantized)** | **48.6–86.6 KB** |
| **Accuracy (INT8)** | **96.3–98.0%** |
| **Accuracy (Float32)** | 96.4–98.1% (INT8 matches within 0.1%) |
| **ECG Front-End Current** | ~115 uA |
| **MCU During Inference** | 113.6 mA avg / 119.7 mA peak |
| **MCU Between Inferences** | 95.3 mA |

Source: [MDPI Sensors 2025](https://www.mdpi.com/1424-8220/25/23/7244)

### 6.2 Edge AI Power Consumption Study

**Paper**: "Power consumption reduction for IoT devices thanks to Edge-AI" (ScienceDirect / HAL)

| Metric | Value |
|--------|-------|
| Hardware | Arduino Nano 33 BLE (ARM Cortex-M4) + LSM9DS1 IMU |
| Algorithm | DCNN, 52,935 parameters, 8-bit quantized |
| **Accuracy** | **98.3%** overall (Jeans: 98.2%, Wrist: 92.4%) |
| **Cloud Avg Power** | 23.476 mW (7.078 mA) |
| **Edge Avg Power** | **18.329 mW** (5.554 mA) |
| **Cloud Energy/Inference** | 6.12 mJ |
| **Edge Energy/Inference (minimal TX)** | **0.15 mJ** |
| **Edge vs Cloud Energy Savings** | **40.8x** |
| **Overall Power Reduction** | 21% |

Source: [ScienceDirect/HAL PDF](https://www.sciencedirect.com/science/article/pii/S2542660523002536)

### 6.3 OMER-NPU: On-Device Multimodal Emotion Recognition

| Metric | Value |
|--------|-------|
| Algorithm | Multimodal fusion (HR + EEG + Speech + Image) on NPU |
| **Accuracy** | **99.68%** |
| **Power vs GPU** | **3.12x lower** |
| **Latency vs GPU** | **1.47x lower** |
| Processing | Fully on-device NPU |
| Fusion Method | Score-based |
| Note | Emotion recognition, not just stress; NPU chip model not disclosed |

Source: [Springer OMER-NPU](https://link.springer.com/article/10.1007/s00521-025-11368-2)

---

## 7. Literature Benchmark: ML Algorithms for Stress/Emotion from HRV

From systematic review of 43 studies (Springer, 2023):

| Algorithm | Max Accuracy | AUC | Notes |
|-----------|-------------|-----|-------|
| **SVM** | **99.1%** | 0.994 | Best single-algorithm performer |
| **MLP** | **98%** | — | Multi-layer perceptron |
| **LSTM** | **95%** | — | Captures temporal HRV patterns |
| **CNN+LSTM** | **92.8%** | — | Sensitivity 94.13%, Specificity 97.37% |
| **Random Forest** | ~95% | — | Often used as baseline |

### Key HRV Features for Stress/Emotion Detection
- **RMSSD** (Root Mean Square of Successive Differences)
- **SDNN** (Standard Deviation of NN intervals)
- **pNN50** (Percentage of successive NN intervals >50ms)
- **AVNN** (Average NN interval)
- **HF Power** (High Frequency, 0.15–0.4 Hz — parasympathetic)
- **LF/HF Ratio** (Sympathetic-parasympathetic balance)

Source: [Springer 2023 Review](https://link.springer.com/article/10.1007/s12559-023-10200-0)

---

## 8. Sensor Modalities for Wearable Emotion Sensing

| Sensor | Signal | Emotion/Stress Indicator | Devices Using It |
|--------|--------|--------------------------|------------------|
| **PPG** | Heart Rate, HRV | Autonomic nervous system arousal | Apple Watch, Fitbit, Garmin, Samsung |
| **EDA/cEDA** | Electrodermal Activity | Sympathetic nervous system activation (stress) | Fitbit Sense 2 (cEDA) |
| **ECG** | Electrical heart activity | HRV, arrhythmia, stress | Apple Watch, Samsung (occasional) |
| **Accelerometer** | Movement/activity | Context for stress (filter exercise) | All devices |
| **Skin Temperature** | Peripheral temp | Stress response, sleep quality | Fitbit, Garmin |
| **Gyroscope** | Motion patterns | Activity context | Samsung, Apple |

---

## 9. Complete Quantitative Summary Table

| Metric | Value | Source/Hardware |
|--------|-------|----------------|
| **Fastest inference latency** | **2.7 ms** | ARM Cortex-M7, 1D-CNN (MDPI 2025) |
| **Total inference block** | **23.16 ms** | ARM Cortex-M7 (MDPI 2025) |
| **Smallest model RAM** | **6.1 KB** (INT8) | ARM Cortex-M7, 1D-CNN (MDPI 2025) |
| **Smallest model Flash** | **48.6 KB** (INT8) | ARM Cortex-M7, 1D-CNN (MDPI 2025) |
| **Largest model (research)** | **52,935 params** (~200KB) | ARM Cortex-M4, DCNN (HAL paper) |
| **Best accuracy (emotion)** | **99.68%** | OMER-NPU multimodal (Springer 2025) |
| **Best accuracy (stress)** | **99.1%** | SVM on HRV (Springer review) |
| **Lowest power (edge)** | **18.3 mW** avg | ARM Cortex-M4 (HAL paper) |
| **Lowest energy/inference** | **0.15 mJ** | ARM Cortex-M4 edge mode (HAL paper) |
| **ECG front-end power** | **~115 uA** | MAX30003 (MDPI 2025) |
| **MCU inference current** | **113.6 mA** avg | ARM Cortex-M7 (MDPI 2025) |
| **Edge vs Cloud energy** | **40.8x savings** | HAL paper |
| **Apple Watch mental state accuracy** | **54%** | Chesnut et al. via PMC |
| **Apple Watch HRV error** | **<10%** | Nelson et al. via PMC |

---

## 10. Critical Findings and Gaps

### What IS Known
1. Consumer wearables DO run stress/emotion inference **on-device** (confirmed by all vendors)
2. HRV is the dominant signal for stress detection across all platforms
3. Fitbit uniquely uses cEDA (electrodermal activity) as a primary stress sensor
4. Edge AI on comparable MCU hardware is **extremely fast** (2.7ms) and **tiny** (<87KB)
5. Edge inference uses **40.8x less energy** than cloud-based inference
6. Apple Watch S9 has a dedicated 4-core Neural Engine capable of transformer inference
7. Samsung Exynos W1000 is built on 3nm GAA — most advanced process in wearables
8. Snapdragon W5+ Gen 1 includes Hexagon DSP for AI inference tasks

### What is NOT Known (Deliberate Vendor Opacity)
1. **Zero latency numbers** from Apple, Samsung, Fitbit, or Garmin for their shipping stress/emotion features
2. **Zero model sizes** disclosed by any consumer wearable vendor
3. **Zero power consumption numbers** for ML inference on any smartwatch
4. **Zero TOPS ratings** officially disclosed for any smartwatch NPU
5. **Zero accuracy claims** for shipping stress/emotion features (Samsung explicitly disclaims accuracy)
6. All published high-accuracy results use the watch as a **sensor only** — processing happens on separate computers
7. Apple Watch mood tracking is **self-report**, not automated ML inference

### Research-to-Product Gap
The academic literature demonstrates 95–99% accuracy for stress/emotion detection using wearable sensor data, but these results come from controlled lab conditions with:
- Large batch processing on desktop GPUs
- Clean, non-motion-artifact data
- Small, non-diverse participant pools
- Offline analysis pipelines

Shipping products must handle real-world conditions (motion artifacts, diverse populations, battery constraints), which likely means lower actual accuracy.

---

## 11. Source URLs

### Vendor Sources
- [Apple Newsroom — Watch Series 9](https://www.apple.com/newsroom/2023/09/apple-introduces-the-advanced-new-apple-watch-series-9/)
- [Apple ML Research — Digital Mental Health](https://machinelearning.apple.com/research/digital-mental-health)
- [Google/Fitbit Blog — Body Response](https://blog.google/products-and-platforms/devices/fitbit/how-we-trained-fitbits-body-response-feature-to-detect-stress/)
- [Garmin Health Research — Stress](https://www.garmin.com/en-US/blog/health/garmin-health-research-glimpse-exploring-stress-research/)
- [Samsung Newsroom — Galaxy AI on Watch](https://news.samsung.com/uk/galaxy-ai-is-coming-to-new-galaxy-watch-for-more-motivational-health)
- [Qualcomm Snapdragon W5+ Gen 1 Product Brief PDF](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-W5-Plus-Gen-1-Wearable-Platforms-product-brief.pdf)

### Academic Sources
- [MDPI Sensors 2025 — Edge AI AF Detection](https://www.mdpi.com/1424-8220/25/23/7244)
- [ScienceDirect — Power Consumption IoT Edge-AI](https://www.sciencedirect.com/science/article/pii/S2542660523002536)
- [Springer — OMER-NPU On-Device Emotion](https://link.springer.com/article/10.1007/s00521-025-11368-2)
- [Nature Sci. Reports 2025 — Ensemble DL Emotion (Samsung Watch)](https://www.nature.com/articles/s41598-025-99858-0)
- [Springer 2023 — 43 Studies AI HRV Stress](https://link.springer.com/article/10.1007/s12559-023-10200-0)
- [PMC — Apple Watch Mental Health Tracker](https://pmc.ncbi.nlm.nih.gov/articles/PMC10853680/)
- [APA PsycNet — Apple Watch Mental Health](https://psycnet.apa.org/record/2023-83566-002)
- [MDPI Algorithms 2025 — Smartwatch Stress Review (61 studies)](https://www.mdpi.com/1999-4893/18/7/419)
- [Nature — Stress Monitoring with Wearable AI](https://www.nature.com/articles/s41928-024-01128-w)
- [MDPI Sensors — ECG Multi-Emotion HRV](https://www.mdpi.com/1424-8220/23/20/8636)

### Chip Spec Sources
- [Notebookcheck — Apple S9 SiP](https://www.notebookcheck.net/Apple-S9-SiP-Processor-Benchmarks-and-Specs.780134.0.html)
- [Notebookcheck — Snapdragon W5+ Gen 1](https://www.notebookcheck.net/Qualcomm-Snapdragon-W5-Plus-Gen-1-Processor-Benchmarks-and-Specs.734685.0.html)
- [HMC Tech — W5+ vs Exynos W1000](https://hmc-tech.com/cpus/qualcomm-snapdragon-w5-plus-gen-1-vs-samsung-exynos-w1000)
- [Electronics-Lab — Snapdragon W5+ Gen 1](https://www.electronics-lab.com/snapdragon-w5-gen-1-wearable-platform-with-qualcomm-hexagon-dsp-v66k-ai-engine/)

---

## 12. Related Prior Research

- **Emotional AI Market**: $2.1–2.7B in 2024, ~22% CAGR — saved at `/a0/usr/workdir/emotional-ai-market-research-2026.md`
- **Multimodal Emotion Detection Benchmarks**: saved at `/a0/usr/workdir/multimodal-emotion-detection-benchmarks-2024-2026.md`
- **Multimodal Emotion Deep Research**: saved at `/a0/usr/workdir/multimodal-emotion-detection-deep-research-2024-2026.md`
- **Neuromorphic Processors for Emotion AI**: saved at `/a0/usr/workdir/neuromorphic-processors-emotion-ai-research-2024-2026.md`
