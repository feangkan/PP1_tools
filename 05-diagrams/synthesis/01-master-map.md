# 01 — Master map: cross-week synthesis (Weeks 1–2)

- **Purpose:** show real relationships between weekly diagrams — not a re-summary of either week
- **Scope:** everything already built in `05-diagrams/week-01/` and `05-diagrams/week-02/`
- **Rule:** this file never introduces a new claim that isn't already sourced in a weekly pack — it only draws the links between existing claims. If you want to trace a node back to its source, check that week's `04-topics-context.md` first.
- **Version:** v01 — rebuild after each new week using `02-concept-index.md`

## Legend

| Element | Meaning |
|---------|---------|
| 🟡 Week 1 only | Claim/cluster unique to Week 1 |
| 🔵 Week 2 only | Claim/cluster unique to Week 2 |
| 🟣 Reconciled | Same claim appeared in both weeks — merged into one node |
| 🟢 Thread | A concept that runs across weeks without being an exact duplicate |
| **→** solid | Primary flow |
| **- - →** dashed | Cross-week relationship |

---

## Diagram

```mermaid
flowchart TB
  subgraph LEGEND["Legend"]
    direction LR
    LG1[🟡 Week 1 only] --- LG2[🔵 Week 2 only]
    LG2 --- LG3[🟣 Reconciled]
    LG3 --- LG4[🟢 Cross-week thread]
  end

  subgraph W1CORE["🟡 Week 1 core loop"]
    direction LR
    W1K[Specialised knowledge] --> W1PWR[Asymmetrical power] --> W1ETH[Ethics + altruism] --> W1TR[Trust] --> W1JUD[Professional judgment] --> W1PUB[Public interest]
    W1PUB -.->|feeds back| W1K
  end

  subgraph W2CORE["🔵 Week 2 core question"]
    direction LR
    W2Q{Six lenses: which organising\nprinciple explains the system?}
  end

  W1CORE ==>|Week 2 asks HOW to organise\nwhat Week 1 established| W2CORE

  subgraph TRAITS["🟣 Reconciled — traits of a profession"]
    TR1[Week 1: Beaton's 11 traits,\nintegrity = head + heart + hand]
    TR2[Week 2: 5-trait evidence method\n— disciplinary knowledge, regulation,\nautonomy, altruism, higher learning]
    TR3[Not the same list — Week 2's 5\nare a working subset of Beaton's 11,\nreframed with an evidence-finding method]
    TR1 --- TR3 --- TR2
  end

  subgraph POWER["🟣 Reconciled — who holds power"]
    PW1[Week 1 Q3: client, practice owner,\nARBV, AACA, university, government]
    PW2[Week 2 Apparatus: same bodies +\nlive poll + Acts/Regs/Codes/Contracts]
    PW3[Week 2 adds the answer Week 1\nleft open: power sits in the\nrelationship between actors, not one]
    PW1 --> PW2 --> PW3
  end

  subgraph ETHICS["🟢 Thread — ethics, altruism, public trust"]
    ET1[Week 1 core loop:\nethics feeds trust feeds judgment]
    ET2[Week 2 Continuum:\nservice ideal + public trust]
    ET3[Week 2 Traits: altruism\nas one of five evidence points]
    ET1 -.-> ET2
    ET1 -.-> ET3
  end

  subgraph LEGIT["🟢 Thread — historical legitimacy"]
    LE1[Week 1 Q4: classic professions\nlaw/medicine/divinity vs neo-pressure]
    LE2[Week 2 Sciulli case: Paris Academie\nprofessionalised 2 centuries before\nEnglish law]
    LE1 -.->|same underlying question,\ndifferent evidence| LE2
  end

  subgraph STRAIN["🟢 Thread — strain forces change"]
    ST1[Week 1 tension: reduced scope/fees,\njudgment does not shrink]
    ST2[Week 2 Kuhn: anomalies accumulate\ninto crisis, then paradigm shift]
    ST1 -.->|commercial pressure is one kind\nof anomaly Kuhn's model predicts| ST2
  end

  subgraph W1ONLY["🟡 Week 1 only — not yet recurring"]
    W1A[Q1: profession vs business]
    W1B[Q2: obligations beyond paying client]
    W1C[Manifesto: judgment over\ncompetency, codes as instruments]
  end

  subgraph W2ONLY["🔵 Week 2 only — not yet recurring"]
    W2A[Continuum spectrum mechanic:\nskill vs judgment-intensity]
    W2B[Divided Line: abstract/physical\nsplit, drawings+contract as instrument]
    W2C[Sciulli structural qualities +\ninstitutional consequences]
    W2D[Tutor design guidance for\nbuilding the diagrams themselves]
  end

  subgraph SPINE["🟣 Reconciled — canonical registration spine"]
    direction LR
    S1[Accredited education] --> S2[Experience / logbook] --> S3[APE exam + interview] --> S4[ARBV registration] --> S5[CPD + PI insurance]
  end

  subgraph A1["🟣 Reconciled — Assessment 1 link"]
    A1N[Disciplinary Matrix —\nonly ONE spine needed, drawn once]
    A1N --> S1
  end

  W1CORE --> TRAITS
  W2CORE --> TRAITS
  W1CORE --> POWER
  W2CORE --> POWER
  W1CORE --> ETHICS
  W2CORE --> ETHICS
  W1CORE --> LEGIT
  W2CORE --> LEGIT
  W1CORE --> STRAIN
  W2CORE --> STRAIN
  W1CORE --> W1ONLY
  W2CORE --> W2ONLY
  TRAITS --> A1N
  POWER --> A1N
  W2ONLY --> A1N
```

---

## What this map is telling you

1. **You've been redrawing the registration spine every week.** It should exist once — this map treats it as the single canonical version. Both weekly packs still keep their own copy (per the scoping rule — each week must stand alone), but going forward, Assessment 1 work should pull from here, not from either week's copy.

2. **Week 2 isn't a new topic — it's Week 1's open question, operationalised.** Week 1 asked "who holds power?" and left it unresolved (Q3 just lists actors). Week 2's apparatus cluster is the direct continuation: same actors, plus a live class poll, plus an actual answer ("power sits in the relationship, not the actor"). That's a genuine argument you can make in Assessment 1 — the two weeks aren't separate content, they're steps in one argument.

3. **The traits lists don't actually match** — worth being precise about this in your matrix rather than treating "5 traits" and "11 traits" as interchangeable. Week 2's 5 are best read as a subset method for finding evidence, not a competing list.

4. **Two threads (legitimacy, strain) are structurally similar but evidentially different** — useful if Assessment 1 wants a "why does the profession need to keep justifying itself" argument, since you now have both a historical case (Sciulli) and a mechanism (Kuhn) to back it, plus your own in-class observation (commercial pressure) as a live example.

---

## Redraw note

This map will get harder to read past 3–4 weeks stacked in one diagram. See `README.md` in this folder for the plan on how synthesis scales.
