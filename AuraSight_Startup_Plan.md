# AuraSight — AR Surgical Navigation System
## Startup Pitch Document & Business Plan
### Version 1.0 | Confidential

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [The Problem](#2-the-problem)
3. [Our Solution — AuraSight Vision](#3-our-solution--aurasight-vision)
4. [Technology Architecture](#4-technology-architecture)
5. [Market Analysis](#5-market-analysis)
6. [Competitive Landscape](#6-competitive-landscape)
7. [SWOT Analysis](#7-swot-analysis)
8. [Business Model](#8-business-model)
9. [Go-to-Market Strategy](#9-go-to-market-strategy)
10. [Roadmap](#10-roadmap)
11. [Financial Projections](#11-financial-projections)
12. [Team & Ask](#12-team--ask)

---

## 1. Executive Summary

**AuraSight** is an AI-powered Augmented Reality (AR) surgical navigation platform that gives surgeons real-time, spatial awareness of the entire operative field — superimposing critical anatomical structures, tool trajectories, and safety alerts directly into their field of view.

> **Mission:** *To make every surgery safer by giving surgeons a second pair of intelligent eyes.*

| Key Metric | Value |
|---|---|
| Global Surgical Navigation Market (2030 est.) | $2B – $6B |
| Preventable surgical errors annually (US) | ~4,000 wrong-site surgeries/yr |
| Existing AR solutions (spine-specific only) | $200K–$300K per hospital |
| AuraSight target price point | $40K–$80K SaaS/yr |
| Current prototype stage | Working real-time hand + tool tracking |

---

## 2. The Problem

### 2.1 Surgical Errors Are Rising

Surgical precision is still largely dependent on the **surgeon's unaided eye and mental model** of the patient's anatomy. This creates catastrophic failure modes:

- **Wrong-site surgeries increased 13% in 2024** (Joint Commission data)
- **68% of these** involved the wrong side of the body
- Sentinel events (serious preventable harm) rose **12–13% in 2024** vs 2023
- **Unintended foreign object retention** (sponges, tools) remains a persistent, preventable issue

### 2.2 The Cognitive Load Crisis

Modern surgery is increasingly complex:
- Surgeons must simultaneously manage anatomical context, tool position, team coordination, and patient vitals
- **They look away from the field repeatedly** to consult 2D imaging monitors (CT/MRI), losing spatial reference each time
- Critical structures (nerve bundles, blood vessels) are invisible beneath tissue — identified only by experience and estimation

### 2.3 Existing Solutions Are Expensive and Narrow

| Solution | Problem |
|---|---|
| Traditional Navigation (Medtronic StealthStation) | Requires looking away at separate screen |
| Augmedics xvision | Spine-only, $200K–$300K capital cost |
| Robotic Systems (da Vinci, Mako) | $1.5M+ hardware, narrow procedure scope |
| Fluoroscopy / X-ray | Radiation exposure, no soft-tissue view |

**No current solution provides whole-field, AI-enhanced, surgeon-first spatial awareness at accessible cost.**

---

## 3. Our Solution — AuraSight Vision

### 3.1 What AuraSight Does

AuraSight is a **software-first AR navigation platform** that:

1. **Maps the entire surgical field in real-time** using depth cameras and structured light projection
2. **Superimposes pre-op imaging** (CT/MRI) onto live operative view via AR headset
3. **Tracks every tool** in the field with sub-millimeter precision using computer vision + sensor fusion
4. **Detects hands and assesses kinematics** — knowing which hand holds which instrument
5. **Alerts surgeons** when tools approach registered critical structures (nerves, vessels)
6. **Logs the entire procedure** for post-op review and medico-legal documentation

### 3.2 The "Whole Surgical Field" Vision

```
Pre-op CT/MRI scan
        ↓
3D Model Registration (patient-specific)
        ↓
Intraoperative AR overlay via headset
        ↓
Real-time tool tracking + critical structure proximity alerts
        ↓
Post-op procedure log + analytics dashboard
```

### 3.3 Key Differentiators

| Feature | AuraSight | Augmedics xvision | Traditional Nav |
|---|---|---|---|
| Hardware-agnostic | YES | NO (proprietary) | NO |
| Whole-field spatial mapping | YES | NO (spine-only) | Partial |
| AI critical structure warnings | YES | Limited | NO |
| Hand & glove tracking | YES | NO | NO |
| SaaS pricing model | YES | NO (CapEx) | NO |
| Procedure logging & analytics | YES | Limited | NO |
| Works without intraoperative CT | YES (vision-based) | NO | NO |

### 3.4 From Prototype to Product

**Current working prototype:**
- Real-time hand kinematic tracking via MediaPipe
- AI tool detection (scissors/knife) via YOLOv8n
- Glove detection (ON/OFF) via skin-color absence analysis
- Live AR HUD with confidence scoring and tool labeling
- GPU-accelerated at 30+ FPS

**Next step vision:**
- Replace webcam with depth camera (Intel RealSense / Azure Kinect)
- Add AR headset output (Meta Quest Pro / Magic Leap 2)
- Integrate DICOM pre-op imaging registration
- Train custom surgical tool detection model

---

## 4. Technology Architecture

### 4.1 Stack Overview

```
PERCEPTION LAYER       INTELLIGENCE LAYER      PRESENTATION LAYER
- Depth Camera         - YOLOv8 (tools)        - AR Headset
- RGB Camera           - MediaPipe (hands)      - Surgeon HUD
- IMU Sensors          - SLAM mapping           - Alert system
- Structured light     - DICOM registration     - Analytics dashboard
                       - Proximity AI
```

### 4.2 Key Technical Components

| Component | Technology | Status |
|---|---|---|
| Tool detection | YOLOv8 custom fine-tuned | Prototype: COCO classes |
| Hand kinematic tracking | MediaPipe HandLandmarker | Working |
| Spatial mapping | SLAM + depth fusion | Roadmap |
| DICOM registration | ICP algorithm + fiducials | Roadmap |
| AR rendering | OpenXR SDK / Unity MARS | Roadmap |
| Glove detection | Skin-color absence (HSV) | Working |
| Proximity alerting | Bounding box + distance calc | Working |
| Edge compute | NVIDIA Jetson Orin / RTX Mobile | Roadmap |

### 4.3 Hardware Requirements (Target Build)

| Component | Specification |
|---|---|
| AR Headset | Meta Quest Pro / Magic Leap 2 |
| Depth Camera | Intel RealSense D435i or Azure Kinect |
| Compute Unit | NVIDIA Jetson Orin (OR-mounted) |
| Connectivity | Local Wi-Fi 6 (no cloud in OR) |

---

## 5. Market Analysis

### 5.1 Total Addressable Market (TAM)

| Segment | 2024 Size | CAGR | 2030 Projection |
|---|---|---|---|
| Global Surgical Navigation Systems | ~$1.8B | 12–15% | ~$4.5B |
| AR/VR in Healthcare | ~$5.1B | 25%+ | ~$19B |
| AI-powered Computer-Aided Surgery | ~$1.2B | 20%+ | ~$3.7B |
| **AuraSight TAM (overlap)** | **~$800M** | **18%** | **~$2.2B** |

### 5.2 Serviceable Addressable Market (SAM)

- India: ~1,200 hospitals with advanced surgical suites
- Southeast Asia: ~800 advanced-tier hospitals
- SAM: ~2,000 hospitals × avg. ₹50L/year = **~₹1,000Cr ARR potential**

### 5.3 Target Customer Segments

```
Priority 1: Tier-1 private hospitals (Apollo, Fortis, Max, Manipal)
Priority 2: Medical colleges & teaching hospitals
Priority 3: Government flagship hospitals (AIIMS network)
Priority 4: International expansion (Southeast Asia, Middle East)
```

### 5.4 India-Specific Opportunity

| Factor | Advantage |
|---|---|
| Surgical volume | 50M+ procedures/year |
| Medical tourism | $9B industry demands precision documentation |
| Cost sensitivity | No $300K CapEx — SaaS model disrupts |
| Regulatory | CDSCO pathway faster than FDA/CE Mark |
| Tech talent | Best-in-class CV/AI talent pool |

---

## 6. Competitive Landscape

### 6.1 Competitor Matrix

| Company | Product | Geography | Price | Specialty | Stage |
|---|---|---|---|---|---|
| Augmedics | xvision Spine | US/EU | $200–300K | Spine only | Commercial |
| Medivis | AR Surgical Platform | US | ~$150K | Neuro/Ortho | Commercial |
| Proprio | Paradigm | US | Undisclosed | Spine | Commercial |
| Pixee Medical | AR Ortho | EU | Undisclosed | Orthopedics | Commercial |
| Novarad | VisAR | US | ~$100K | General | Commercial |
| Brainlab | Mixed Reality Viewer | Global | $250K+ | Neuro | Commercial |
| **AuraSight** | **Whole-field AI Nav** | **India-first** | **~$50K SaaS** | **General** | **Prototype** |

### 6.2 Our Unfair Advantages

1. **Software-first**: No proprietary hardware lock-in
2. **India-first pricing**: SaaS at 5–10x cheaper than Western competitors
3. **Whole-field**: Not limited to one anatomy type
4. **AI + AR convergence**: Multi-modal (hand tracking + tool detection + anatomical overlay)
5. **Prototype validated**: Working system built in weeks, not years

---

## 7. SWOT Analysis

### 7.1 Strengths

| | Strength | Detail |
|---|---|---|
| S1 | **Working Prototype** | Real-time hand tracking, tool detection, glove sensing — proven feasibility |
| S2 | **Software-First Architecture** | Hardware-agnostic design, lower capex and time-to-market |
| S3 | **India Cost Advantage** | 70–80% lower R&D cost vs US/EU competitors |
| S4 | **AI/CV Expertise** | YOLOv8, MediaPipe, GPU-accelerated computer vision |
| S5 | **Whole-Field Vision** | No competitor addresses general surgery navigation at this breadth |
| S6 | **Glove Detection** | Novel skin-tone-based approach not seen in competitors |
| S7 | **Lower Regulatory Barrier** | CDSCO pathway faster and cheaper than FDA 510(k) or CE Mark |

### 7.2 Weaknesses

| | Weakness | Mitigation |
|---|---|---|
| W1 | **No DICOM integration yet** | Roadmap item — partner with radiology software vendors |
| W2 | **No AR headset output** | Phase 2 using existing headset SDKs (OpenXR) |
| W3 | **Webcam vs depth camera** | Replace with RealSense/Kinect in next hardware iteration |
| W4 | **No surgical dataset for fine-tuning** | Hospital data partnership for annotated instrument images |
| W5 | **Small founding team** | Strategic hiring plan underway |
| W6 | **No regulatory clearance** | Begin CDSCO process in Year 1 |
| W7 | **No clinical validation data** | Design IRB-approved clinical study as Year 1 priority |

### 7.3 Opportunities

| | Opportunity | Detail |
|---|---|---|
| O1 | **Growing Indian private healthcare** | Apollo, Fortis, Max expanding aggressively — demand for OR innovation |
| O2 | **Medical tourism boom** | International patients expect technology-forward hospitals |
| O3 | **AI in healthcare investment surge** | $45B+ invested globally in health AI (2024) |
| O4 | **Acquisition validation** | VB Spine acquired Augmedics in 2026 — exit model proven |
| O5 | **Government digital health** | PM-ABHIM, ABDM creating hospital digitization funding |
| O6 | **Surgical training sub-market** | AR surgical education is a $2B+ opportunity |
| O7 | **Post-op analytics** | Procedural data logging is a separate billable revenue stream |
| O8 | **HoloLens 2 discontinuation** | Competition has hardware uncertainty — we are HW-agnostic |

### 7.4 Threats

| | Threat | Mitigation |
|---|---|---|
| T1 | **Medtech giants entering AR** | Medtronic, Stryker have deep pockets — differentiate on price & breadth |
| T2 | **Regulatory delays** | Start CDSCO process early; target Class B classification |
| T3 | **Hospital adoption inertia** | Surgeon champion program; start with early adopters |
| T4 | **Liability / medico-legal risk** | Frame as decision-support tool, not autonomous decision-maker |
| T5 | **Data privacy in OR** | Local compute only — no video leaves hospital network |
| T6 | **Surgeon resistance** | Co-design with surgeons; make HUD invisible/intuitive |
| T7 | **Deep tech funding winter** | Focus on early revenue; lean prototype-to-pilot model |

---

## 8. Business Model

### 8.1 Revenue Streams

| Stream | % of Revenue | Description |
|---|---|---|
| SaaS Subscription | 60% | ₹30–50L/year per hospital (software + updates + support) |
| Hardware Lease | 20% | Depth cameras, compute units — leased, not sold |
| Procedure Analytics Platform | 15% | Post-op dashboards, hospital benchmarking |
| Training & Simulation | 5% | Surgical training modules, medical college licensing |

### 8.2 Pricing Tiers

| Tier | Target | Annual Price | Features |
|---|---|---|---|
| **Starter** | Small hospitals / clinics | ₹15L / $18K | 1 OR, basic tool tracking, HUD |
| **Professional** | Mid-tier private hospitals | ₹35L / $42K | 3 ORs, DICOM integration, analytics |
| **Enterprise** | Apollo/Fortis/AIIMS level | ₹65L / $78K | Unlimited ORs, API access, custom AI models, training |

### 8.3 Unit Economics (Year 3 Target)

| Metric | Value |
|---|---|
| Average Contract Value (ACV) | ₹40L ($48K) |
| Cost to Serve (CTS) | ₹8L ($10K) |
| Gross Margin | ~80% |
| Customer Acquisition Cost (CAC) | ₹12L ($14K) |
| Lifetime Value (5-year avg.) | ₹2Cr ($240K) |
| LTV/CAC Ratio | 16:1 |

---

## 9. Go-to-Market Strategy

### 9.1 Phase 1 — Seed & Validate (Months 1–12)

**Target:** 3 pilot hospitals in Tier-1 Indian cities

- Direct sales through surgical department heads
- Free 6-month pilot in exchange for clinical data and testimonials
- Target early adopters: AIIMS Delhi, Apollo Chennai, Fortis Gurgaon
- Key milestone: 1 peer-reviewed publication with clinical outcomes data

### 9.2 Phase 2 — Scale India (Year 2–3)

**Target:** 50 hospitals

- Distribution partnerships with medical equipment distributors (HLL Lifecare, Wipro GE)
- Major surgical conferences (IAGES, ASICON, ISA)
- Hospital chain deals (Apollo ~70 hospitals, Fortis ~28)
- PR narrative: "First Made-in-India AR Surgical System"

### 9.3 Phase 3 — International Expansion (Year 3–5)

**Target:** Southeast Asia, Middle East, Africa

- India pricing as competitive advantage in cost-sensitive markets
- FDA 510(k) / CE Mark pursuit for eventual US/EU entry
- OEM partnership with large medtech player for global distribution

### 9.4 Marketing Playbook

| Tactic | Rationale |
|---|---|
| Surgeon KOL program | Surgeons trust surgeons — identify 10 champion early adopters |
| Conference live demonstrations | AR demo is the best sales tool |
| Clinical outcomes data | Published studies = procurement committee approval |
| Medico-legal angle | Position as liability reduction tool for administrators |
| Surgical education | Residency training = next generation of loyal users |

---

## 10. Roadmap

### 10.1 Development Milestones

| Quarter | Milestone |
|---|---|
| 2025 Q2 | ✅ Prototype: Real-time CV navigation (DONE) |
| 2025 Q2 | ✅ YOLOv8 tool detection + hand tracking + glove detection |
| 2025 Q3 | Depth camera integration (Intel RealSense) |
| 2025 Q3 | 3D surgical field mapping (SLAM) |
| 2025 Q3 | Custom surgical instrument dataset (500+ images) |
| 2025 Q4 | AR headset output (Meta Quest Pro SDK) |
| 2025 Q4 | DICOM image ingestion + 3D reconstruction |
| 2025 Q4 | CDSCO regulatory filing |
| 2026 Q1 | Pilot deployment: Hospital 1 (simulated OR) |
| 2026 Q1 | IRB clinical study protocol approval |
| 2026 Q2 | Live OR pilot: 3 hospitals |
| 2026 Q2 | First clinical outcomes data + Series A fundraise |
| 2027 | 50 hospitals, India leadership, Southeast Asia launch |

### 10.2 Regulatory Roadmap

| Milestone | Timeline | Estimated Cost |
|---|---|---|
| CDSCO Class B registration (India) | 12–18 months | ₹25–40L |
| CE Mark (EU) | 24–36 months | ₹1–2Cr |
| FDA 510(k) (US) | 24–36 months | ₹2–4Cr |

---

## 11. Financial Projections

### 11.1 Revenue Forecast

| Year | Hospitals | ARR (INR) | ARR (USD) |
|---|---|---|---|
| Year 1 | 3 (pilots, free) | ₹0 | $0 |
| Year 2 | 12 paying | ₹4.8Cr | ~$580K |
| Year 3 | 45 | ₹18Cr | ~$2.2M |
| Year 4 | 120 | ₹48Cr | ~$5.8M |
| Year 5 | 280 | ₹112Cr | ~$13.5M |

### 11.2 Funding Requirements

| Round | Amount | Primary Use | Timeline |
|---|---|---|---|
| **Pre-Seed / Angel** | ₹1.5Cr ($180K) | Hardware + team (4 FTE) + CDSCO filing | Now |
| **Seed** | ₹6Cr ($720K) | AR headset SDK, clinical pilots, 10-person team | Month 12 |
| **Series A** | ₹25Cr ($3M) | Scale to 50 hospitals, regulatory, international BD | Month 24 |

### 11.3 Cost Structure (Year 2)

| Category | % of Cost |
|---|---|
| Engineering & R&D | 45% |
| Sales & Marketing | 25% |
| Clinical & Regulatory | 15% |
| G&A / Operations | 15% |

---

## 12. Team & Ask

### 12.1 Target Founding Team (10 people)

| Role | Count |
|---|---|
| Computer Vision / Deep Learning Engineers | 3 |
| Clinical Advisor / Surgeon Co-founder | 1 |
| Regulatory Affairs Specialist | 1 |
| Sales / Hospital Relations | 2 |
| AR/XR Software Engineers | 2 |
| CEO / Strategy | 1 |

### 12.2 The Ask

> **Seeking ₹1.5 Crore in Pre-Seed / Angel Funding**
> **In exchange for: 8–12% equity**

**Use of funds:**
- ₹40L — Hardware (depth cameras, AR headsets for development)
- ₹60L — Team salaries (6 months runway, 4 FTE)
- ₹25L — CDSCO regulatory filing
- ₹15L — Clinical study setup costs
- ₹10L — IP filing (2 provisional patents)

### 12.3 Why Now

1. Surgical errors are rising year-over-year — documented urgency
2. AR hardware is mature (Meta Quest Pro, Magic Leap 2)
3. AI is proven — foundation models make custom surgical AI feasible in months
4. India private healthcare capex is at all-time high
5. Competition is expensive — we enter with 5x cost advantage
6. Augmedics exit in 2026 validates the acquisition path

---

## Appendix: Key Data Sources

| Data Point | Source |
|---|---|
| Wrong-site surgeries +13% in 2024 | The Joint Commission Sentinel Event Database |
| Augmedics xvision pricing $200–300K | NIH/PubMed clinical studies |
| Surgical navigation market $4.5B by 2030 | Grand View Research, GM Insights |
| HoloLens 2 discontinued | Microsoft official support notice |
| Augmedics acquired by VB Spine | Glass Almanac, 2026 |
| India surgical volume 50M+/year | WHO, Ministry of Health India |

---

*AuraSight — Seeing Beyond the Incision*
*Pitch Document v1.0 | March 2026 | Confidential & Proprietary*
