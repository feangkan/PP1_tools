# 01 — Diagram: Assessment 1 — The Disciplinary Matrix of Architecture

- **Assessment:** 02-assessment-tasks/assessment-1-brief.md — A1 Disciplinary Matrix + 150-word critical position
- **Date:** 2026-08-20 (v07 — metaphor dropped, see "Redraw notes" below)
- **Layout:** hybrid, composite-layered (see `08-diagram-style/STYLE_GUIDE.md`) — every required topic is its own cluster with its own native layout type, cross-linked by relationship arrows. Cluster names now use the brief's own vocabulary directly (Registration Pathway, Education, Employment, Legislation, Professional Bodies, Ethics & Public Value, Research & Innovation, Procurement, Power Structure) instead of a theme-park metaphor — see "Redraw notes" for why. This file is the **thinking draft** (Mermaid) — see "Translating to the hand-drawn A1" below for how it becomes the actual submission.
- **Sources scoped:** the `05-diagrams/synthesis/01-master-map.md` v03 (Weeks 1–4), the Week 5 pre-readings (`03-weekly-resources/week-05/`), `02-assessment-tasks/procurement-research-note.md` (tagged independent research), and a tutorial whiteboard capture (Trust/Risk + NSCA project-stage process, photographed by the student, added 2026-08-16 — see `04-topics-context.md` for the transcription and flagged ambiguities). No new unsourced claims are introduced here — every node traces to one of those.

## Legend — Diagram Key

| Element | Meaning |
|---------|---------|
| Main cluster (bold border, tinted fill) | Required Assessment 1 topic |
| Plain node | Detail/subtopic inside a cluster |
| Green node | Named theorist, case, or cross-week thread from the synthesis map |
| Blue node, dashed cluster border | Procurement — independent research, not lecture-sourced (tagged) |
| Orange node, "Power Structure" cluster | Critical-position cluster — deliberately drawn with less visual weight than the required topics |
| **→** solid | Primary relationship (enables / depends upon) |
| **- - →** dashed | Relationship / influence (limits / causes) |
| Gate | A real competency or legal checkpoint, not decoration |

**Cross-link categories** (the cross-cluster relationship labels are prefixed with one of these — a plain-text stand-in for coloured line *strokes*: this diagram has 130+ edges, and Mermaid's line-colouring needs an exact numeric index per edge counted across the whole file — one miscount silently recolours the wrong link rather than erroring, so labels carry the category name instead):

| Marker | Category | Covers |
|--------|----------|--------|
| [spine] | Required-topic backbone | Hub → Registration Pathway → each required cluster (education, employment, legislation, professional bodies) |
| [regulation] | Codes, standards, competencies, research | Legislation ↔ Professional Bodies ↔ Ethics & Public Value ↔ Research & Innovation, and the Delivery Process's regulatory gates |
| [practice] | What happens once you're working | Employment ↔ Procurement ↔ Delivery Process |
| [critical] | Power, critique, backstage | Registration Pathway / Legislation / Procurement → Power Structure, and back to the hub question |

**Layout type per cluster**: HUB = radial; REGISTRATION PATHWAY = linear process with gated stages, entrance framing, and re-queue loops; EDUCATION = hierarchy; EMPLOYMENT = network, with PROJECT DELIVERY PROCESS nested inside it as a small linear/iterative sub-process; LEGISLATION = top-down; PROFESSIONAL BODIES = list-network; ETHICS & PUBLIC VALUE = radial; RESEARCH & INNOVATION = left→right timeline; PROCUREMENT = small linear, drawn attached by an unfinished connector; POWER STRUCTURE (critical position) = top-down hierarchy, visually behind everything else. Cross-links are relationship claims, not one uniform flow, per `08-diagram-style/STYLE_GUIDE.md` "Composite layering."

---

## Diagram

```mermaid
flowchart TB
  classDef default fill:#ffffff,color:#1a1a1a,stroke:#999999,stroke-width:1px;
  classDef main fill:#F4D35E,color:#1a1a1a,stroke:#8a6c1f,stroke-width:1px;
  classDef theory fill:#8FBF8F,color:#1a1a1a,stroke:#3f5a3f,stroke-width:1px;
  classDef transform fill:#9EC1D9,color:#1a1a1a,stroke:#345070,stroke-width:1px;
  classDef backstage fill:#E07A5F,color:#1a1a1a,stroke:#7a3b28,stroke-width:1px;
  classDef gate fill:#ffffff,color:#1a1a1a,stroke:#8a6c1f,stroke-width:2px,stroke-dasharray: 3 2;

  subgraph LEGEND["Diagram Key — node colour"]
    direction LR
    K1[Main cluster] --- K2[Subtopic]
    K2 --- K3[Integrated / theory]
    K3 --- K4[Procurement — independent research]
    K4 --- K5[Power Structure — critical position]
  end

  subgraph LINELEGEND["Diagram Key — lines + cross-link markers"]
    direction LR
    LL1[Primary] -->|enables / depends upon| LL2[Flow]
    LL3[Relates] -.->|limits / causes / feedback| LL4[Influence]
    LL5["[spine] backbone · [regulation] codes/standards · [practice] procurement/delivery · [critical] critical position — cross-link label prefix"]
  end
  LEGEND --- LINELEGEND

  subgraph HUB["Organising question [radial hub]"]
    direction LR
    HQ{"What does it take to be\ntrusted with the title\n'Architect' — and trusted\nby whom, for what?"}
    HQ1["Registration is the ONE\ncompulsory pathway required\nby the brief — everything else\nis optional, but shapes what\nthat pathway is actually worth"]
    HQ --> HQ1
  end
  class HQ main

  subgraph RIDE["REGISTRATION PATHWAY — Victoria's path to Architect [linear, gated]"]
    direction LR
    RSIGN1["Framing — TRUST:\nAutonomy · Discretion ·\nAccountability. Every gate\non this pathway tests one of\nthese three, not just\n'knowledge' (tutorial whiteboard)"]
    RSIGN2["Framing — RISK: owed\nto the PUBLIC and to the\nPROFESSION. More knowledge +\nexperience = more risk you're\ntrusted to carry (tutorial\nwhiteboard — see 04-topics-\ncontext.md for a reading note)"]
    RS1["Stage 1: Accredited\neducation (AQF Part 1/2)"]
    RS2["Stage 2: Supervised\nexperience — logbook,\n3,300 hrs / 35 competencies"]
    RS3["Stage 3: APE — National\nExam (80 MCQ) + interview\n(45-60min, probes gaps)"]
    RS4["Stage 4: ARBV\nregistration granted"]
    RS5["Stage 5: CPD + PI\ninsurance — ongoing, loops\nrather than ending"]
    RQ1["Contingency: fail/repeat\nexam, incomplete hours,\ninterstate/overseas mutual\nrecognition — repeat the\nstage, not excluded"]
    RQ2["Excluded from the pathway:\nTribunal finding, discipline\nregister, loss of title"]
    RSIGN1 -.-> RS1
    RSIGN2 -.-> RS1
    RS1 -->|depends upon| RS2 -->|depends upon| RS3 -->|enables| RS4 -->|enables| RS5
    RS3 -.->|limits — fail a gate| RQ1 -.->|re-attempt| RS3
    RS5 -.->|causes, on serious breach| RQ2
    RS5 -->|feeds back into| RS5
  end
  class RS1,RS3,RS4 main
  class RQ2 backstage
  class RSIGN1,RSIGN2 gate

  subgraph APPRENTICELAND["EDUCATION (incl. CPD) [hierarchy]"]
    E1[University / accredited course\n— AQF-governed]
    E2[Graduation → eligible for\nlogbook stage]
    E3[CPD — only mandated\nARBV-wide since ~2022]
    E4["Molander: CPD is a FORMATIVE\nepistemic measure — builds\njudgment before it's tested"]
    E1 --> E2
    E4 -.-> E3
    %% E2's and E3's specific feeds into Registration Pathway (RS1, RS5)
    %% are stated in their own node text and in prose, not as graph edges
    %% back into RIDE — RIDE already reaches every required cluster via the
    %% spine, and a reverse edge here closed a 2-cluster cycle with RIDE.
  end
  class E1 main
  class E4 theory

  subgraph PRACTICE["EMPLOYMENT [network]"]
    P1[Practice / firm — where\nlogged hours are earned]
    P2["Project management — ceded\nby the profession in the\n1960s-70s, now a separate,\nmore lucrative field (Week 4)"]
    P3["ACA — business, procurement,\nemployment conditions"]
    P4[Professionals Australia\n— union]
    P1 -.->|limits, if scope ceded| P2
    P3 -.-> P1
    P4 -.-> P1
  end
  class P1 main
  %% P1's dependency on RS2 (logged hours require Registration Pathway's
  %% experience stage) is stated in prose, not as a graph edge back into
  %% RIDE — same reasoning as APPRENTICELAND above.

  subgraph FLUME["PROJECT DELIVERY PROCESS — nested inside Employment, run once per project [linear, gated, iterative — tutorial whiteboard]"]
    direction LR
    F0["Client + Stakeholders\n→ the Brief"]
    F1["Feasibility (F)"]
    F2["Concept / Sketch\nDesign (SK)"]
    F3["Developed\nDesign (DD)"]
    F4["Construction\nDocumentation (CD)"]
    F5["Contract\nAdministration (CA)"]
    F6["Gate: Town Planning\n(Council) approval"]
    F7["Gate: Building\nSurveyor (BS) sign-off"]
    F8["NSCA competencies span\nBOTH the design process\nAND contract administration\n— not just design skill"]
    F0 -->|depends upon| F1 -->|depends upon| F2 -->|depends upon| F3 -->|depends upon| F4 -->|depends upon| F5
    F2 -.->|limits, until approved| F6
    F4 -.->|limits, until signed off| F7
    F6 & F7 -.->|feeds back into,\nprocess loops rather\nthan runs straight| F0
    F8 -.-> F1
    F8 -.-> F5
  end
  class F1,F4 main
  class F8 theory
  PRACTICE -.->|[practice],\nevery project runs this loop| FLUME
  FLUME -.->|[regulation],\nCouncil + Building\nSurveyor are LEGISLATION's\ncheckpoints, playing out\nproject by project| REGULATION
  RS2 -.->|[practice],\nsame 35 NSCA\ncompetencies, tested here\nin the abstract and\nthere in practice| F8

  subgraph REGULATION["LEGISLATION [top-down]"]
    L1[Architects Act 1991\n+ Regulations]
    L2[Building Act / VBA]
    L3["National Construction Code —\namendable (see RESEARCH &\nINNOVATION, Dan Hill roadmap)"]
    L4[Planning and Environment Act\n/ OVGA / DELWP-VPA]
    L5["Duty to public (s.17-18) +\nduty to resign a contract\nrather than breach the Act\n(fire-isolated-stair case)"]
    L1 --> L5
  end
  class L1,L5 main
  %% L1/L2/L3/L4's role enabling and constraining ARBV registration (RS4)
  %% is stated in prose, not as graph edges back into RIDE — REGULATION
  %% already reaches RIDE's territory via the Delivery Process's Council/
  %% Building-Surveyor gates, and a second reverse edge here closed a
  %% 2-cluster cycle directly with RIDE (on top of that mediated path).

  subgraph GUILD["PROFESSIONAL BODIES [list-network]"]
    G1[AIA — voluntary,\nadvances the discipline]
    G2[ARBV — statutory,\npublic accountability]
    G3[AACA — national competency\nstandard, coordinates boards]
    G4["Parlour · ArchiTeam ·\nArchitects Declare · AASA —\nfill gaps AIA alone can't cover"]
    G5["Bates Smart Award, AIA\ncategories — the RECOGNITION\nmachinery, distinct from G2's\nREGULATION machinery (Week 4)"]
    G1 -.->|contrast| G2
    G4 -.-> G1
    G1 --> G5
  end
  class G1,G2 main

  subgraph TOWNHALL["ETHICS & PUBLIC VALUE — who the profession serves [radial]"]
    T1["Duty beyond the paying\nclient — future occupants,\nneighbours, the public"]
    T2["Loos 1910: before God, no\ngood or bad architects — a\nmatter of degree, not kind"]
    T3["Bailey/Shaw/Bruhn: 'Architecture,\nnot Architects' — recognition\nshould serve public value, not\nmanufacture individual reputation"]
    T4["Stead: searchlight or lantern?\nDoes the profession's own record\nreflect the public it serves?"]
    T1 --> T2 --> T3 --> T4
  end
  class T1,T3 main
  %% T4's point — this is the real test for every cluster in the diagram — is
  %% argued in prose (see "Primary links to say aloud" #6) rather than as
  %% a graph edge back to HQ: that edge closed a cycle through HUB->RIDE->
  %% GUILD->TOWNHALL, and dagre's auto-layout resolves cycles by flipping
  %% an edge, which is what was throwing zones to unpredictable positions.

  subgraph INNOVATION["RESEARCH & INNOVATION [timeline]"]
    direction LR
    N1["What architecture IS (fit for\npurpose) vs what it DOES\n(performance) — Week 4"]
    N2["Lui: building codes are a site\nof CO-AUTHORSHIP — gender-\ninclusive bathrooms (2018),\npost-Triangle Fire egress\nrules (1911), ADA accessibility,\ndesegregation (1958-73) all\nchanged codes through activism"]
    N3["Dan Hill: 200,000 homes/yr at\ncurrent practice = 200% of\nAustralia's whole emissions\nbudget — Roadmap proposes\ncascading NCC emissions limits,\n461.8 → 6.63 kgCO2e/m²·a by 2028"]
    N4["'Fire, Water, Building'\nexhibition — 13 practices\nreframe fire/water from pure\nrisk-aversion toward\necologically-attuned design"]
    N1 --> N2 --> N3 --> N4
    %% N3's claim (proposes changing L3, the NCC, directly) is argued in
    %% prose (see explanation file) rather than as a graph edge back into
    %% REGULATION: REGULATION already reaches INNOVATION via GUILD and
    %% TOWNHALL, so an edge the other way closed a 4-hop cycle that was
    %% forcing dagre to flip a rank somewhere in that chain.
  end
  class N2,N3 theory

  subgraph PROCUREMENT["PROCUREMENT — independent research, unfinished connector [small linear]"]
    U1["Traditional (AS4000) vs\nDesign & Construct (AS4902)\nvs Novated D&C"]
    U2["AIA National Novation\nSurvey 2019: 266 practices,\n484 novated projects —\n'enormous opportunity to\naddress building quality\nand prevent risk'"]
    U3["Novation can diminish design\nintent — lost direct client\ncontact, restricted site access,\nexcluded from value management"]
    U4["A registered architect can\nlose creative control WITHOUT\nlosing registration — a\ndifferent kind of vulnerability\nthan anything in the pathway"]
    U1 --> U2 --> U3 --> U4
  end
  class U1,U4 transform

  subgraph BACKSTAGE["POWER STRUCTURE — who actually sets the rules [keyword network, drawn behind everything else — this is the critical position]"]
    direction TB
    BS1[SCHOOLS]
    BS2[INSTITUTE]
    BS3[BOARD]
    BSAME["same overlapping group\n(Week 4, 'TheyRule' pattern)"]
    BREG["REGISTRATION\ntightly gated —\n5 reqs · 3 pathways · 3-part exam"]
    BCODE["CODE + CONTRACT\nloosely gated —\namendable by whoever shows up (Lui);\nnovated away by contract (U3-U4)"]
    B4{"= CRITICAL POSITION"}
    BS1 & BS2 & BS3 --> BSAME
    BSAME --> BREG
    BSAME --> BCODE
    BREG -.->|≠| BCODE
    BREG --> B4
    BCODE --> B4
  end
  class BREG,BCODE backstage
  class BSAME,BS1,BS2,BS3 default

  %% CLUSTER COLOUR WASH — each cluster tinted so it reads as its own
  %% coloured zone at a glance, plus visual hierarchy: Registration Pathway
  %% gets the thickest border (the one compulsory pathway), the Project
  %% Delivery Process the thinnest (a small process run once per project,
  %% not a required topic in its own right).
  style LEGEND fill:#f7f6f2,stroke:#999999,color:#1a1a1a
  style LINELEGEND fill:#f7f6f2,stroke:#999999,color:#1a1a1a
  style HUB fill:#FFF6DA,stroke:#C9A227,stroke-width:2px,color:#1a1a1a
  style RIDE fill:#FCE9B0,stroke:#8a6c1f,stroke-width:4px,color:#1a1a1a
  style APPRENTICELAND fill:#E6F2E6,stroke:#6b9b6b,stroke-width:2px,color:#1a1a1a
  style PRACTICE fill:#F3EDE3,stroke:#a68a5b,stroke-width:2px,color:#1a1a1a
  style FLUME fill:#E3F2F0,stroke:#4a9b91,stroke-width:1.5px,color:#1a1a1a
  style REGULATION fill:#E7EDF2,stroke:#5b7c99,stroke-width:2px,color:#1a1a1a
  style GUILD fill:#EFE7F5,stroke:#8a6ba8,stroke-width:2px,color:#1a1a1a
  style TOWNHALL fill:#F7E9EC,stroke:#b06a7a,stroke-width:2px,color:#1a1a1a
  style INNOVATION fill:#E4F5E9,stroke:#4d8f6a,stroke-width:2px,color:#1a1a1a
  style PROCUREMENT fill:#E4EEF5,stroke:#345070,stroke-width:2px,stroke-dasharray:5 3,color:#1a1a1a
  style BACKSTAGE fill:#F2E4DE,stroke:#7a3b28,stroke-width:1.5px,color:#1a1a1a

  HUB -->|[spine]| RIDE
  RIDE -->|[spine]| APPRENTICELAND
  RIDE -->|[spine]| PRACTICE
  RIDE -->|[spine]| REGULATION
  RIDE -->|[spine]| GUILD
  APPRENTICELAND -.->|[spine]| PRACTICE
  PRACTICE -.->|[practice], depends upon| PROCUREMENT
  REGULATION -.->|[regulation]| GUILD
  GUILD -.->|[regulation]| TOWNHALL
  REGULATION -.->|[regulation]| INNOVATION
  TOWNHALL -.->|[regulation]| INNOVATION
  RIDE -.->|[critical]| BACKSTAGE
  REGULATION -.->|[critical]| BACKSTAGE
  PROCUREMENT -.->|[critical], unfinished connector| BACKSTAGE
  %% Power Structure "feeding back to" the hub question is this diagram's
  %% thesis (see explanation file + "Primary links to say aloud" #5) —
  %% deliberately not drawn as a graph edge back to HQ: that edge closed
  %% the HUB->RIDE->BACKSTAGE->HUB cycle that was throwing Power Structure
  %% to the top of the auto-layout instead of staying visually subordinate.
```

---

## Primary links to say aloud

1. **The diagram has exactly one compulsory pathway, and it's heavily gated on purpose.** The Registration Pathway is Victoria's real, legally required path to the title "Architect" — education, logged experience, the APE's exam and interview, ARBV registration, then an ongoing loop of CPD and insurance. Failing a gate sends you back to repeat that stage (resit, log more hours); only a serious breach gets you excluded from the pathway entirely (Tribunal, discipline register).
2. **Every other required cluster is optional, but none of them are decorative.** Education, Employment, Legislation, Professional Bodies and Ethics & Public Value are the required Assessment 1 topics, each drawn in its own native layout, connected to the pathway and to each other by cross-links.
3. **Procurement is deliberately drawn with an unfinished connector** — Weeks 1–4 gave almost no sourced material on procurement (one line, in Week 4), so this cluster is built from independent AIA research (tagged, not lecture content): novated design-and-construct can strip a *registered* architect of design control without touching their registration at all — a genuinely different kind of vulnerability than anything the pathway tests for.
4. **Research & Innovation is where the diagram's own rules get rewritten.** Ann Lui's argument that building codes are a site of co-authorship — gender-inclusive bathrooms, post-Triangle-Fire egress rules, disability access, the removal of segregation codes — shows codes changing through activism, not just expert committee. Dan Hill's Reduction Roadmap proposes exactly that kind of code amendment for Australia's National Construction Code, to close a 98% embodied-carbon gap.
5. **Power Structure is the diagram's actual argument, and it's drawn behind everything else on purpose.** A small, overlapping group of people sit across schools, the Institute and the registration board at once (Week 4's "TheyRule" reading). The Registration Pathway — the one gate everyone can see — is exhaustively regulated. Legislation (who gets to write the code) and Procurement (who keeps design control after novation) are comparatively loosely guarded. That mismatch — tightly gating who becomes an architect while leaving who controls what gets built much more open — is this diagram's critical position.
6. **The Registration Pathway's entrance framing names what the gates are actually testing.** Trust breaks into Autonomy, Discretion and Accountability; Risk is owed to both the Public and the Profession, and grows with knowledge and experience — so the pathway isn't testing knowledge alone, it's testing how much of that trust/risk pairing a candidate can be handed. This came directly off a tutorial whiteboard, not a lecture slide — see `04-topics-context.md` for the exact transcription.
7. **The Project Delivery Process shows what "practice" actually means, project by project.** Nested inside Employment, it runs Feasibility → Concept/Sketch Design → Developed Design → Construction Documentation → Contract Administration, gated twice by real external checkpoints (Town Planning/Council, the Building Surveyor) and looping back to the client and brief rather than ending cleanly — it operationalises the NSCA competencies the Registration Pathway only lists in the abstract (Stage 2), and gives Legislation's checkpoints (Council, the Building Surveyor) something concrete to actually gate.

---

## Translating to the hand-drawn A1

This Mermaid file is the thinking draft (per `08-diagram-style/STYLE_GUIDE.md`, "Mermaid is the thinking draft; final class presentation diagram may be redrawn in your Proprac visual language"). For the physical A1:

- Draw the Registration Pathway as the single most visually dominant element — thickest line weight, literally drawn taller/more central than any other cluster, matching the brief's requirement that the registration pathway be the **organising spine**.
- Draw Power Structure small and set back/behind the rest of the layout (not a cluster you engage with directly) — its subordinate visual weight relative to the Registration Pathway's dominance IS the critical position, made visible rather than just argued in prose.
- Procurement's "unfinished connector" should be drawn literally unfinished (dashed/incomplete line) — an honest signal that this is the newest, least-integrated part of your own matrix.
- Reuse the existing legend/colour system from `08-diagram-style/legend.md` so a marker unfamiliar with the diagram can still read it correctly.
- No illustrative theme (park, map, or otherwise) is required or implied by this version — plain diagrammatic conventions (boxes, arrows, gates, colour-coded clusters) carry the argument on their own, per the brief's own framework options (pathways, ecosystems, layered systems, networks, cycles, hierarchies).

---

## Redraw notes

- **v07 (2026-08-20):** dropped the theme-park metaphor entirely, at the student's request. Every cluster, node and legend entry is renamed to plain, brief-matching vocabulary (Registration Pathway, Education, Employment, Legislation, Professional Bodies, Ethics & Public Value, Research & Innovation, Procurement, Power Structure) instead of park terms (Registration Mountain, Apprenticeland, Practice Square, Regulation Row, Guild Quarter, Town Hall, Innovation Pavilion, Procurement Annex, Control Booth, Main Street). No sourced content, relationships, or citations changed — this is a relabeling pass only, done so the diagram answers the brief's own required-topic list directly rather than through a narrative skin. `02-explanation.md`, `03-presentation-script.md` and the 150-word critical-position note (`02-assessment-tasks/assessment-1-critical-position.md`) were updated to match in the same pass. The hand-illustrated `architectland-map.svg` and `architectland-zoomable.html` still use the old park theme and have **not** been redrawn — they need a manual pass (or a fresh hand-drawn A1 built directly from this version) before submission; flagging rather than silently leaving them inconsistent.
- **v06 (2026-08-17, same day):** removed every remaining graph edge that pointed "backward" against the Hub → Pathway → clusters flow (Ethics & Public Value → Hub, Power Structure → Hub, Research & Innovation → Legislation, and each required cluster's specific feed into a Registration Pathway stage: Education → RS1/RS5, Employment → RS2, Legislation → RS4 twice). Those edges were thematically real but they closed cycles, and Mermaid's auto-layout (dagre) resolves a cycle by flipping an edge — which is exactly what was throwing Power Structure to the top of the page and tangling the Legislation/Professional Bodies/Ethics/Research cluster instead of laying out top-to-bottom the way the brief's spine concept intends. The graph is now a clean DAG rooted at the Hub; the removed relationships are still stated in each node's own text and in the prose sections, just not as edges fighting the layout. If you want a diagram with full control over where every cluster sits — not subject to any auto-layout algorithm's decisions — that's what a hand-placed SVG is for; it's hand-placed, not auto-laid-out.
- **v05 (2026-08-17, same day):** Power Structure rebuilt as an actual keyword network instead of two paragraph-length nodes — three small SCHOOLS/INSTITUTE/BOARD nodes converge on "same overlapping group," which fans out to two short contrast nodes (REGISTRATION: tightly gated vs CODE + CONTRACT: loosely gated), closing on a short `= CRITICAL POSITION` node — same logic as before, but every node is now a phrase, not a sentence.
- **v04 (2026-08-17, same day):** three fixes together. (1) Added `classDef default` — every previously-unclassed node (the Legend, most expansion-level nodes across every cluster) now gets an explicit light fill + black text, which fixes them rendering with GitHub's own dark-mode node default: GitHub strips `%%{init}%%` theme directives for security, so only real graph syntax (`classDef`/`class`/`style`) is reliable across every renderer, not theme config. (2) Added a `LINELEGEND` subgraph showing the two line types that actually exist in this diagram (solid = primary/enables/depends; dash-dot = relationship/limits/causes/feedback — there is no third, visually distinct "dotted," despite three verbs being listed in the prose legend elsewhere in this repo) plus the cross-link marker key. (3) Added a `style` line per cluster so each zone is tinted its own pale colour, with the Registration Pathway given the thickest border (4px, the one compulsory pathway) and the Project Delivery Process the thinnest (1.5px, a small process run once per project) — so the hierarchy (one dominant pathway > required clusters > a nested sub-process) still reads when the whole map is zoomed out to an overview.
- **v03 (2026-08-17):** every cross-cluster relationship label now carries a category marker ([spine], [regulation], [practice], [critical]) — see the Legend's "Cross-link categories" table. This is deliberately a label marker, not a Mermaid `linkStyle` line-colour: this diagram has 130+ edges, and line-colouring needs an exact numeric index per edge — a miscount recolours the wrong link silently. If you want true coloured strokes on the hand-drawn A1, use these four categories directly as literal marker/highlighter colours along each cross-link line.
- **v02 (2026-08-16, same day):** added the Registration Pathway's entrance framing (Trust/Risk) and the Project Delivery Process inside Employment, from a tutorial whiteboard capture. The Risk equation ("knowledge + experience = risk") was visually emphasised/revised on the board — treat it as a prompt to discuss in your verbal presentation, not a settled formula to quote as-is; see `04-topics-context.md`.
- This is a first full pass at the assessment master under the new (v07) naming — expect at least one more version before Week 5's submission, especially once Week 5 is actually lectured (currently only pre-reading material is included, clearly tagged).
- Victorian registration year (1922 vs 1923) is still unresolved from Week 3 — confirm before finalising Stage 4's date, if a date is added to the hand-drawn version.
- Consider whether Professional Bodies and Ethics & Public Value should merge on the hand-drawn version if space is tight — both are about who the profession answers to, just from different angles (institutional vs ethical).
- Check `02-assessment-tasks/assessment-1-brief.md`'s deliverables checklist against this pack before submission — this file plus `02-explanation.md` covers the diagram and its reading logic; the separate 150-word note is `02-assessment-tasks/assessment-1-critical-position.md`.
