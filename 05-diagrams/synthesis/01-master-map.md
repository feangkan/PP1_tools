# 01 — Master map: cross-week synthesis (Weeks 1–3)

- **Purpose:** show real relationships between weekly diagrams — not a re-summary of any single week
- **Scope:** everything already built in `05-diagrams/week-01/`, `05-diagrams/week-02/`, `05-diagrams/week-03/`
- **Rule:** this file never introduces a new claim that isn't already sourced in a weekly pack — it only draws the links between existing claims. If you want to trace a node back to its source, check that week's `04-topics-context.md` first.
- **Version:** v02 — rebuilt 2026-08-10, stacking Week 3 onto the existing Weeks 1–2 map. Rebuild again after each new week using `02-concept-index.md`.
- **Zoning:** this map is the **temporal zoning** layer — each week (W1CORE/W2CORE/W3CORE) is its own zone, kept in its own native layout type (Week 1 = circular core loop, Week 2 = radial six-lens hub, Week 3 = linear history→mechanism spine) rather than forced into one shape. Threads/reconciled clusters are the cross-links connecting those zones. See `08-diagram-style/STYLE_GUIDE.md` "Composite layering" for the full method.

## Legend

| Element | Meaning |
|---------|---------|
| 🟡 Week 1 only | Claim/cluster unique to Week 1 |
| 🔵 Week 2 only | Claim/cluster unique to Week 2 |
| 🟠 Week 3 only | Claim/cluster unique to Week 3 |
| 🟣 Reconciled | Same claim appeared in more than one week — merged into one node |
| 🟢 Thread | A concept that runs across weeks without being an exact duplicate |
| **→** solid | Primary flow |
| **- - →** dashed | Cross-week relationship |
| **==>** bold | Week-to-week progression (this week operationalises the last) |

---

## Diagram

```mermaid
flowchart TB
  subgraph LEGEND["Legend"]
    direction LR
    LG1[🟡 Week 1 only] --- LG2[🔵 Week 2 only]
    LG2 --- LG3[🟠 Week 3 only]
    LG3 --- LG4[🟣 Reconciled]
    LG4 --- LG5[🟢 Cross-week thread]
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

  subgraph W3CORE["🟠 Week 3 core question"]
    direction LR
    W3Q{"Why does the Act exist? —\ngives legal form to\nknowledge, authority, responsibility"}
  end

  W1CORE ==>|Week 2 asks HOW to organise\nwhat Week 1 established| W2CORE
  W2CORE ==>|Week 3 shows the actual\nlegal mechanism the organising\nframeworks were pointing at| W3CORE

  subgraph TRAITS["🟣 Reconciled — traits of a profession"]
    TR1[Week 1: Beaton's 11 traits,\nintegrity = head + heart + hand]
    TR2[Week 2: 5-trait evidence method\n— disciplinary knowledge, regulation,\nautonomy, altruism, higher learning]
    TR3[Not the same list — Week 2's 5\nare a working subset of Beaton's 11,\nreframed with an evidence-finding method]
    TR4[Week 3: traits become enforceable\nAct clauses — CPD, sign-off rule,\nconflict-of-interest disclosure,\nduty to resign a contract]
    TR1 --- TR3 --- TR2
    TR2 -->|Week 3 supplies the legal\nclause behind each trait| TR4
  end

  subgraph POWER["🟣 Reconciled — who holds power"]
    PW1[Week 1 Q3: client, practice owner,\nARBV, AACA, university, government]
    PW2[Week 2 Apparatus: same bodies +\nlive poll + Acts/Regs/Codes/Contracts]
    PW3[Week 2 adds the answer Week 1\nleft open: power sits in the\nrelationship between actors, not one]
    PW4[Week 3: explains WHY the apparatus\nhas this shape — Institute advances\nthe discipline, Board holds\naccountability; now fragmented further]
    PW1 --> PW2 --> PW3
    PW3 -->|Week 3 explains the\nhistorical origin of this split| PW4
  end

  subgraph ETHICS["🟢 Thread — ethics, altruism, public trust"]
    ET1[Week 1 core loop:\nethics feeds trust feeds judgment]
    ET2[Week 2 Continuum:\nservice ideal + public trust]
    ET3[Week 2 Traits: altruism\nas one of five evidence points]
    ET4["Week 3: legal teeth — conflict of\ninterest disclosure, duty to RESIGN\na contract rather than breach the\nAct, fire-isolated-stair case"]
    ET1 -.-> ET2
    ET1 -.-> ET3
    ET3 -.->|thread gets concrete\nlegal mechanism| ET4
  end

  subgraph CLIENTROOM["🟣 Reconciled — RESOLVED — obligations beyond the paying client"]
    CR1[Week 1 Q2: future occupants,\nneighbours, community,\n\"client not in the room\"\n— left as an open question]
    CR2["Week 3: resolved — architect\n\"ultimately serves the public and\nnot just the paying client\"\n(fire-stair case, duty to withdraw)"]
    CR1 ==>|Week 1's open question\nanswered with an actual\nlegal mechanism| CR2
  end

  subgraph LEGIT["🟢 Thread — historical legitimacy"]
    LE1[Week 1 Q4: classic professions\nlaw/medicine/divinity vs neo-pressure]
    LE2[Week 2 Sciulli case: Paris Academie\nprofessionalised 2 centuries before\nEnglish law]
    LE3["Week 3: RIBA 1834/37 (advance\nknowledge, not license) + Australia's\nfragmented 1856-1929 founding +\nVic statutory registration 1922/23"]
    LE1 -.->|same underlying question,\ndifferent evidence| LE2
    LE2 -.->|third independent\nhistorical case| LE3
  end

  subgraph STRAIN["🟢 Thread — strain forces change"]
    ST1[Week 1 tension: reduced scope/fees,\njudgment does not shrink]
    ST2[Week 2 Kuhn: anomalies accumulate\ninto crisis, then paradigm shift]
    ST3["Week 3: NSW 2024-25 proposal to fold\nthe Architects Act into a Building\nBill — a live, current-events instance\nof the same pattern"]
    ST1 -.->|commercial pressure is one kind\nof anomaly Kuhn's model predicts| ST2
    ST2 -.->|Kuhn's crisis stage,\nhappening in real time| ST3
  end

  subgraph W1ONLY["🟡 Week 1 only — not yet recurring"]
    W1A[Q1: profession vs business]
    W1B[Manifesto: judgment over\ncompetency, codes as instruments]
  end

  subgraph W2ONLY["🔵 Week 2 only — not yet recurring"]
    W2A[Continuum spectrum mechanic:\nskill vs judgment-intensity]
    W2B[Divided Line: abstract/physical\nsplit, drawings+contract as instrument\n— still open, not touched Wk3]
    W2C[Sciulli structural qualities +\ninstitutional consequences]
    W2D[Tutor design guidance for\nbuilding the diagrams themselves]
  end

  subgraph W3ONLY["🟠 Week 3 only — not yet recurring, watch for Week 4+"]
    W3A["Institute vs Board — two connected\nbut distinct bodies (voluntary\nadvancement vs statutory accountability)"]
    W3B["Compliance culture / compliance\nmindset — regulation as an ongoing,\ncultivated mindset, not a one-off gate"]
    W3C["Molander et al.: discretion has a\nstructural side (the space) and an\nepistemic side (the reasoning) —\naccountability needs both kinds\nof measure"]
    W3A -.->|theory explains why\nboth kinds of body exist| W3C
    W3B -.->|compliance culture IS an\nepistemic accountability strategy| W3C
  end

  subgraph SPINE["🟣 Reconciled — canonical registration spine"]
    direction LR
    S1[Accredited education] --> S2[Experience / logbook] --> S3[APE exam + interview] --> S4[ARBV registration] --> S5[CPD + PI insurance]
  end

  subgraph W3REG["🟠 Week 3 — actual mechanism behind the spine"]
    direction LR
    R1[5 statutory requirements] --> R2[3 pathways — APE most common]
    R2 --> R3["APE: logbook/SOPE (3,300hrs) →\nNational Exam Paper → interview"]
  end

  subgraph A1["🟣 Reconciled — Assessment 1 link"]
    A1N[Disciplinary Matrix —\nonly ONE spine needed, drawn once]
    A1N --> S1
  end

  W1CORE --> TRAITS
  W2CORE --> TRAITS
  W3CORE --> TRAITS
  W1CORE --> POWER
  W2CORE --> POWER
  W3CORE --> POWER
  W1CORE --> ETHICS
  W2CORE --> ETHICS
  W3CORE --> ETHICS
  ETHICS --> CLIENTROOM
  W1CORE --> LEGIT
  W2CORE --> LEGIT
  W3CORE --> LEGIT
  W1CORE --> STRAIN
  W2CORE --> STRAIN
  W3CORE --> STRAIN
  W1CORE --> W1ONLY
  W2CORE --> W2ONLY
  W3CORE --> W3ONLY
  TRAITS --> A1N
  POWER --> A1N
  W2ONLY --> A1N
  W3REG -->|supplies the mechanism\nWeeks 1-2 only sketched| SPINE
  W3CORE --> W3REG
  W3ONLY -.->|explains why the ARBV system\nneeds BOTH the Tribunal AND\nCPD/the interview| W3REG
```

---

## What this map is telling you

1. **You've been redrawing the registration spine every week — Week 3 is where it finally gets real detail.** The spine still exists once (canonical), but Week 3 is the first week to actually supply the statutory mechanism behind it: 5 requirements, 3 pathways, and the APE's 3 parts. Treat `W3REG` as the detail layer sitting on top of the same canonical `SPINE`.

2. **Week 3 closes a question Week 1 left open.** Week 1's Q2 asked who an architect is obligated to beyond the paying client (future occupants, neighbours, the public) and left it as a discussion prompt. Week 3's fire-isolated-stair case and the duty-to-withdraw clause answer it with an actual enforceable mechanism — this is a genuinely strong three-week argument for Assessment 1: *here's the claim (Wk1), here's why it matters structurally (Wk2's apparatus), here's the law that enforces it (Wk3)*.

3. **Three threads are now three weeks deep** — ETHICS, LEGIT, and STRAIN each have independent evidence from all three weeks. That's the strongest material for a sustained Assessment 1 argument, because you're not repeating a claim, you're showing it get more concrete each week (abstract principle → organising framework → enforceable clause / live case).

4. **Week 3 also explains *why* the Week 1–2 apparatus has the shape it does.** POWER (Weeks 1–2) listed the actors and located power in their relationships; Week 3's Institute-vs-Board history explains the actual historical reason two separate kinds of body exist at all.

5. **New Week 3 theory (Molander et al.) is a strong candidate lens for the whole map, not just Week 3** — its structural/epistemic accountability split can, in principle, be applied retroactively to explain *why* Week 1's registration spine and Week 2's apparatus need the specific mix of mechanisms they have. Left as "Open" in the concept index rather than forced into a thread — worth testing against Week 4 material before committing to that reading.

---

## Redraw note

This map is still readable as one diagram at 3 weeks. Per the scaling plan in `README.md`, expect to split it into per-thread diagrams (e.g. `ethics-thread.md`, `legit-thread.md`) around Week 5–6, once a fourth and fifth week's worth of clusters would make a single diagram unreadable at a glance.
