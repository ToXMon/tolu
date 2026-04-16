# Apple Watch & Samsung Galaxy Watch — On-Device Emotion/Stress Sensing: Technical Details Extraction
## Compiled from 8 Sources

---

## SOURCE 1: Apple ML Research — Digital Mental Health
**URL:** https://machinelearning.apple.com/research/digital-mental-health

| Dimension | Details |
|-----------|--------|
| **Study Name** | Apple Digital Mental Health Study |
| **Participants** | >4,000 participants, diverse by age, sex, ethnicity, depression severity |
| **Study Duration** | Up to 12 months longitudinal |
| **Data Sources** | iPhone + Apple Watch sensor data (physiological, behavioral, emotional domains) |
| **Assessments** | Periodic self-report + interview-based scales for depression, anxiety, perceived stress |
| **Processing** | Not specified (on-device vs cloud not disclosed) |
| **ML Models/Algorithms** | NOT DISCLOSED — paper focuses on study design feasibility, not technical ML implementation |
| **Accuracy Metrics** | NOT DISCLOSED |
| **Sensors** | General "sensor data" mentioned; no specific sensor types (HRV, ECG, accelerometer) enumerated |
| **Key Finding** | High participant engagement/adherence over 12 months; longitudinal symptom trajectories demonstrated |

**NOTE:** Apple's own ML research page is deliberately vague about model architectures, accuracy, and technical implementation. No hard numbers for latency, model size, power, or specific algorithms.

---

## SOURCE 2: Samsung News — Galaxy AI on Galaxy Watch
**URL:** https://news.samsung.com/uk/galaxy-ai-is-coming-to-new-galaxy-watch-for-more-motivational-health

| Dimension | Details |
|-----------|--------|
| **Processing** | On-device — "powerful on-device AI" combined with Samsung Health app |
| **Algorithm** | "Galaxy AI" — proprietary; includes "sleep AI algorithm" and "advanced health algorithms" |
| **Specific Algorithm Type** | NOT DISCLOSED (no LSTM, CNN, etc. named) |
| **Features** | Energy Score, Wellness Tips, sleep coaching, heart rate monitoring |
| **Accuracy** | NOT DISCLOSED |
| **Sensors** | Heart rate, HRV implied; exact sensor suite not specified |
| **Power** | NOT DISCLOSED |
| **Latency** | NOT DISCLOSED |
| **Model Size** | NOT DISCLOSED |

---

## SOURCE 3: Android Authority — How Galaxy Watch Measures Stress
**URL:** https://www.androidauthority.com/how-does-galaxy-watch-measure-stress-3234828/

| Dimension | Details |
|-----------|--------|
| **Samsung Stress Method** | HRV (Heart Rate Variability) analysis — continuous + on-demand |
| **Galaxy Watch Models** | Galaxy Watch 4, 5, 6, 7 (all support stress measurement) |
| **Competitor Comparison** | Fitbit Sense series & Pixel Watch 2 use EDA (electrodermal activity) sensors |
| **Accuracy** | Described as "aren't completely accurate" — no numerical percentage given |
| **Processing** | On-device (Samsung Health app processes locally) |
| **Sensors — Samsung** | HRV, Heart Rate (via PPG optical sensor) |
| **Sensors — Fitbit/Pixel** | EDA (electrodermal activity / cEDA), heart rate, skin temperature |
| **Scale** | Stress scored 1-100; categorized as low, moderate, high |
| **Key Limitation** | Smartwatches are NOT medical devices; not FDA-cleared for clinical stress diagnosis |

---

## SOURCE 4: 9to5Mac — Track Mood on Apple Watch (watchOS 10)
**URL:** https://9to5mac.com/2024/05/01/track-mood-on-apple-watch-how-to/

| Dimension | Details |
|-----------|--------|
| **Feature** | State of Mind mood logging (watchOS 10) |
| **Method** | USER SELF-REPORT — not automated ML detection |
| **How It Works** | User scrolls through emotions (e.g., Happy, Sad, Anxious) and rates intensity |
| **Associations** | Links mood entries with sleep, exercise, and other Apple Health data correlations |
| **Processing** | N/A — no ML inference; self-report only |
| **Sensors** | None directly — correlates with existing Health data post-hoc |
| **Accuracy** | N/A — self-report tool |
| **Key Note** | Apple Watch mood tracking is NOT automated emotion sensing — it requires manual user input |

---

## SOURCE 5: Nature — Ensemble Deep Learning Emotion Recognition with Samsung Galaxy Watch ★★★ RICHEST APPLE/SAMSUNG SOURCE ★★★
**URL:** https://www.nature.com/articles/s41598-025-99858-0

### Hardware & Dataset
| Dimension | Details |
|-----------|--------|
| **Device** | **Samsung Galaxy Watch SM-R810** |
| **Dataset** | **EMOGNITION database** — 43 participants (21F/22M), aged 19-29 |
| **Data Collection** | July 16 – August 4, 2020 |
| **Emotions (9)** | Amusement, Awe, Enthusiasm, Liking, Surprise, Anger, Disgust, Fear, Sadness |
| **Self-Report** | Self-Assessment Manikin (SAM) scale 1-9 |
| **Other Devices Compared** | MUSE 2 headband, Empatica E4 wristband |

### Sensors — Samsung Galaxy Watch
| Sensor | Signal |
|--------|--------|
| Accelerometer | ACC |
| Photoplethysmography (PPG) | BVP (Blood Volume Pulse) |
| Gyroscope | GYRO |
| Optical Heart Rate | HR |
| Peak-to-Peak Interval | PPI |
| Rotation | ROT |
| **NOT available** | EDA, EEG (device does not record these) |

### Model Architecture — Ensemble Stacked LSTM-GRU
| Parameter | Value |
|-----------|-------|
| **Architecture** | Stacked ensemble: LSTM (base learner) → GRU (meta learner) |
| **LSTM units** | 32 recurrent units per layer |
| **GRU units** | 32 recurrent units |
| **Hidden layer** | 32 units, tanh activation |
| **Activation (binary)** | Sigmoid |
| **Activation (multi-class)** | SoftMax |
| **Optimizer** | AdaMax |
| **Loss Function** | Sparse categorical cross-entropy |
| **Epochs** | 100 |
| **Batch Size** | 64 |
| **Recurrent Dropout** | 0.1 |
| **Standard Dropout** | 0.5 |
| **L2 Regularization** | 0.001 |
| **Framework** | Keras + TensorFlow (Python) |
| **Data Split** | 60% train / 20% validation / 20% test |
| **Class Balancing** | SMOTE-Tomek (applied to training set only) |
| **Preprocessing** | Noise reduction, normalization, linear interpolation for temporal alignment |
| **Feature Extraction** | None (deep learning learns directly from raw signal sequences) |

### Accuracy Results — Samsung Galaxy Watch
| Metric | Discrete (9 emotions) | Valence (2D) | Arousal (2D) |
|--------|----------------------|---------------|--------------|
| **Accuracy** | **99.14%** | **97.81%** | **72.94%** |
| **Precision** | **99.15%** | — | — |
| **Recall** | **99.14%** | — | — |
| **F1 Score** | **99.14%** | — | — |
| **Best single emotion** | Surprise: **99.93%** | — | — |

### Cross-Device Comparison
| Device | Accuracy | Precision | Recall | F1 |
|--------|----------|-----------|--------|-----|
| **Samsung Galaxy Watch** | **99.14%** | **99.15%** | **99.14%** | **99.14%** |
| MUSE 2 headband | 99.41% | 99.41% | 99.36% | 99.38% |
| Empatica E4 | 49.75% | — | — | — |
| MUSE 2 best single | Sadness: 99.94% | — | — | — |

### Processing Location
| Dimension | Details |
|-----------|--------|
| **Processing** | OFFLINE on computer (Python/Keras/TensorFlow) — NOT deployed on-watch |
| **Real-time claim** | Paper claims "capability for real-time emotion detection" but no on-device deployment demonstrated |

### NOT Disclosed
- No latency numbers (ms)
- No model size (MB or parameter count beyond 32-unit layers)
- No power consumption
- No on-device deployment benchmarks

---

## SOURCE 6: PMC — Apple Watch Effectiveness as Mental Health Tracker
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10853680/

| Dimension | Details |
|-----------|--------|
| **Apple Watch Models** | General "Apple Watch" mentioned; Apple Watch 6 specifically referenced |
| **Key Accuracy (mental state)** | **54% accuracy** associating neural + physiological markers with mental states (Chesnut et al.) |
| **HR/HRV Error** | **<10% error margin** for heart rate and HRV measurement (Nelson et al.) |
| **HRV Source** | Apple Watch RR interval series |
| **HRV Stress Correlation** | Hernando et al.: HRV metrics "effectively reflected changes caused by mild mental stress" |
| **Accuracy vs competitors** | Dooley et al.: Apple Watch more reliable than Fitbit and Forerunner for HR and energy expenditure |
| **Known Limitations** | Overestimates sleep duration and energy expenditure |
| **ML Algorithms** | NOT SPECIFIED in this review |
| **Processing** | NOT SPECIFIED (on-device vs cloud) |
| **Clinical Note** | Cannot diagnose mental health conditions; useful for monitoring physiological indicators only |

---

## SOURCE 7: MDPI — Systematic Review of 61 Studies (Smartwatches in Stress/Mental Health)
**URL:** https://www.mdpi.com/1999-4893/18/7/419
**Status:** HTTP 403 — could not access full text

**Expected content:** Systematic review covering smartwatch-based stress and mental health detection across 61 studies.

---

## SOURCE 8: Springer — 43 Studies AI Algorithms for Stress from HRV ★★★ RICH BENCHMARK SOURCE ★★★
**URL:** https://link.springer.com/article/10.1007/s12559-023-10200-0

### Algorithm Performance Rankings (All Studies)

#### Best Performers:
| Study | Algorithm | Accuracy | Other Metrics |
|-------|-----------|----------|---------------|
| Sevil et al. | **SVM** | **99.1%** | — |
| Castaldo et al. | **MLP** | **98%** | — |
| Ding et al. | **BPNN** | **96.4%** | With combined signals |
| Dhaouadi & Ben Khelifa | **LSTM** | **95%** | — |
| Rastgoo et al. | **CNN + LSTM** | **92.8%** | Sens: 94.13%, Spec: 97.37%, Prec: 95.00% |
| Kalatzis et al. | **ANN** | **90.83%** | — |
| Koldijk et al. | **SVM** | **90.03%** | — |
| Can et al. | **MLP** | **92.19%** | — |

#### AUC Values:
| Study | Algorithm | AUC |
|-------|-----------|-----|
| Women 22.4±2.8yr study | SVM | **0.994** |
| Maldonado et al. | SVM | **0.99** |
| Akbulut et al. | FFNN | **0.97** |
| Huang et al. | KNN | **0.74** |
| Huang et al. | SVM | **0.68** |
| Huang et al. | LR | **0.65** |
| Huang et al. | NB | **0.64** |

#### Extended Accuracy Comparison:
| Study | Algorithm | Accuracy |
|-------|-----------|----------|
| Koldijk et al. | SVM | 90.03% |
| Koldijk et al. | MLP | 88.54% |
| Koldijk et al. | RF | 87.09% |
| Koldijk et al. | IBk | 84.52% |
| Koldijk et al. | J48 | 78.20% |
| Koldijk et al. | Bayes net | 69.08% |
| Koldijk et al. | K-star | 65.81% |
| Koldijk et al. | NB | 64.77% |
| Munla et al. | SVM / SVM-RBF | 83.33% |
| Munla et al. | KNN | 66.66% |
| Hantono et al. | KNN | 82% |
| Hantono et al. | NN | 73% |
| Hantono et al. | DA | 66% |
| Hantono et al. | NB | 60% |
| Castaldo et al. | MLP | 98% |
| Castaldo et al. | C4.5 DT | 94% |
| Castaldo et al. | IBK | 94% |
| Castaldo et al. | LDA | 94% |
| Castaldo et al. | SVM | 88% |
| Can et al. | MLP | 92.19% |
| Can et al. | RF | 88.26% |
| Sriramprakash et al. | SVM-RBF | 72.83% |
| Sriramprakash et al. | KNN | 66.52% |
| Delmastro et al. | AB | 88.2% |
| Delmastro et al. | RF | 87% |
| Padmaja et al. | NB | 72% |
| Padmaja et al. | DT | 62% |
| Huang et al. | KNN | 65.37% |
| Huang et al. | LR | 59.71% |
| Huang et al. | SVM | 57.08% |
| Huang et al. | NB | 48.84% |
| Giannakakis et al. | RF | 75.1% |
| Ciabattoni et al. | KNN | 84.5% |
| Tiwari et al. | SVM-RBF | 80% |
| Qin et al. | BPNN | 93.75% |

### Most Important HRV Features
| Feature Category | Specific Features |
|------------------|-------------------|
| **Time-domain** | RMSSD, SDNN, pNN50, AVNN, MeanNN, StdNN, MeanHR, StdHR |
| **Frequency-domain** | HF, LF, VLF, TP, LF/HF ratio |
| **Nonlinear** | SD2 |
| **Ultra-short (consistent)** | MeanNN, StdNN, MeanHR, StdHR, HF, SD2 |

### Datasets Referenced
| Dataset | Description |
|---------|-------------|
| WESAD | Wearable Stress and Affect Detection |
| drivedb / DRIVEDB | Stress Recognition in Automobile Drivers |
| SWELL-KW | 2,688 instances |
| RML | Ryerson Multimedia Research Laboratory |
| CVDiMo | — |

### Sample Sizes Across Studies
9, 15, 16, 17, 18, 21, 24, 27, 34, 35, 38, 41, 42, 56, 57, 61, 83 participants

### Wearable Devices Mentioned
- Microsoft Smart Band 2
- Samsung Gear S / S2
- Fitbit
- Empatica E4
- Polar H10 / H7 chest strap
- Zephyr BioHarness34
- Shimmer3 GSR+ Development Kit
- PPG sensors (wrist-based)

### Processing Notes
- "Low-power multi-physiological monitoring processor" for hardware implementation (Attaran et al.)
- Real-time detection on smartwatches/smartphones (Ciabattoni et al., Hantono et al.)
- Ultra-short-term segments: <5 min (Tiwari et al.), 3 min HRV (Castaldo et al.)
- Deep learning requires "substantial computational resources" vs shallow ML

---

## SUPPLEMENTARY: Chip/Hardware Specifications

### Apple Watch Series 9 — S9 SiP
| Spec | Value |
|------|-------|
| **Chip** | Apple S9 SiP |
| **Process Node** | ~4nm (based on A16 Bionic die) |
| **Transistors** | 5.6 billion |
| **CPU** | Dual-core (Sawtooth) |
| **GPU** | Single core, 30% faster than S8 |
| **Neural Engine** | **4-core (quad-core)** — first multi-core NPU on Apple Watch |
| **ML Performance** | 2x faster ML tasks vs S8 |
| **ML Feature** | On-device Siri processing, dictation 25% better accuracy |
| **RAM** | Not officially disclosed (estimated ~1.5-2 GB) |
| **Storage** | 64 GB |
| **Framework** | Core ML (CPU + GPU + Neural Engine via MPS Graph / BNNS Graph) |
| **TOPS** | NOT OFFICIALLY DISCLOSED (A16 Bionic ANE = 17 TOPS; S9 likely lower) |

### Apple Watch Neural Engine History
| SiP | Neural Engine Cores | First watchOS with Core ML |
|-----|---------------------|----------------------------|
| S4 | 2-core | watchOS 6 |
| S5 | 2-core | watchOS 6 |
| S6 | 2-core | watchOS 6+ |
| S7 | 2-core | watchOS 6+ |
| S8 | 2-core | watchOS 6+ |
| **S9** | **4-core** | watchOS 10 |
| S10 | 4-core | watchOS 11 |

### Samsung Galaxy Watch 7 / Ultra — Exynos W1000
| Spec | Value |
|------|-------|
| **Chip** | Samsung Exynos W1000 |
| **Process Node** | **3nm GAA** (first 3nm wearable chip) |
| **CPU** | Penta-core Big.Little: 1x Cortex-A78 @ 1.6GHz + 4x Cortex-A55 @ 1.5GHz |
| **GPU** | Mali-G68 MP2 (supports up to 960×540 display) |
| **RAM** | 2 GB LPDDR5 |
| **Storage** | 32 GB eMMC |
| **NPU / TOPS** | NOT OFFICIALLY DISCLOSED |
| **Packaging** | Fan-Out Panel Level Packaging (FO-PLP) for heat management |
| **Performance Claims** | 2.7x faster app launches, 3.4x single-core, 3.7x multi-core vs Exynos W930 |
| **Battery** | 2-3 days typical (Watch 7), up to ~4 days (Watch Ultra) |

---

## CROSS-SOURCE SYNTHESIS — WHAT THE NUMBERS TELL US

### Summary: Hard Numbers Found

| Metric | Apple Watch | Samsung Galaxy Watch |
|--------|-------------|---------------------|
| **Best Published Accuracy (emotion)** | N/A (no automated emotion detection published) | **99.14%** (9 emotions, offline) |
| **Best Published Accuracy (stress)** | 54% (physiological→mental state association) | N/A for Samsung-specific stress accuracy |
| **HR/HRV Measurement Error** | <10% | N/A (not benchmarked) |
| **Neural Engine Cores** | 4 (S9) | No dedicated NPU disclosed |
| **Process Node** | ~4nm | **3nm GAA** |
| **RAM** | ~1.5-2 GB (est.) | 2 GB LPDDR5 |
| **On-Device Processing** | Yes (Core ML / Neural Engine) | Yes (Galaxy AI / Samsung Health) |
| **Published Latency** | N/A | N/A |
| **Published Power (ML inference)** | N/A | N/A |
| **Published Model Size** | N/A | 32-unit LSTM + 32-unit GRU (offline) |

### Summary: What Was NOT Found (Gaps)
1. **Apple publishes ZERO technical ML details** about their emotion/mental health models
2. **Samsung publishes ZERO accuracy numbers** for their on-device stress measurement
3. **No latency numbers** published by either company for emotion/stress inference
4. **No model sizes in MB** disclosed by either company
5. **No power consumption numbers** for ML inference on either watch
6. **No TOPS ratings** officially disclosed for either watch's NPU
7. **Apple Watch mood tracking (watchOS 10) is self-report only** — not automated ML
8. **All published high-accuracy results come from offline research** using watch sensor data processed on separate computers

### Best Available Benchmarks for On-Device Emotion/Stress ML (from literature)

| Algorithm | Accuracy | Hardware Context |
|-----------|----------|------------------|
| Stacked LSTM-GRU (Nature 2025) | 99.14% | Samsung Galaxy Watch data, offline Python/Keras |
| SVM (Sevil et al.) | 99.1% | HRV-based stress, research setting |
| MLP (Castaldo et al.) | 98% | Ultra-short-term HRV (3 min) |
| 1D-CNN (Edge AF, MDPI) | 96.3-98.0% | ARM Cortex-M7, 2.7ms inference, 6-16KB RAM |
| LSTM (Dhaouadi) | 95% | HRV stress detection |
| CNN+LSTM (Rastgoo et al.) | 92.8% | Stress detection, sensitivity 94.13% |
| DCNN (SciDirect Power) | 98.3% | ARM Cortex-M4, 0.15 mJ/inference edge, 52,935 params |
| DCNN (SciDirect Power) | 92.4% | Wrist position accuracy |

### Edge AI Power Reference (from prior research, wearable-class hardware)
- ARM Cortex-M7: 113.6 mA during neural inference, 2.7 ms latency, 6-16 KB RAM
- ARM Cortex-M4: 18.3 mW avg power, 0.15 mJ per inference (edge) vs 6.12 mJ (cloud)
- Edge AI reduces energy by 21-79% vs cloud by eliminating radio transmissions

---

*Compiled 2025-04-15 from 8 requested sources + supplementary chip specification searches.*
