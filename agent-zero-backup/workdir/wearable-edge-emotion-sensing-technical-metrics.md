# Wearable Emotion/Stress Sensing — On-Device/Edge Technical Metrics
## Compiled Research Notes

---

## Source 1: Fitbit Body Response Feature (Google Blog)
**URL:** https://blog.google/products-and-platforms/devices/fitbit/how-we-trained-fitbits-body-response-feature-to-detect-stress/
**Processing:** On-device (Fitbit Sense 2 / Fitbit Sense)
**Algorithm:** "Classical machine learning" — Body Response algorithm
**Sensors:** EDA (electrodermal activity / cEDA), heart rate, skin temperature
**Hardware:** Fitbit Sense, Fitbit Sense 2

### Specific Numbers Found:
- No exact latency, model size, accuracy %, power consumption, or chip names disclosed
- Qualitative: algorithm detects "body responses" in real-time using cEDA + HR + skin temp
- Trained on proprietary dataset; no public benchmarks cited
- Stress management score feature; no F1/sensitivity/specificity published

---

## Source 2: Garmin Health Research — Stress Research
**URL:** https://www.garmin.com/en-US/blog/health/garmin-health-research-glimpse-exploring-stress-research/
**Processing:** On-device (Garmin smartwatches) — implied real-time tracking
**Algorithm:** Not specifically named; references "proprietary AI model" in MindFit app context
**Sensors:** HRV (heart rate variability), EDA (micro-sweat levels), skin temperature, sleep patterns
**Hardware:** Garmin Forerunner 55, Forerunner 255, Venu smartwatches
**SDK:** Garmin Health SDK, Garmin Health Companion SDK

### Specific Numbers Found:
- No exact latency, model size, accuracy %, power consumption, or chip names disclosed
- Qualitative: devices produced "reliable health data" and served as "good alternative to ECG-based, research-grade devices"
- Study successfully identified periods of logged stress; no quantitative accuracy metrics published

---

## Source 3: Nature — Wearable Electronic Skin (s41928-024-01128-w)
**URL:** https://www.nature.com/articles/s41928-024-01128-w
**Status:** Could not extract specific technical metrics — content appeared paywall-restricted or abstract-only
**Topic:** Physicochemical-sensing electronic skins with AI
**Note:** This paper focuses on sensor materials/fabrication rather than edge ML deployment metrics

### Specific Numbers Found:
- None extracted — no latency, model size, accuracy, power, or chip data available from accessible text

---

## Source 4: OMER-NPU — On-Device Multimodal Emotion Recognition (Springer)
**URL:** https://link.springer.com/article/10.1007/s00521-025-11368-2
**Processing:** ON-DEVICE (Neural Processing Unit — NPU)
**Algorithm:** Score-based fusion (multimodal); models compressed and embedded in NPU
**Modalities:** Heart rate, EEG, Speech, Image (multimodal)
**Datasets:** CK+ (images), TESS (speech), RAVDESS (audio-visual), Complex Image Data for Korean Emotion Recognition

### Specific Numbers Found:
| Metric | Value |
|--------|-------|
| Accuracy (multimodal) | **99.68%** |
| Power consumption reduction vs GPU | **3.1151x** lower |
| Latency reduction vs GPU | **1.4703x** lower |
| Processing | On-device (NPU) |
| Fusion method | Score-based fusion |
| Model optimization | Compressed for NPU embedding |

- No absolute latency in ms, no absolute power in mW, no model size in MB/params disclosed
- Outperformed unimodal and bimodal configurations
- Exact NPU chip name not specified

---

## Source 5: Edge AI for AF Detection on Wearables (MDPI Sensors) ★★★ RICHEST SOURCE ★★★
**URL:** https://www.mdpi.com/1424-8220/25/23/7244
**Title:** "An Edge AI Approach for Low-Power, Real-Time Atrial Fibrillation Detection on Wearable Devices Based on Heartbeat Intervals"
**Processing:** ON-DEVICE (Edge Impulse inference engine on MCU)
**Algorithm:** 1D Convolutional Neural Network (1D-CNN)
**Model Architecture:**
  - Block 1: Conv1D (16 filters, kernel 3) → BatchNorm → ReLU → AvgPool (size 2) → Dropout (0.25)
  - Block 2: Conv1D (32 filters, kernel 3) → BatchNorm → ReLU → AvgPool (size 2)
  - Flatten → Dense (64, ReLU) → Dropout (0.1) → Softmax output
**Framework:** Edge Impulse

### Specific Numbers Found:

| Metric | Value |
|--------|-------|
| **Hardware** | **NUCLEO-F767ZI (ARM Cortex-M7)** |
| ECG Front-End | **MAX30003** |
| Communication | **STEVAL-STMODLTE** (LTE/MQTT) |
| ECG Sampling | **125 Hz, 18-bit resolution** |
| AI Inference Time | **2.7 ms** (AI computation alone) |
| Total Inference Block Latency | **23.16 ms** |

#### Model Size (Memory):
| Config | RAM | Flash |
|--------|-----|-------|
| INT8, 25 RR intervals | **6.1 KB** | **48.6 KB** |
| INT8, 50 RR intervals | **6.9 KB** | **62.5 KB** |
| INT8, 100 RR intervals | **8.5 KB** | **86.6 KB** |
| Float32, 25 RR intervals | **6.6 KB** | **69.9 KB** |
| Float32, 50 RR intervals | **9.7 KB** | **125.8 KB** |
| Float32, 100 RR intervals | **16.0 KB** | **221.9 KB** |

#### Accuracy:
| Config | Accuracy |
|--------|----------|
| INT8, 25 RR | **0.963 ± 0.031** |
| INT8, 50 RR | **0.976 ± 0.022** |
| INT8, 100 RR | **0.980 ± 0.023** |
| Float32, 25 RR | **0.962 ± 0.031** |
| Float32, 50 RR | **0.975 ± 0.022** |
| Float32, 100 RR | **0.980 ± 0.021** |

#### Power Consumption:
| Component / State | Avg Current | Peak Current |
|-------------------|-------------|-------------|
| ECG Front-End (MAX30003) | **~115 µA** | **~140 µA** |
| MCU — Acquisition interrupts | **96.7 mA** | **119.7 mA** |
| MCU — Neural inference | **113.6 mA** | **119.7 mA** |
| MCU — MQTT publication | **57.4 mA** | **111.3 mA** |
| MCU — Between publications | **95.3 mA** | **120.7 mA** |
| LTE Module — MQTT transmission | **61.1 mA** | **405.4 mA** |

---

## Source 6: Power Consumption IoT Edge-AI (ScienceDirect / HAL) ★★★ RICHEST SOURCE ★★★
**URL:** https://www.sciencedirect.com/science/article/pii/S2542660523002536
**PDF:** https://hal.science/hal-04204492v1/file/S2542660523002536.pdf
**Title:** "Power consumption reduction for IoT devices thanks to Edge-AI — Application to human activity recognition"
**Processing:** ON-DEVICE (Edge AI) vs Cloud comparison
**Algorithm:** Deep Convolutional Neural Network (DCNN), with 8-bit integer quantization, 60% dropout
**Application:** Human Activity Recognition (HAR) — wearable sensing

### Specific Numbers Found:

| Metric | Value |
|--------|-------|
| **Hardware** | **Arduino Nano 33 BLE** |
| **Processor** | **ARM Cortex-M4** |
| **IMU Sensor** | **LSM9DS1** |
| **Measurement Tool** | **Keysight Cx3324A** |
| **Voltage Supply** | **3.3V** |
| **Model Parameters** | **52,935 trainable** |
| **Quantization** | **8-bit integer** |

#### Power Consumption by Scenario:
| Scenario | Mode | Avg Power | Avg Current | Energy/Inference (BLE) |
|----------|------|-----------|-------------|----------------------|
| I (7.5ms interval) | Cloud — Raw data TX | **23.476 mW** | **7.078 mA** | **6.12 mJ** |
| II (1500ms interval) | Edge — Label TX | **19.915 mW** | **6.035 mA** | **5.81 mJ** |
| III (3500ms interval) | Edge — Compressed buffer | **20.054 mW** | **6.007 mA** | **6.07 mJ** |
| IV (7.5ms interval) | Edge — Minimal TX | **18.329 mW** | **5.554 mA** | **0.15 mJ** |

#### Accuracy by Sensor Position:
| Position | Accuracy | F1 Score |
|----------|----------|----------|
| Jeans Pockets | **98.2%** | **98.8%** |
| Wrist | **92.4%** | **92.4%** |
| Upper Arm | **92.9%** | **92.8%** |
| Belt | **80.9%** | **80.4%** |
| Overall (Table 8) | **98.3%** | — |

#### Key Findings:
- **Edge AI reduces energy consumption by 21%** vs Cloud/Remote server
- Best edge scenario (IV) achieves **0.15 mJ per inference** vs **6.12 mJ** for cloud
- That is a **40.8x reduction** in energy per inference (Scenario IV vs I)
- Referenced work [18] reports **79% power saving** with edge NN
- Referenced work [9] achieves **6.3 µW** with FPGA Hybrid NN (simulated)

---

## CROSS-SOURCE COMPARISON TABLE

| Source | Hardware | Algorithm | Accuracy | Latency | Power | Model Size | On-Device? |
|--------|----------|-----------|----------|---------|-------|------------|------------|
| Fitbit Blog | Fitbit Sense 2 | Classical ML | Undisclosed | Undisclosed | Undisclosed | Undisclosed | Yes |
| Garmin Blog | Forerunner 55/255, Venu | Proprietary AI | Undisclosed | Undisclosed | Undisclosed | Undisclosed | Yes |
| OMER-NPU | Unnamed NPU | Score-based fusion | 99.68% | 1.47x less than GPU | 3.12x less than GPU | Compressed (not specified) | Yes (NPU) |
| MDPI Edge AF | ARM Cortex-M7 (NUCLEO-F767ZI) | 1D-CNN | 96.3-98.0% | 2.7 ms (AI) / 23.16 ms (total) | 113.6 mA (inference) | 6.1-16 KB RAM / 48.6-222 KB Flash | Yes |
| SciDirect Power | ARM Cortex-M4 (Arduino Nano 33 BLE) | DCNN | 98.3% | N/A (2s window) | 18.3-23.5 mW | 52,935 params | Yes |
| Nature E-skin | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

---

## KEY TAKEAWAYS

1. **Most deployable edge AI for wearables uses tiny models**: 6-16 KB RAM, 48-222 KB flash on Cortex-M class processors
2. **Inference latency is sub-10ms for AI computation**: 2.7 ms on Cortex-M7 for 1D-CNN
3. **Power at inference: ~100-115 mA on Cortex-M7** at 3.3V, but edge AI saves 21% overall vs cloud by reducing radio transmissions
4. **Accuracy: 96-98% is achievable on-device** for heartbeat-based detection with INT8 quantization matching Float32
5. **Edge vs Cloud energy**: Best case 0.15 mJ per inference (edge) vs 6.12 mJ (cloud) — 40x improvement when minimizing radio use
6. **Commercial wearables (Fitbit, Garmin) do NOT publish their technical ML specs** — only research papers disclose hard numbers
