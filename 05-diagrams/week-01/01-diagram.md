# 01 — Diagram: Week 01 — What is a Profession?

- **Week:** 01
- **Date:** 2026-07-26
- **Layout:** hybrid (circular core + radial clusters + bottom registration strip)
- **Style:** `08-diagram-style/` — short-form nodes, networked links
- **Sources scoped:** `03-weekly-resources/week-01/` only
- **Version:** v01

## Legend

| Element | Meaning |
|---------|---------|
| 🟡 Main / stage | Core topic or primary cluster |
| ⬜ Expansion | Short-form detail |
| 🟢 Integrated | Beaton / theory / Assessment 1 link |
| **→** solid | Primary flow |
| **- - →** dashed | Relationship / influence |
| **···→** dotted | Feedback loop |
| 🔴 accent | Tension / conflict |

---

## Diagram

```mermaid
flowchart TB
  subgraph LEGEND["Legend"]
    direction LR
    L1[🟡 Main node] --- L2[⬜ Expansion]
    L2 --- L3[🟢 Theory / A1]
  end

  subgraph Q1["Q1 — Profession vs business"]
    P1[Altruism + ethics]
    P2[Learned + specialised]
    P3[Self-regulatory body]
    B1[Profit primary]
    B2[Market / member focus]
    P1 -.- B1
    P2 -.- B2
  end

  subgraph CORE["🟡 Core loop — professional capacity"]
    direction LR
    K[Specialised knowledge] --> PWR[Asymmetrical power]
    PWR --> ETH[Ethics + altruism]
    ETH --> TR[Trust]
    TR --> JUD[Professional judgment]
    JUD --> PUB[Public interest]
    PUB -.->|feeds back| K
  end

  subgraph GREEN["🟢 Beaton / Cheetham-Chivers"]
    G1[11 profession traits]
    G2[Integrity = head + heart + hand]
    G3[Profit OK — not if it trumps altruism]
  end

  subgraph Q2["Q2 — Beyond paying client"]
    O1[Future occupants]
    O2[Neighbours + community]
    O3[Future generations]
    O4[Client not in room]
  end

  subgraph Q3["Q3 — Who holds power?"]
    PW1[Client / developer]
    PW2[Practice owners]
    PW3[ARBV / registration]
    PW4[AACA / accreditation]
    PW5[University + institutes]
    PW6[Government / NCC]
    PW7[ARBV absorption proposal?]
  end

  subgraph Q4["Q4 — Classic ↔ neo"]
    C1[Classic: law · medicine · divinity]
    C2[Architecture = design profession]
    C3[Neo-profession pressure]
    C1 --> C2 --> C3
  end

  subgraph TENSION["🔴 Q5 — Commercial vs professional"]
    T1[Reduced scope + fees]
    T2[Judgment does not shrink]
    T3[Student: speed vs care]
    T4[Innovation for profit vs public benefit]
    T1 --> T2
  end

  subgraph MANIFESTO["⬜ Week 1 manifesto themes"]
    M1[Judgment over competency alone]
    M2[Registration = entrusted judgment]
    M3[Codes as instruments — not barriers]
    M4[Collective knowledge]
    M5[Measure by public contribution]
  end

  subgraph SPINE["Bottom strip — A1 registration spine VIC draft"]
    direction LR
    S1[Accredited education] --> S2[Experience / logbook]
    S2 --> S3[APE exam + interview]
    S3 --> S4[ARBV registration]
    S4 --> S5[CPD + PI insurance]
  end

  subgraph A1["🟢 Assessment 1 link"]
    A1N[Disciplinary Matrix]
    A1N --> S1
  end

  Q1 --> CORE
  GREEN --> CORE
  CORE --> Q2
  CORE --> Q3
  Q3 --> TENSION
  CORE --> Q4
  MANIFESTO --> CORE
  CORE --> SPINE
  TENSION -.->|limits| JUD
  Q2 -->|depends upon| JUD
  PW3 -->|enables| S4
  PW4 -->|influences| S1
```

---

## Primary links to say aloud

1. **Specialised knowledge → power → ethics** — Beaton: asymmetrical knowledge creates duty, not just expertise.  
2. **Professional judgment** — centre of Week 1 manifesto; not reducible to competency checklists alone.  
3. **Obligations beyond fee-payer** — future occupants and public are “clients not in the room.”  
4. **Power cluster** — clients and firms hold commercial power; ARBV/AACA hold regulatory power; tension when scope/fees cut but judgment expected.  
5. **Registration spine** — draft strip for Assessment 1; will be refined with exact gateways/times.  

---

## Redraw notes (v02)

- Hand-draw in Proprac yellow/white/green style when ready for class.  
- Add only verified ARBV/AACA timeframes from later weeks.  
- Mark your **position** on classic ↔ neo with one blue label.
