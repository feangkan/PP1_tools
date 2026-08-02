# 01 — Diagram: Week 02 — Models for Understanding a Profession

- **Week:** 02
- **Date:** 2026-08-02
- **Layout:** hybrid (radial frameworks core + branch clusters + bottom A1 spine)
- **Style:** `08-diagram-style/` — short-form nodes, networked links
- **Sources scoped:** `03-weekly-resources/week-02/` only
- **Version:** v01
- **Tutor design brief applied:** see "Design response to tutor email" below

## Legend

| Element | Meaning |
|---------|---------|
| 🟡 Main / stage | Core topic or primary cluster |
| ⬜ Expansion | Short-form detail |
| 🟢 Integrated | Sciulli theory / case study / Assessment 1 link |
| 🔵 Transform | Tutor design guidance shaping how the diagram itself is built |
| **→** solid | Primary flow |
| **- - →** dashed | Relationship / influence |
| **···→** dotted | Feedback loop |
| 🔴 accent | Tension / crisis / unresolved question |

---

## Diagram

```mermaid
flowchart TB
  subgraph LEGEND["Legend"]
    direction LR
    L1[🟡 Main node] --- L2[⬜ Expansion]
    L2 --- L3[🟢 Theory / case]
    L3 --- L4[🔵 Transform]
  end

  subgraph CORE["🟡 Core — organising the profession as a system"]
    direction LR
    FR[6 organising frameworks] --> Q{Which lens reveals\nwhich part of the system?}
  end

  subgraph TRAITS["🟡 Traits model — evidence pointers"]
    T1[Disciplinary knowledge → Acumen, journals, canon]
    T2[Regulation → ARBV, Architects Act, NCC]
    T3[Autonomy → judgment, signing, sign-off]
    T4[Altruism → code of conduct, client not in room]
    T5[Higher learning → AQF master's-level inquiry]
    T6[Priority order is contested — uni vs practice vs AIA]
  end

  subgraph CONTINUUM["🟡 Continuum model — Goode and Moore"]
    C1[Occupation ←→ profession spectrum]
    C2[Knowledge base + service ideal + public trust]
    C3[Skilled trade = repeatable competence]
    C4[Profession = judgment on a novel subject]
    C5[Nurse ↔ doctor boundary is shifting]
    C6[Builder ↔ architect boundary overlaps]
    C1 --> C2
    C3 -.->|contrast| C4
  end

  subgraph APPARATUS["🟡 Apparatus — institutions, laws, power"]
    AP1[ARBV, AACA, AIA, university, unions]
    AP2[Acts, Regulations, Codes, Contracts]
    AP3[Who holds most power: client, builder,\narchitect, regulator, finance?]
    AP4[Influence may sit in relationships,\nnot single actors]
    AP5[Bodies renew every 5–6 years —\npower is not fixed]
    AP1 --> AP3
    AP2 --> AP3
  end

  subgraph KUHN["🔴 Kuhn — Structure of Scientific Revolutions"]
    K1[Normal practice / business as usual]
    K2[Anomalies accumulate]
    K3[Crisis — cladding, cracked slabs]
    K4[Revolution — contested, incomplete]
    K5[New paradigm shift]
    K6[Class split: normal-ops vs crisis-aware]
    K1 --> K2 --> K3 --> K4 --> K5
    K5 -.->|feeds back| K1
  end

  subgraph DIVIDED["🟡 Plato's Divided Line — abstract ↔ physical"]
    direction LR
    D1[Abstract: laws, codes, disciplinary\nknowledge, IP]
    D2[Instruments: drawings, contract —\ntranslate idea to build]
    D3[Physical: building, materials, client,\nbuilder]
    D1 -->|administered through| D2 --> D3
    D4[Exemplar → award / journal / precedent]
    D3 -->|published, disseminated| D4
    D4 -.->|feeds| D1
  end

  subgraph SCIULLI["🟢 Sciulli — structural + institutional invariance"]
    SC1[8 structural qualities —\nstructured situations, authority,\nfiducial duty, merit, jurisdiction]
    SC2[4 institutional consequences —\nauthority + governance, upgraded\ndiscourse, restrained power,\nsupports democratic design]
    SC3[🟢 Case: Paris visual Academie 1648–80]
    SC4[Meritocratic student competitions —\nnot nepotism or patronage]
    SC5[Gentlemen once designed their own\nresidential architecture — pre-professional]
    SC6[Professionalised 2 centuries before\nEnglish law or architecture]
    SC1 --> SC2
    SC3 --> SC1
    SC4 --> SC3
    SC5 -.->|backdrop contrast| SC3
  end

  subgraph TUTOR["🔵 Design response to tutor email (Week 3 recap)"]
    TU1[Frameworks to think WITH,\nnot templates to copy]
    TU2[Diagram must reveal an argument,\nnot list components]
    TU3[Registration pathway = spine,\neverything else attaches]
    TU4[Readable at 3 distances:\nfar / medium / close]
    TU5[Precedents: MVRDV, OMA/Koolhaas\nspine, Neurath Isotype]
    TU1 --> TU2 --> TU3
    TU4 -.->|governs layout| CORE
  end

  subgraph SPINE["Bottom strip — A1 registration spine v02"]
    direction LR
    S1[Accredited education] --> S2[Experience / logbook]
    S2 --> S3[APE exam + interview]
    S3 --> S4[ARBV registration]
    S4 --> S5[CPD + PI insurance]
  end

  subgraph A1["🟢 Assessment 1 link"]
    A1N[Disciplinary Matrix —\nchoose organising lens]
    A1N --> S1
  end

  CORE --> TRAITS
  CORE --> CONTINUUM
  CORE --> APPARATUS
  CORE --> KUHN
  CORE --> DIVIDED
  CORE --> SCIULLI
  TUTOR --> A1N
  TRAITS -->|feeds| S1
  APPARATUS -->|enables| S4
  KUHN -.->|limits/challenges| DIVIDED
  SCIULLI -->|structural evidence for| A1N
  DIVIDED -->|instrument for| SPINE
```

---

## Primary links to say aloud

1. **Six frameworks, one question** — traits, continuum, apparatus, Kuhn, divided line, and Sciulli's invariance model all answer *"what organising principle explains the profession as a system?"* — that is this week's actual topic, per the tutor's Week 3 recap email.
2. **Continuum sharpens the traits model** — traits list *qualities*; the continuum asks *how much judgment vs repeatable competence* a role requires, which is what separates architect from draftsperson, doctor from nurse.
3. **Apparatus is where power actually sits** — not fixed in one actor; it moves between client, builder, regulator, and finance, and changes as institutional leadership renews.
4. **Kuhn explains *why* the profession should not stay static** — anomalies (cladding, cracked slabs) becoming crisis is the mechanism for paradigm change, not personal failure.
5. **Divided Line shows the architect's instruments** — drawings and contracts sit *on* the line, translating abstract knowledge into physical building; without them nothing can be built or valued.
6. **Sciulli's case (Paris visual Academie) is the closest historical parallel to architecture's own registration story** — a meritocratic, competition-based credentialing system built two centuries before English law professionalised.

---

## Design response to tutor email (Jack Stirling, "Welcome to Week 3")

This diagram deliberately implements the tutor's Week 3 preview email:

- **"Frameworks to think with, not templates to copy"** → each cluster above is used as a *lens*, not copied wholesale; the Sciulli case is worked through rather than just listed.
- **"Registration pathway should act as the spine"** → the bottom strip stays the organising spine; every framework cluster links back to it rather than floating independently.
- **Three reading distances** → far (six-framework radial core is legible as a shape), medium (cluster titles + primary links), close (expansion nodes + case study detail).
- **Precedents (MVRDV, OMA/Koolhaas, Neurath Isotype)** → informs the *next* hand-drawn iteration (v02): a single strong organising spine (Koolhaas-style "stack/section") with nested detail (Isotype-style legibility), not a flat list of boxes.

---

## Redraw notes (v02)

- Hand-draw with **one dominant spine** (registration pathway, Koolhaas-style) rather than six equal radial branches — tutor flagged flat lists as a risk.
- Test the diagram at arm's length — if the six-framework shape isn't legible without reading labels, simplify.
- Confirm the count of Sciulli's structural qualities against the source paper before finalising node count (this draft groups some together for space; the PDF itself lists eight separately — see `04-topics-context.md`).
- Consider dropping Traits and Continuum into one merged cluster in v02, since both largely restate the Week 1 argument — the tutor's recap treats Week 2 as "Conceptual Frameworks" (Kuhn, Divided Line, Apparatus, Sciulli), not a Week 1 repeat.
