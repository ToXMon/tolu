# Multimodal Emotion Detection Breakthroughs (2024-2026)
## Structured Benchmark Report for Product-Market Fit Analysis

Generated: 2026-04-15

---

## 1. WavFusion

| Field | Detail |
|-------|--------|
| **Paper** | WavFusion: Gated Cross-modal Attention and Multimodal Homogeneous Feature Discrepancy Learning for Speech Emotion Recognition |
| **Source** | arxiv.org/html/2412.05558v1 |
| **Date** | December 2024 |

### Benchmark Results

| Benchmark | Accuracy (ACC) | Weighted F1 (WF1) |
|-----------|----------------|---------------------|
| **IEMOCAP** | **70.53%** | **70.60%** |
| **MELD** | **66.93%** | **66.10%** |

### Architecture
- **Core**: wav2vec 2.0 as Major Modality Encoder (shallow + deep transformer layers)
- **Text**: RoBERTa (frozen) for text feature extraction
- **Visual**: EfficientNet (frozen) + A-GRU-LVC module (global + local visual features)
- **Fusion**: Gated cross-modal attention mechanism + multimodal homogeneous feature discrepancy learning
- **Parameters**: Not explicitly stated

### Dataset Sizes
- **IEMOCAP**: 7,380 total samples, 12 hours of data, 5-fold cross-validation

### Latency/Speed
- Not reported

---

## 2. MiSTER-E

| Field | Detail |
|-------|--------|
| **Paper** | MiSTER-E: Mixture-of-Experts Speech Emotion Recognition with Contextual Modeling |
| **Source** | arxiv.org/html/2602.23300v1 |
| **Date** | February 2026 |

### Benchmark Results

| Benchmark | Weighted F1 | Notes |
|-----------|-------------|-------|
| **IEMOCAP** | **70.90%** | Full model (~14B params) |
| **MELD** | **69.50%** | Full model (~14B params) |
| **MOSI** | **87.90%** | Full model (~14B params) |

**Variant Comparison:**

| Variant | IEMOCAP WF1 | MELD WF1 | Params |
|---------|-------------|----------|--------|
| MiSTER-E (full) | 70.9% | 69.5% | ~14B |
| w/o LLM/SLLM (large) | 71.1% | 68.4% | ~750M |
| w/o LLM/SLLM (small) | 69.5% | 66.4% | ~450M |

**IEMOCAP Per-Class F1:** Angry 68.4%, Excited 77.9%, Frustrated 69.0%, Happy 40.2%, Neutral 80.2%, Sad 83.8%

**MELD Per-Class F1:** Angry 62.5%, Disgust 42.9%, Fear 30.6%, Joy 65.4%, Neutral 81.3%, Sad 50.3%, Surprise 61.5%

### Architecture
- **Core**: Mixture-of-Experts (MoE) model, decoupled context modeling from cross-modal fusion
- **Text Encoder**: LLaMA-3.1-8B (fine-tuned via LoRA)
- **Speech Encoder**: SALMONN-7B (fine-tuned via LoRA)
- **Context**: Context Addition Network (CAN) with BiGRU for conversational modeling
- **Total Parameters**: ~14 billion
- **Trainable Parameters**: 97M (88M each for LLM/SLLM LoRA + 81M conversational modeling)

### Dataset Sizes
- **IEMOCAP**: 7,433 utterances total (5,810 train/val in 92 conversations; 1,623 test in 31 conversations)
- **MOSI**: 2,199 utterances total (1,188 train in 49 monologues; 325 val in 13; 686 test in 31)

### Latency/Speed
- LLM training: ~10 min/epoch
- SLLM training: ~20 min/epoch
- Rest of model: ~10 min for 100 epochs
- **Real-time limitation noted**: "non-trivial computational and memory overhead" may limit real-time applicability

---

## 3. TACFN

| Field | Detail |
|-------|--------|
| **Paper** | TACFN: Transformer-based Adaptive Cross-modal Fusion Network for Multimodal Emotion Recognition |
| **Source** | arxiv.org/abs/2505.06536 |
| **Date** | May 2025 |

### Benchmark Results

**RAVDESS (8-class emotion):**

| Method | Accuracy |
|--------|----------|
| 3D RexNeXt50 (Vis.) | 62.99% |
| 1D CNN (Aud.) | 56.53% |
| Averaging | 68.82% |
| MCA | 74.58% |
| MSAF | 74.86% |
| **TACFN (Ours)** | **76.76%** |

**RAVDESS Per-Class Accuracy (Audio / Visual / TACFN):**
- Neutral: 54.2 / 58.6 / 65.6
- Calm: 63.4 / 66.5 / 71.2
- Happy: 57.3 / 68.1 / 70.2
- Sad: 72.0 / 64.9 / 81.4
- Angry: 68.3 / 77.2 / 87.0
- Fearful: 73.4 / 68.8 / 86.3
- Disgust: 61.5 / 69.5 / 73.2
- Surprised: 74.1 / 76.3 / 81.7

**IEMOCAP Comparison:**

| Method | Metrics (Acc/F1 per class) |
|--------|--------------------------|
| MulT | 84.8, 81.9, 77.7, 74.1, 73.9, 70.2, 62.5, 59.7 |
| LMF-MulT | 85.6, 79.0, 79.4, 70.3, 75.8, 65.4, 59.2, 44.0 |
| PMR | 86.4, 83.3, 78.5, 75.3, 75.0, 71.3, 63.7, 60.9 |
| **TACFN** | **85.7, 82.5, 79.4, 75.6, 76.0, 71.7, 63.6, 60.5** |

### Architecture
- **Audio Encoder**: 1D CNN on MFCC features + max-pooling
- **Visual Encoder**: 2D face markers for RAVDESS (crop to 224x224); Facet facial action units for IEMOCAP
- **Fusion**: Adaptive Cross-modal Blocks (Transformer encoder) with self-attention for intra-modal selection + cross-modal attention for feature reinforcement + residual connections + feature splicing for fused weight vector

### Parameters
- **IEMOCAP**: **0.34M** parameters
- **RAVDESS**: **26.30M** parameters (different backbone)

### Dataset Sizes
- **RAVDESS**: 1,440 video clips, 24 actors
- **IEMOCAP**: 151 videos (2,717 train, 798 validation, 938 test)

### Hardware
- Single NVIDIA RTX 8000 GPU

---

## 4. AVT-CA

| Field | Detail |
|-------|--------|
| **Paper** | Multimodal Emotion Recognition using Audio-Video Transformer Fusion with Cross Attention |
| **Source** | arxiv.org/abs/2407.18552 (v4) |
| **Date** | July 2024 (updated 2025) |

### Benchmark Results

| Benchmark | Accuracy (%) | F1-Score (%) |
|-----------|-------------|-------------|
| **RAVDESS** | **96.11%** | **93.78%** |
| **CMU-MOSEI** | **95.84%** | **94.13%** |
| **CREMA-D** | **94.13%** | **94.67%** |

These are the highest reported accuracies across all papers in this analysis.

### Architecture
- **Audio Pipeline**: Two consecutive convolutional blocks (local + global patterns) + batch norm + ReLU + max pooling
- **Video Pipeline**: Conv2D blocks + channel attention + spatial attention + two inverted residual blocks (depthwise separable convolutions for micro-expressions)
- **Fusion**:
  - Intermediate Transformers (IT-4): 4-head attention for audio-video temporal synchronization
  - Cross-Self-Attention (CT-4): Bidirectional audio-video attention for significant feature isolation
- **Prediction**: Max-pooling + element-wise addition + FC + softmax
- **Parameters**: Not stated

### Dataset Sizes
- CMU-MOSEI, RAVDESS, CREMA-D used (exact split sizes not reported in paper)

### Training Details
- **Training Time**: ~72 hours
- **Epochs**: 128
- **Optimizer**: Adam (lr=0.01, weight decay=0.001)
- **Batch Size**: 8
- **Hardware**: AMD EPYC 7763 64-core (128 CPUs), Linux 5.15.133

### Latency/Speed
- Inference latency not reported
- Computational complexity for inverted residual blocks: O(H'W'(k^2C' + C'^2))

---

## 5. Emotion-LLaMA

| Field | Detail |
|-------|--------|
| **Paper** | Emotion-LLaMA: Multimodal Emotion Recognition and Reasoning with Instruction Tuning |
| **Source** | arxiv.org/abs/2406.11161 |
| **Date** | June 2024 |

### Benchmark Results

| Benchmark | Metric | Score |
|-----------|--------|-------|
| **EMER** | Clue Overlap | **7.83** |
| **EMER** | Label Overlap | **6.25** |
| **MER2023** | F1 Score | **0.9036** |
| **DFEW** (zero-shot) | UAR | **45.59** |
| **DFEW** (zero-shot) | WAR | **59.37** |

### Architecture
- **Backbone**: Modified LLaMA2-chat (7B parameters)
- **Encoders**: Audio, visual, and text emotion-specific encoders (frozen)
- **Alignment**: Features aligned into shared space via linear projection
- **Tuning**: Instruction tuning with LoRA
- **Total Parameters**: 7B (LLaMA2-chat)
- **Trainable Parameters**: **34M** (0.495% of total)

### Dataset Sizes
- **MERR Dataset**: 28,618 coarse-grained + 4,487 fine-grained annotated samples

### Latency/Speed
- Not reported

---

## 6. MemoCMT

| Field | Detail |
|-------|--------|
| **Paper** | MemoCMT: Cross-Attention Fusion of HuBERT and BERT for Enhanced Speech Emotion Recognition |
| **Source** | nature.com/articles/s41598-025-89202-x |
| **Date** | 2025 (Nature Scientific Reports) |

### Benchmark Results

**IEMOCAP:**

| Metric | Score |
|--------|-------|
| **Weighted Accuracy (W-Acc)** | **81.85%** |
| **Unweighted Accuracy (UW-Acc)** | **81.33%** |

| Emotion | AUC-ROC |
|---------|---------|
| Anger | 0.9738 |
| Happiness | 0.9426 |
| Sadness | 0.9611 |
| Neutral | 0.9043 |

**ESD Dataset:**

| Metric | Score |
|--------|-------|
| **Weighted Accuracy (W-Acc)** | **91.84%** |
| **Unweighted Accuracy (UW-Acc)** | **91.93%** |
| Neutral Accuracy | 97.24% |
| Other Emotions | >90% each |
| AUC-ROC | ~0.9900 (all 5 emotions) |

**MELD:**

| Phase | Aggregation | Accuracy | F1 | Precision | Recall |
|-------|-------------|----------|-----|-----------|--------|
| Validation | CMT+MEAN | 60.83% | 57.71% | 58.18% | 60.83% |
| Validation | CMT+MIN | 60.38% | 57.99% | 58.29% | 60.38% |
| **Testing** | **CMT+MIN** | **64.18%** | **62.52%** | **63.82%** | **64.18%** |

### Architecture
- **SER Module**: HuBERT (frozen during training)
- **TER Module**: BERT
- **Fusion**: Cross-attention Module based Fusion Strategy (CMT)
- **Aggregation**: CLS / MEAN / MIN / MAX (MIN performed best on IEMOCAP and ESD)
- **Parameters**: Not stated

### Training Details
- Batch size: 1
- Epochs: 100
- Learning rate: 0.0001
- High computational requirements noted (transformer architecture)

### Latency/Speed
- Not reported

---

## Cross-Paper Comparison Matrix

### IEMOCAP Performance

| Model | Accuracy | WF1 | Params | Date |
|-------|----------|-----|--------|------|
| MemoCMT | 81.85% (W-Acc) | - | Not stated | 2025 |
| TACFN | 85.7 (best class) | 82.5 (best class) | 0.34M | 2025 |
| WavFusion | 70.53% | 70.60% | Not stated | Dec 2024 |
| MiSTER-E | - | 70.90% | ~14B (97M trainable) | Feb 2026 |

### MELD Performance

| Model | Accuracy | WF1 | Date |
|-------|----------|-----|------|
| MemoCMT | 64.18% | 62.52% | 2025 |
| MiSTER-E | - | 69.50% | Feb 2026 |
| WavFusion | 66.93% | 66.10% | Dec 2024 |

### RAVDESS Performance

| Model | Accuracy | F1 | Params | Date |
|-------|----------|-----|--------|------|
| AVT-CA | **96.11%** | **93.78%** | Not stated | Jul 2024 |
| TACFN | 76.76% | - | 26.30M | May 2025 |

### Other Benchmarks

| Model | Benchmark | Metric | Score |
|-------|-----------|--------|-------|
| AVT-CA | CMU-MOSEI | Acc / F1 | 95.84% / 94.13% |
| AVT-CA | CREMA-D | Acc / F1 | 94.13% / 94.67% |
| MiSTER-E | MOSI | WF1 | 87.90% |
| MemoCMT | ESD | W-Acc / UW-Acc | 91.84% / 91.93% |
| Emotion-LLaMA | MER2023 | F1 | 0.9036 |
| Emotion-LLaMA | DFEW (zero-shot) | WAR / UAR | 59.37 / 45.59 |

---

## Product-Market Fit Key Takeaways

1. **Best-in-class accuracy**: AVT-CA dominates RAVDESS (96.11%) and CMU-MOSEI (95.84%) but uses audio+video only
2. **Most parameter-efficient**: TACFN achieves competitive results with only 0.34M params on IEMOCAP
3. **Best speech+text fusion**: MemoCMT achieves 81.85% on IEMOCAP with HuBERT+BERT cross-attention
4. **Highest MELD performance**: MiSTER-E leads MELD at 69.50% WF1 but requires ~14B params
5. **Instruction-following capable**: Emotion-LLaMA enables reasoning-based emotion recognition (MER2023 F1=0.9036)
6. **Real-time viability**: TACFN (0.34M params) and MemoCMT are best suited for edge deployment; MiSTER-E explicitly noted as challenging for real-time
7. **Training cost spectrum**: TACFN runs on single RTX 8000; AVT-CA requires 72 hours on 128-core server; MiSTER-E uses 14B-param LLMs
