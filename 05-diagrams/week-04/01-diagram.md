# 01 — Diagram: Week 04 — The Good and the Bad Architect (Media + Differentiation)

- **Week:** 04
- **Date:** 2026-08-16
- **Layout:** hybrid, composite-layered (see `08-diagram-style/STYLE_GUIDE.md` "Composite layering") — radial core + hierarchy + network + timeline + list-network + top-down + small linear crossover, cross-linked
- **Style:** `08-diagram-style/` — hybrid short-form nodes, networked links
- **Sources scoped:** `03-weekly-resources/week-04/` only (lecture recording, slide deck "The Good and the Bad Architect — Media + Differentiation" by Helen Duong + Peter Brew, Naomi Stead's "Architecture Australia turns 120")
- **Version:** v01 — dump pass applied per the "3 D's": every named person, award, body and case the sources support is a node, not just cluster-level summary

## Legend

| Element | Meaning |
|---------|---------|
| 🟡 Main / stage | Core topic or primary cluster |
| ⬜ Expansion | Short-form detail / keyword node |
| 🟢 Integrated | Named theorist / case study / Assessment 1 link |
| 🔵 Transform | Live tension / forward pointer to next lecture |
| **→** solid | Primary flow |
| **- - →** dashed | Relationship / influence |
| **···→** dotted | Feedback loop |
| 🔴 accent | Tension / unresolved question |

**Depth lenses applied this week** (see `08-diagram-style/STYLE_GUIDE.md` "3 D's"): ethical = Loos's "all architects are equally guilty" claim; professional/regulatory (default) = Architects Act minimum-standard framing, awards-as-institutional-machinery; historical = Bailey 1985 → Hyde 2011 → Shaw 1999 → Stead 2024 critique thread.

**Layout type per zone**: CORE = radial hub; AWARDS = hierarchy/list; COUNTER = network; VOICES = left→right timeline; MEDIAMAP = list-network; POWER = top-down (Divided Line, this week's own instance); INNOVATION = small linear crossover. Cross-links between zones are relationship claims, not one uniform flow.

*Cross-**week** relationships (e.g. to Week 2's Apparatus/Divided Line) are intentionally not drawn here — this pack stays scoped to Week 4 sources only, per `weekly-diagram-pack.mdc`. See `05-diagrams/synthesis/01-master-map.md` for the cross-week version.*

---

## Diagram

```mermaid
flowchart TB
  classDef main fill:#F4D35E,color:#1a1a1a,stroke:#8a6c1f,stroke-width:1px;
  classDef theory fill:#8FBF8F,color:#1a1a1a,stroke:#3f5a3f,stroke-width:1px;
  classDef transform fill:#9EC1D9,color:#1a1a1a,stroke:#345070,stroke-width:1px;

  subgraph LEGEND["Legend"]
    direction LR
    L1[🟡 Main node] --- L2[⬜ Expansion]
    L2 --- L3[🟢 Theory / case]
    L3 --- L4[🔵 Live tension]
  end

  subgraph CORE["🟡 Core — is good/bad architect a real distinction? [radial hub]"]
    direction LR
    Q{"Loos 1910: before God no good\nor bad architects — only\nsubtle nuances 'in the presence\nof Belial.' A matter of degree,\nnot kind"}
    Q1["Lake Como parable: the villa\ndesecrates the lake regardless\nof whether its architect is\n'good' or 'bad'"]
    Q2["Taste vs Architecture:\nArchitecture=Culture=Collective=\nEveryday // Artist=Taste=\nIndividual=Bespoke — 'confusing\nart and culture'"]
    Q3["Registration reframe: Act s.10\nrequires only 'good character' +\n2yrs practice — one minimum\nstandard for all. Can good/bad\nstill exist once that's met?"]
    Q --> Q1
    Q --> Q2
    Q --> Q3
  end
  class Q main

  subgraph AWARDS["🟡 Awards as a value system [hierarchy/list]"]
    A1["AIA categories: Commercial ·\nEducational · Heritage · Interior ·\nPublic · Residential (New/Alts/\nMultiple) · Small Project · Urban\nDesign · Sustainable · Colorbond\nSteel · Enduring · Emerging ·\nEmAGN · Regional · Melbourne ·\nBates Smart Media"]
    A2["'Are these different\nArchitectures? Or different\nbusiness models, marketing\nstrategies?'"]
    A3["Awards = 'professional\nconstitution of value' — decide\nin advance what counts:\ntypology, authorship, visual\ndistinction, technical skill"]
    A4["...vs what stays peripheral:\nsocial benefit, working on\ncountry, collaboration,\nmaintenance, long-term\noccupation"]
    A5["Case: 'Judging Architecture'\n(1929-2003 retrospective) —\n1969 Southland Shopping Centre\nbeat the now-iconic NGV"]
    A5a["No categories existed then —\njudged on merit + contribution,\nnot type. Southland = suburban\nretail R&D; NGV = cultural value.\nRetrospect reversed the verdict"]
    A6["Case: Melbourne Park Tennis\nCentre (NH Architecture) — TV\nstudio, sport venue, concert hall.\nWhich single award category?"]
    A7["Freeland: Vic journal (RVIA,\n1929-42) = professional record /\nNSW journal (Art + Architecture,\n1908) = public culture + discourse.\nJournals/awards = 'machinery\nthrough which the profession\ndecides who represents it'"]
    A1 --> A2 --> A3 --> A4
    A3 --> A5 --> A5a
    A2 --> A6
    A3 -.-> A7
  end
  class A1,A3 main

  subgraph COUNTER["🟡 Counter-models — external accountability [network]"]
    C1["Architecture, Au Award for\nSocial Impact — jury includes\na politician, an Indigenous\nengagement consultant\n(Blaklash Creative), the Disability\nDiscrimination Commissioner"]
    C1a["Criteria: demonstrable social\nbenefit — social cohesion, racial\njustice, inclusive housing,\naccessibility, equity, sustainability"]
    C2["Learning Environments Australia\n(LEA) awards — Planning Process,\nDesign Outcome, Flexibility,\nInnovation criteria, judged by\nindustry practitioners not architects"]
    C2a["2025: AIA Henry Bastow Award\n(Pascoe Vale Primary, Kosloff) ≠\nLEA Overall Winner (Scientia\nTerrace, Hayball) — different\nprojects, different values,\nhistorically almost never the same"]
    C3["Indigenous awards debate\n(Sarah Lynn Rees, 2020) — Louis\nAnderson Mokak: separate award\nvs embedding Indigenous\nknowledge in ALL criteria"]
    C3a["'Power and benefit does not lie\nwithin the dominant role of the\narchitect' — separate category\nrisks easy tokenism over\nwholesale change"]
    C1 --> C1a
    C2 --> C2a
    C3 --> C3a
    C1a -.->|tests whether AIA\nmainstream criteria could\nabsorb this instead| C3a
  end
  class C1,C2,C3 main

  subgraph VOICES["🟡 Historical critique thread — 1985 to 2024 [timeline]"]
    direction LR
    V1["Don Bailey 1985: awards =\n'self-congratulatory,' corporate\nnarcissism. Defensible only when\nthey educate the public, sharpen\ncollective judgment, stay\naccountable to users"]
    V1a["'May it never be a vehicle for\nperpetuating a clique of\narchitectural prima donnas but\nrather portray architects as\nquietly competent facilitators'"]
    V2["Rory Hyde 2011 (Robin Boyd\nAward review): awards reward\n'safe, clear, consistent, refined'\nwork — 'celebrate success,\npunish ambition'"]
    V3["Nigel Shaw 1999 (AIA National\nPresident's foreword): 'the\ncommunity does not see\nArchitecture, it sees Architects'"]
    V3a["'We must move forward with a\npositive view on the value of\nArchitecture, not Architects as\nindividuals — that will follow'"]
    V4["Naomi Stead 2024 ('Architecture\nAustralia turns 120'): bias against\nwork that is modest, unglamorous,\nhard to photograph — nearly all\nindustrial architecture"]
    V4a["AA as a 'walled garden' — passing\nover Cronulla riots, the Apology to\nthe Stolen Generations, Black\nSaturday, Gillard's election, NDIS,\nthe Uluru Statement from the Heart"]
    V4b["'It is in the nature of a\nprofessional magazine to be more\nof a searchlight than a lantern' —\nshould AA be a lantern instead?"]
    V1 --> V1a --> V2 --> V3 --> V3a --> V4 --> V4a --> V4b
  end
  class V1,V3,V4 main

  subgraph MEDIAMAP["🟡 Media ecosystem — six channels [list-network]"]
    M1["Awards (institutions/juries) →\nrecognised excellence // risk:\nprestige circulates among those\nable to enter + document"]
    M2["Journals (editors/critics) →\nselected projects, argument //\nrisk: criticism + promotion\nhard to separate"]
    M3["Online design media (web\ntraffic) → novelty, global reach\n// risk: detached from local\ncontext (e.g. ArchDaily)"]
    M4["Practice site + PR (the\npractice/publicist) → consistent\nbrand narrative // risk: no\nindependent evaluation"]
    M5["Instagram/TikTok (algorithm) →\nimages, frequency, engagement //\nrisk: popularity = value proxy"]
    M6["LinkedIn (networks/algorithm) →\nleadership persona // risk:\nauthority via repetition, not merit"]
    M7["Independence spectrum: from\nowners, advertisers, sponsors,\narchitects who grant access +\nphotography, and institutions\nsharing the same networks"]
    M8["Bates Smart Award for\nArchitecture in Media — est.\n1986, tests what media is really\nfor across 3 recent years"]
    M8a["2023: Australian Indigenous\nDesign Charter + 'Deadly\nDjurumin Yarns' (Parlour) —\nredistributes authority,\nbuilds collective capacity"]
    M8b["2025: March Studio monograph\n(Fleur Watson) — jury citation:\n'strategic point in career' —\nconsolidates individual status"]
    M8c["2026: Izzie White, TikTok +\nInstagram, ~50,000 followers —\npublic architectural literacy,\nor personal brand, or both?"]
    M9["Case: A'Beckett Tower 2011\n(Elenberg Fraser) — Beyoncé-\nbody-inspired facade won Best\nOverend Residential Award, pre-\nBetter Apartment Design\nStandards, bedrooms with no\nwindows"]
    M9a["Debate at the time was the\nfacade — not the windowless\nbedrooms. $500 dining-voucher\nInstagram photo competition ran\nalongside"]
    M1 & M2 & M3 & M4 & M5 & M6 --> M7
    M8 --> M8a & M8b & M8c
    M7 -.-> M9 --> M9a
  end
  class M1,M8 main

  subgraph POWER["🟡 Power apparatus — Foucault's discourse network [top-down]"]
    P1["'TheyRule' precedent — US\ncorporate board interlocks (e.g.\nExxonMobil directors sitting on\nmultiple boards)"]
    P2["Same pattern in architecture: a\nsmall number of people sit\nacross schools, the Institute,\nand the registration board\nsimultaneously"]
    P3["Abstract/intelligible world\n(forms, reason): AACA, ARBV,\nVBA, University, AQF, NSCA,\nArchitects Act, Building Act, NCC,\nAustralian Standards, Planning +\nEnvironment Act, OVGA, DELWP/VPA"]
    P4["Physical/visible world (images,\nopinion): CLIENT, BUILDER,\nProduction/Construction,\nBuilding — divided from the\nabstract world by the\nARCHITECT line"]
    P5["Institute layer: AIA, Parlour,\nACA, Architeam, Professionals\nAustralia (union), ACCC, Fair\nWork — mediate between the two"]
    P6["Exemplars/Opinions/Marketing\noverlay: Awards, print + online\nmagazines, books, podcasts,\npublic events, newspapers,\nInstagram — sit around the same\nArchitect-Client line"]
    P7["Open question: does this\ninterconnectedness produce real\noversight and debate, or just\n'keep the boat afloat'?"]
    P1 --> P2 --> P3
    P3 --> P4
    P3 --> P5 --> P6
    P6 --> P7
  end
  class P2,P3 main

  subgraph INNOVATION["🔵 Fit-for-purpose → performance [small linear crossover]"]
    I1["PP1: what architecture IS —\nfit for purpose, manufactured/\nbuilt, traditional drawing-set\nrepresentation"]
    I2["PP2: what architecture DOES —\nhow it performs, new geometry/\ndesign tools/construction/\ncommunication"]
    I3["Example: Liasanden rest-stop\n(Jensen & Skodvin) — 'what it is'\n= carpark; 'what it does' =\nreflects the landscape, protects\nthe trees. The lines cross"]
    I1 -->|innovation| I2
    I1 -.->|crosses over at| I3
    I2 -.-> I3
  end
  class I1,I2 transform

  subgraph BRUHN["🔵 Cameron Bruhn extracts — editor turned AIA CEO"]
    B1["Media as a 'tripart loop':\npublic event → magazine → award\n→ back into content"]
    B2["Starts from public value, not the\nindividual architect — housing\ncrisis example (Anglicare data)"]
    B3["Post-GFC diversification\n(magazines + websites + awards +\nevents) freed magazines from\nnews reporting — more issues,\nlong-form material"]
    B4["Prefab dream since Crystal\nPalace 1851, 're-dreamed' every\ndecade, never delivered —\nconstruction industry now near\ncrisis (builders going broke, COVID\nsupply shocks), not equipped for\n2050 net-zero targets"]
    B5["Profession ceded project\nmanagement as 'not our domain'\nin the 1960s-70s — now a\nlucrative separate field, arguably\nto the profession's detriment"]
    B6["Multiple roles proposed:\nagency beyond design (Bruhn) ·\ngovernment/policy (guest) ·\ncultural producer/public\nintellectual (Stead) · not\nover-promoting individuals\n(Shaw) · trust granted by\nsociety (Bailey)"]
    B1 --> B2
    B3 -.-> B1
    B4 -.->|scope the profession\nchose to keep or shed| B5
    B2 --> B6
  end
  class B2,B6 transform

  CORE --> AWARDS
  AWARDS --> COUNTER
  AWARDS -.->|same machinery,\nread historically| VOICES
  COUNTER -.->|same accountability\nquestion, media-wide| MEDIAMAP
  VOICES --> MEDIAMAP
  MEDIAMAP --> POWER
  POWER -.->|who actually gets\nto answer this| CORE
  MEDIAMAP -.->|forward pointer,\nnext lecture| INNOVATION
  POWER -.-> BRUHN
  BRUHN -.->|"the collective test": does\nthis make architecture more useful,\nequitable, publicly accountable — or\njust one architect more marketable?"| CORE
```

---

## Primary links to say aloud

1. **Loos's 1910 provocation still frames the whole lecture** — if before God there are no good or bad architects, only degrees of the same guilt, then "differentiation" (awards, categories, media personas) is doing social and commercial work, not describing a real quality gap. The registration reframe sharpens this: the Act sets one minimum ("good character," two years' practice) for everyone — so what is the awards system actually measuring?
2. **Awards are a "professional constitution of value," not a neutral scoreboard** — the *Judging Architecture* retrospective proves it: Southland Shopping Centre beat the National Gallery of Victoria in 1969 under no-category, merit-only judging, and only later did retrospect reverse that call. Categories decide in advance what counts (typology, authorship, technical polish) and what stays invisible (social benefit, maintenance, "working on country").
3. **Counter-models expose the gap directly** — the Social Impact Award uses an external, non-architect-majority jury; LEA judges education buildings on post-occupancy evidence and rarely agrees with the AIA's own education award. The Indigenous-awards debate poses the sharpest version of the question: a separate category is easier to grant, but embedding Indigenous knowledge in *every* criterion is the harder, more real change.
4. **Four decades of the profession's own critics say the same thing from different angles** — Bailey (1985): awards risk becoming "corporate narcissism." Hyde (2011): they "celebrate success, punish ambition." Shaw (1999): the public sees architects, not Architecture, and that's a problem. Stead (2024): the flagship magazine is a "walled garden," a searchlight where a lantern might serve the public better.
5. **The media ecosystem table turns "differentiation" into infrastructure** — six channels (awards, journals, online design media, practice PR, Instagram/TikTok, LinkedIn) each reward something different and each carries its own independence risk. The Bates Smart Award's own three-year swing — from a collective Indigenous knowledge charter, to an individual-career monograph, to a TikTok advocacy account — *is* the tension the whole lecture is naming, playing out inside one prize.
6. **The power-apparatus diagram (this week's own Divided Line) shows why none of this self-corrects easily** — a small, overlapping set of people sit across schools, the Institute and the registration board at once, echoing the "TheyRule" interlocking-directorate visual. The open question is explicit in the lecture: does that interconnection produce real oversight, or does it just "keep the boat afloat"?
7. **The lecture ends on its own "collective test"** — does an award, publication or campaign make architecture more useful, equitable and publicly accountable, or does it just make one architect more marketable? The lecturer's own list of what gets neglected while the profession "celebrates itself" names housing, climate, country, labour conditions, **procurement**, and public trust explicitly — the first direct, sourced appearance of "procurement" anywhere in Weeks 1–4, worth carrying straight into Assessment 1.

---

## Redraw notes (v01)

- This pack favours atomic nodes over clean simplicity (dump pass, per the tutor's Detail principle) — refine before hand-drawing: the AWARDS and MEDIAMAP clusters are the densest and are the best candidates to trim or split across two sheets if space runs out.
- If splitting for a hand-drawn sheet: **Loos + Awards + Counter-models** (one sheet, "what counts as good architecture") vs **Media ecosystem + Power apparatus + Innovation/Bruhn** (a second sheet, "who decides, and what's next") — both trace back to the same CORE question.
- The POWER cluster deliberately reuses the slide deck's own "Divided Line" diagram in its Week-4-specific form (with AQF/NSCA/VBA/OVGA/DELWP-VPA labelled explicitly) rather than referencing Week 2's Apparatus cluster directly — cross-week continuity for this recurring frame lives in `05-diagrams/synthesis/`, not here.
- "Procurement" is a genuine, directly-quoted Week 4 source term (see Primary Link 7) — flag this for the synthesis update and for Assessment 1, since it is the first sourced mention of procurement anywhere in the toolkit so far.
