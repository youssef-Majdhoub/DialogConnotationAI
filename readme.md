# Conversational Connotation AI

## Overview

This project is an **end-to-end AI system** for analyzing the **connotation of sentences in dialogs**.
Each sentence is assigned a **continuous score** from **-1 (direct insult)** to **+1 (clear flirtation)**, with **0 as neutral**.

Unlike typical sentiment analysis, this project focuses on **gradual social nuance** and conversational context.

The project demonstrates the ability to **build AI from scratch**, covering:

* Data collection and cleaning
* Dataset creation and annotation tools
* Data pipeline construction
* Model development and fine-tuning
* Model evaluation and deployment experiments

It also serves as a **professional showcase** for future freelance opportunities.

---

## Connotation Scale

| Value | Meaning                                 |
| ----- | --------------------------------------- |
| -1.0  | Direct insult / hostility               |
| <0    | Negative / unfriendly tone              |
| 0     | Neutral / factual                       |
| >0    | Positive / friendly tone                |
| +1.0  | Clear flirtation or affectionate intent |

**Internal Note:** `None` is used internally in the annotation UI to indicate sentences **not yet labeled**.
It is **not a semantic label** and is excluded from training and evaluation.

---

## Key Features

### Dialog-Aware Classification

* Sentences are analyzed **in conversational context**
* Supports nuance, sarcasm, and implied intent

### Annotation Interface

* Custom UI for labeling sentence connotations
* Slider interface for continuous values
* Supports iterative dataset improvement

### Data Pipeline

* Raw text ingestion from movie conversations
* Cleaning, normalization, and validation
* Structured output for model training

### Model Development

* Regression-based connotation models
* Fine-tuning for better accuracy
* Evaluation using correlation and error metrics

### Deployment Experiments

* End-to-end inference pipeline
* Planned application to YouTube comments or chat logs

---

## Project Motivation

This project demonstrates:

* End-to-end AI system development
* Dataset creation from scratch
* Production-ready data pipeline design
* Real-world deployment preparation

It is designed to be **both technically rigorous and portfolio-ready**.

---

## Repository Structure

```
data/
├── raw/                 # Original movie lines and conversations
├── processed/           # Cleaned conversations
├── annotations/         # Labeled connotation data

annotation_ui/           # Interface for labeling sentences
pipelines/               # Data cleaning and preparation scripts
models/                  # Model training and evaluation code
deployment/              # Inference and application scripts
README.md
```

---

## Project Status

* Annotation system: In progress
* Dataset creation: Ongoing
* Model training: Planned
* Deployment experiments: Planned

---

## Author

**Youssef Majdoub**
AI / Data Science
Focused on building interpretable, scalable, and practical AI systems
