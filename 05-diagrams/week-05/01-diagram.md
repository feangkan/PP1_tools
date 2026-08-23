# 01 — Diagram: Week 05 — Architecture and the Instruments of Law

- **Week:** 05
- **Date:** 2026-08-23
- **Layout:** hybrid — linear three-role spine + radial NCC cluster + left→right 1666 parallel + dotted amendment loop
- **Style:** `08-diagram-style/` (short-form nodes + networked links)
- **Sources scoped:** `03-weekly-resources/week-05/` and lecture slides captured in `02-assessment-tasks/assessment-1-development/week-05-contents.md` (no recording in the repo)

## Legend

| Element | Meaning |
|---------|---------|
| Yellow | Main / stage node |
| White | Expansion (short-form) |
| Green | Assessment 1 / named reading |
| Solid → | Primary flow |
| Dashed - - → | Relationship |
| Dotted ···→ | Feedback / amendment |

**Layout type per zone:** ROLES = linear; NCC = radial; 1666 = timeline parallel; WHO = dotted loop. Cross-links are relationship claims.

---

## Diagram

```mermaid
flowchart TB
  classDef main fill:#F4D35E,color:#1a1a1a,stroke:#8a6c1f,stroke-width:1px;
  classDef theory fill:#8FBF8F,color:#1a1a1a,stroke:#3f5a3f,stroke-width:1px;

  subgraph ROLES["🟡 Architect vs the instrument [linear]"]
    S[Subject: what must I do?]
    I[Interpreter: why does this exist?]
    C[Co-author: who may change it?]
    S --> I --> C
  end
  class S,I,C main

  subgraph NCC["🟡 NCC — measurable translations [radial]"]
    N0[Code enables buildings to exist]
    N1[A6 class + storeys → Type A/B/C]
    N2[C2D2 type determines construction]
    N3[F5D2 room heights 2.4 / 2.1 / 2.7]
    N4[F6 light 10% / 5% · F6 air]
    N0 --> N1
    N0 --> N2
    N0 --> N3
    N0 --> N4
  end
  class N0 main

  subgraph PROV["⬜ Law is provisional"]
    P1[Written]
    P2[Interpreted]
    P3[Amended]
    P4[Repealed]
    P1 --> P2 --> P3 --> P4
  end

  subgraph WHO["🟢 Who gets written in [dotted loop]"]
    W1[Lived experience]
    W2[Advocacy]
    W3[Consultation]
    W4[NCC change]
    W5[Future buildings]
    W1 --> W2 --> W3 --> W4 --> W5
    W5 -.-> W1
  end
  class W2,W4 theory

  subgraph CASES["🟢 Cases on the slides / pre-readings"]
    G1[Lui: code as battleground / co-authorship]
    G2[Bathrooms: 2023 propose → 2025 DTS · May 2026]
    G3[Livable housing: optional becomes ordinary]
    G4[Tight envelope → moisture → new rule]
    G5[Hill carbon limits — pre-reading only]
    G6[Fire Water Building — title slide only]
  end
  class G1,G2 theory

  subgraph THEN["⬜ 1666 London Act ↔ today"]
    T1[Types / rates]
    T2[Type determines construction]
    T3[Min. dimensions]
    T4[Measurable light + air]
    T5[Time · neighbours · disputes · property]
  end

  N0 -->|enables| S
  I -.->|interprets| N0
  C -->|influences| P3
  W2 -->|causes| W4
  G1 -.-> C
  G2 --> W4
  N0 -.->|same four tags| T1
  P3 -.->|feeds back| N0
```

## Key links to say aloud

1. The NCC **enables** buildings to exist — it is not a neutral manual.
2. Advocacy **influences** / **causes** amendment (lived path → NCC change).
3. A new energy rule **causes** a moisture problem — then another rule answers it.
4. The architect moves from **subject** to **interpreter** to **co-author**.

## Version

- v01 — first network from Week 5 slides + pre-reading URLs (2026-08-23)
