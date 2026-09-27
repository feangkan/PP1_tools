# 01 — Diagram: SOH parties, instruments and tracing documents

- **Assessment:** `../../02-assessment-tasks/assessment-3-brief.md`
- **Date:** 2026-09-26 (v01)
- **Layout:** hybrid — a **top→down contract triangle** (client / architect / contractor, with the instrument named on each edge), a **consultant + regulator** side zone, and a **tracing-documents strip** along the bottom that every change runs through. Built from the tutor's Miro clusters (`../../03-weekly-resources/week-09/miro-board-parties-instruments.jpg`).
- **Sources:** A3 brief; the SOH project-information extract shown in the brief's video still (Utzon engaged Mar 1957; Arup engaged directly by client; Stage I Civil & Civic; Stage II & III Hornibrook). Historical names/dates carry `[verify]` until checked against the supplied SOH PDF.
- **Style:** `../../08-diagram-style/STYLE_GUIDE.md`

## Legend

| Element | Meaning |
|---------|---------|
| 🟡 Party (contracting) | Signs a contract |
| ⬜ Party (non-contracting) | Acts in the project but isn't party to that contract |
| 🟥 Instrument | The contract / agreement / form |
| 🟢 Tracing document | Where a change shows up (cost, time, drawings) |
| **→** solid | Contractual relationship (named instrument) |
| **- - →** dashed | Administers / advises / coordinates (no contract between them) |
| **···→** dotted | Regulates / reviews |

## Diagram

```mermaid
flowchart TB
  classDef party fill:#F4D35E,color:#1a1a1a,stroke:#8a6c1f,stroke-width:2px;
  classDef nonparty fill:#ffffff,color:#1a1a1a,stroke:#999,stroke-width:1px;
  classDef instr fill:#E07A5F,color:#1a1a1a,stroke:#7a3b28,stroke-width:1px;
  classDef trace fill:#8FBF8F,color:#1a1a1a,stroke:#3f5a3f,stroke-width:1px;
  classDef factor fill:#9EC1D9,color:#1a1a1a,stroke:#345070,stroke-width:1px;

  CL["CLIENT\nNSW Government\n(Premier · Minister for Public Works / PWD)\n[verify who signs]"]:::party
  AR["ARCHITECT\nJørn Utzon 1957–66\n→ Hall · Todd · Littlemore 1966–73"]:::party
  CO["CONTRACTOR\nStage I Civil & Civic\nStage II/III Hornibrook"]:::party

  CAA["CAA 2024\n(full services)"]:::instr
  SW["ABIC Simple Works 2018\n+ forms SW-11/12/13/14/31/40/42/49"]:::instr
  LTR["Intro letter\nUtzon → NSW Govt"]:::instr

  CL -->|signs| CAA -->|engages| AR
  CL -->|signs| SW -->|engages| CO
  AR -.->|"administers — NOT a party\n(instructs · assesses · certifies)"| SW
  AR -.->|opens the relationship| LTR -.-> CL

  subgraph SIDE["Consultants + regulators"]
    ENG["ENGINEER\nOve Arup & Partners\nengaged DIRECTLY by client\nstructural · electrical · HVAC · acoustic"]:::nonparty
    QS["Quantity surveyor\n[A] / [verify]"]:::nonparty
    REG["REGULATORY BODIES\nbuilding authority [verify]\n+ (contemporary) ARBV"]:::nonparty
  end
  CL -->|separate engagement| ENG
  AR -.->|"coordinates — but no contract\nover the engineer"| ENG
  REG -.->|regulates / reviews practice| AR

  subgraph TRACE["Tracing documents — where every change must show up"]
    direction LR
    T1["Design / construction\ndocumentation set"]:::trace
    T2["Cost plan /\nquantities"]:::trace
    T3["Gantt chart /\nprogramme"]:::trace
    T4["Document\nRegister"]:::trace
  end
  AR --> T1
  QS --> T2
  CO --> T3
  AR --> T4

  subgraph FACT["Factors (tutor's board — Scope in red)"]
    direction LR
    F1[SCOPE]:::factor --- F2[TIME]:::factor --- F3[COST]:::factor --- F4[QUALITY]:::factor
  end
  T1 -.-> F1
  T3 -.-> F2
  T2 -.-> F3
  T1 -.-> F4
```

## What the map makes visible

1. **The architect administers a contract they are not party to.** Under ABIC SW the contract is client ↔ contractor; the architect instructs, assesses and certifies. That's the *integrity, fairness and impartiality* duty the brief quotes from Architects Regulations 2015 reg 5.2 — the core Part B mechanism.
2. **The engineer was engaged directly by the client**, not through the architect. The architect coordinates a consultant they have no contract with — scenario 3's engineer-vs-architect conflict lives on this dashed line. (Link to A2: this is *responsibility without authority* in a concrete case — use only if it helps Part B, don't import the frame.)
3. **One event produces two change chains.** A redesign after construction starts changes the **construction contract** (SW-12 → SW-14 → SW-11 → SW-31) *and* the **architect's own services** (extra design work under the CAA — rubric C2). The file needs both. See `03-change-chain.md`.
4. **The client changed.** Cahill (d. 1959) → later premiers → Askin government 1965 with Davis Hughes as Minister for Public Works `[verify]`. A change of client representative is itself a change the file should record.

## Gaps

- Who signs for the client in our file (Premier? Minister? SOH Executive Committee?) — decide + declare `[A]`.
- Was there a QS on Stage I? `[verify]`
- Which building authority applies historically — or do we treat it contemporarily `[A]`?
