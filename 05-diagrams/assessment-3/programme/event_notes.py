"""Plain-language summaries and source links for the events in build_scenario1_timeline.py.

SOURCES maps each source key (as used in the builder's src= field) to (title, type, url).
NOTES maps the start of an event's name (without the ★) to a short summary: what happened,
then why it matters for our file. build_board_layout.py matches each event to the longest
NOTES key its name starts with, and reports any event without a note.

Source verification notes: 15-sources-A-J-verified.md (A-J), 17-interiors-1967-1975.md (K-T),
18-miro-board-verified.md (U-AF).
"""

SOURCES = {
    "A": ("Sydney Opera House — Construction begins", "Official (SOH)",
          "https://www.sydneyoperahouse.com/our-story/construction-begins"),
    "B": ("Sydney Opera House — The spherical solution", "Official (SOH)",
          "https://www.sydneyoperahouse.com/our-story/the-spherical-solution"),
    "C": ("Museums of History NSW — Public Works archives: contracts (Sydney Opera House)", "Archive",
          "https://concise.mhnsw.au/pr/pwd00024.htm"),
    "D": ("Museums of History NSW — Sydney Opera House guide (chronology)", "Archive",
          "https://mhnsw.au/guides/sydney-opera-house/"),
    "E": ("NSW State Archives NRS-12781 — Agreement, Stage 2 (Minister + Hornibrook, 18 Oct 1962)", "Archive",
          "https://researchdata.edu.au/nrs-12781-agreement-stage-2/178986"),
    "F": ("Sydney Opera House — Peter Hall and the completion of the Opera House", "Official (SOH)",
          "https://www.sydneyoperahouse.com/our-story/peter-hall-and-completion-opera-house"),
    "G": ("Sydney Opera House — Utzon departs the House", "Official (SOH)",
          "https://www.sydneyoperahouse.com/our-story/utzon-departs-the-house"),
    "H": ("NSW State Archives NRS-12824 — the 'White Book' (Hall, Todd & Littlemore, 1967–69)", "Archive",
          "https://researchdata.edu.au/nrs-12824-first-opera-house/179029"),
    "I": ("Museums of History NSW — Public Works archives: plans (Sydney Opera House)", "Archive",
          "https://concise.mhnsw.au/pr/pwd00027.htm"),
    "J": ("Museums of History NSW — Opening of the Sydney Opera House", "Archive",
          "https://mhnsw.au/opening-of-the-sydney-opera-house/"),
    "K": ("Google Arts & Culture (SOH) — The Final Stage", "Official (SOH)",
          "https://artsandculture.google.com/story/the-final-stage-sydney-opera-house/RwVhIfNkP9JCIA?hl=en"),
    "L": ("Google Arts & Culture (SOH) — Peter Hall", "Official (SOH)",
          "https://artsandculture.google.com/story/peter-hall-sydney-opera-house/CgWR3S-pZki0Ig?hl=en"),
    "M": ("Google Arts & Culture (SOH) — Acoustic reflectors and the Concert Hall", "Official (SOH)",
          "https://artsandculture.google.com/story/acoustic-reflectors-and-the-concert-hall-sydney-opera-house/ogXR06ulZxJwZg?hl=en"),
    "N": ("Google Arts & Culture (SOH) — Art, Colour and Performance", "Official (SOH)",
          "https://artsandculture.google.com/story/art-colour-and-performance-sydney-opera-house/4wXx7zl6VBlTqw?hl=en"),
    "O": ("Sydney Opera House — Preserving the Grand Organ", "Official (SOH)",
          "https://www.sydneyoperahouse.com/building/preserving-grand-organ"),
    "P": ("NSW State Archives NRS-12748 — Stage 3, Concert Hall, Grand Organ (Sharp, 1969)", "Archive",
          "https://researchdata.edu.au/nrs-12748-sydney-grand-organ/178953"),
    "Q": ("Sydney Opera House — 50 years of extraordinary moments", "Official (SOH)",
          "https://www.sydneyoperahouse.com/our-story/50-years-extraordinary-moments"),
    "R": ("Australian Dictionary of Biography — Hall, Peter Brian", "Scholarly",
          "https://adb.anu.edu.au/biography/hall-peter-brian-23687"),
    "S": ("Google Arts & Culture (SOH) — The Ghost of a Machine", "Official (SOH)",
          "https://artsandculture.google.com/story/the-ghost-of-a-machine-sydney-opera-house/egXx07Btno3aLA"),
    "T": ("NSW State Archives NRS-12800 — Waagner-Biro stage machinery assembly drawings", "Archive",
          "https://researchdata.edu.au/stage-machinery-assembly-opera-house/179005"),
    "U": ("Australian Dictionary of Biography — Cahill, John Joseph (Joe)", "Scholarly",
          "https://adb.anu.edu.au/biography/cahill-john-joseph-joe-9659"),
    "V": ("NSW Legislation — Sydney Opera House Trust Act 1961 No 9", "Legislation",
          "https://legislation.nsw.gov.au/view/whole/html/inforce/current/act-1961-009"),
    "W": ("Wikipedia — Robert Askin (premier dates; also Bob Heffron, Jack Renshaw, Tom Lewis pages)",
          "Secondary", "https://en.wikipedia.org/wiki/Robert_Askin"),
    "X": ("ArchitectureAU — Fifty years of Sydney Opera House in 50 facts", "Secondary (professional press)",
          "https://architectureau.com/articles/fifty-years-of-sydney-opera-house-in-50-facts/"),
    "Y": ("arq (Cambridge) — A specialist partnership frustrated: Utzon and Symonds at Sydney", "Scholarly",
          "https://www.cambridge.org/core/journals/arq-architectural-research-quarterly/article/specialist-partnership-frustrated-utzon-and-symonds-at-sydney/AA16A51AEFB4EB302E0D7825A722A19D"),
    "Z": ("NSW Treasury — The House the Lotteries Built", "Official (NSW Govt)",
          "https://www.nsw.gov.au/departments-and-agencies/nsw-treasury/about-us/nsw-treasury-bicentenary/walking-a-tightrope/moments/house-lotteries-built"),
    "AA": ("Steensen Varming — 90 Years of Looking Forward: The Sydney Opera House", "Secondary (firm's own history)",
           "https://steensenvarming.com/90-years-of-looking-forward-the-sydney-opera-house/"),
    "AB": ("BDSA Quantity Surveyors — Estimating at the Edge of Impossible", "Secondary (industry blog)",
           "https://blog.bdsaqs.com.au/estimating-at-the-edge-of-impossible-the-sydney-opera-house/"),
    "AC": ("Wikipedia — Sydney Opera House (cites Murray, The Saga of Sydney Opera House)", "Secondary — follow its citation",
           "https://en.wikipedia.org/wiki/Sydney_Opera_House"),
    "AD": ("Wikipedia — Davis Hughes", "Secondary", "https://en.wikipedia.org/wiki/Davis_Hughes"),
    "AE": ("Museums of History NSW — The myth of a non-invitation (Utzon and the opening)", "Archive",
           "https://mhnsw.au/stories/general/the-myth-of-a-non-invitation-utzon/"),
    "AF": ("ArchDaily — Spotlight: Jørn Utzon", "Secondary", "https://www.archdaily.com/494535/happy-birthday-jorn-utzon"),
    "REG": ("The group's Document Register (Week 10 / DOCUMENT REGISTER_PP1.pdf)", "Our own working document", ""),
    "tutor": ("Tutor's Assessment 3 instruction video (Canvas) — notes in 10-tutor-video-notes.md", "Course material", ""),
    "brief": ("Assessment 3 brief — project extract (Canvas)", "Course material", ""),
    "search": ("Web-search lead only — find a primary source (e.g. NSW Hansard 1968–69) before citing", "Unverified", ""),
}

NOTES = {
    # ---------------- D0 CAA services stage
    "A.1 Concept design": "Utzon turns the competition sketch into a concept, finished as the Red Book (Mar 1958). "
        "In CAA 2024 terms this is Schedule A stage A.1. The start month is our assumption.",
    "Gate: concept approved": "Under the CAA the client approves each stage in writing before the next starts. "
        "We place the concept approval at the Red Book (Mar 1958) — an assumed date, not a recorded one.",
    "A.2 Design development": "Design development ran for four years because the roof shells had no buildable "
        "geometry until the Yellow Book (Jan 1962). This is the design still running while the podium was built.",
    "A.4 Construction documentation": "Tender drawings and documents for Stage I (podium) only, ready by Dec 1958. "
        "Only the podium was documented — the roof was not.",
    "Gate SKIPPED": "Construction started (Feb–Mar 1959) before design development was approved — the step the CAA "
        "process expects was skipped because the Premier wanted an early start. This is the root cause of Scenario 1.",
    "A.6 Contract administration": "The architect administers the building contract from site possession (2 Mar 1959) "
        "to the final certificate (31 May 1975): instructions, claims, certificates.",
    # ---------------- D1 Client + brief
    "Competition announced": "Premier Cahill announces an international design competition for an opera house at "
        "Bennelong Point: two halls (3,000–3,500 and 1,200 seats), a restaurant and meeting rooms. This is the "
        "original client brief.",
    "Introductory letter": "Our first required document (GL1): the architect introduces the practice and the "
        "services to the client. Utzon writes to the Government (Premier Cahill). It sets the Cost of Works at $9.6m, "
        "a 6% fee ($576,000, including a $10,000 Mobilisation Fee) and two ways to run the project (staged or "
        "sequential). The Register has no date; 11 Feb 1957 (after the win) is our assumption.",
    "CAA 2024 signed": "The Client Architect Agreement is signed (Register: 21 Feb 1957). Our file uses the CAA 2024 template "
        "(the Register said CAA 2019). It repeats the letter: Cost of Works $9.6m, 6% fee, $10,000 Mobilisation "
        "Fee, staged program with the early-start risk recorded in Schedule C.",
    "Premier Cahill dies": "Cahill dies in office on 22 Oct 1959 (ADB; the archive guide says 19 Oct) and Heffron "
        "becomes Premier. The client's representative changes, which CAA C.3 requires the client to notify.",
    "Architect notifies client": "Our constructed event: the extra piers mean extra design work for the architect, "
        "so the architect notifies the client in writing of additional services and fee (CAA D.8). Not in any "
        "source — it is the client-side twin of SW-12.",
    "Askin government": "The Liberal–Country coalition wins office on 13 May 1965. The new Minister for Public "
        "Works, Davis Hughes, takes control of payments from the Opera House Committee — the start of the fee "
        "dispute.",
    "Sydney Opera House Act 1960": "The 1960 Act makes the Minister for Public Works the constructing authority "
        "(backdated to 1 Jan 1957) and sets up the lottery account. Legally, the client who signs the building "
        "contracts is the Minister.",
    "Trust Act 1961": "The Sydney Opera House Trust Act (assented 14 Mar 1961) creates the Trust that will run the "
        "building, replacing the Executive Committee. The Trust operates the House; it did not build it.",
    "Utzon resigns": "After a meeting with Hughes over unpaid fees and refused plywood prototypes, Utzon sends his "
        "resignation on 28 Feb 1966. The project loses its architect with Stage III undocumented.",
    "Hall / Todd / Littlemore appointed": "A panel replaces Utzon on 19 Apr 1966: E.H. Farmer (Government Architect), "
        "Peter Hall (design), David Littlemore (supervision) and Lionel Todd (contract documents).",
    "Govt pays $160,000": "The Government pays Utzon's representatives $160,000 for 130 Stage III drawings "
        "(17 May 1966). The new team inherits sketches and these drawings, not a full documentation set.",
    "Review of Program": "Hall, Todd & Littlemore propose major changes to how the halls are used (12 Dec 1966). "
        "This is the brief being changed after construction had started.",
    "Opening Committee": "Premier Askin heads the Official Opening Committee (28 Feb 1972). The client now plans "
        "the handover and opening.",
    "Hughes resigns": "Davis Hughes leaves parliament on 17 Jan 1973 and Leon Punch becomes Minister for Public "
        "Works — another change of client representative (CAA C.3) shortly before completion.",
    "Premier Askin formally invites Utzon": "Archive letters show Askin formally invited Utzon and his wife to the "
        "opening, with flights and accommodation (20 Jun 1973). The popular story that he was never invited is a "
        "myth.",
    "Building handed to the Trust": "Responsibility for the Opera House passes to the Sydney Opera House Trust and "
        "the Minister for Cultural Activities, George Freudenstein (1973). The client who operates the building is "
        "no longer the client who built it.",
    "Utzon declines": "Utzon declines (1 Aug 1973): he could not be the Government's guest and also criticise its "
        "Minister. A strong Part B example of professional conduct in a dispute.",
    "Askin resigns": "Askin resigns on 3 Jan 1975 and Tom Lewis becomes Premier — the head of the client government "
        "when the final certificate (SW-31) is issued.",
    # ---------------- D2 Architect design output
    "Competition design phase": "Entrants prepare their designs from the Sep 1955 announcement; drawings are "
        "submitted in 1956. 233 entries from 32 countries.",
    "Utzon wins first prize": "Jørn Utzon wins first prize (£5,000) on 29 Jan 1957 and is then commissioned for the "
        "final drawings and supervision.",
    "Red Book sent": "Utzon's Red Book — the developed concept — is sent to the NSW Government in Mar 1958.",
    "Roof / shell design": "The shells go through parabolic, ellipsoid and finally spherical geometry (1958–62). "
        "By late 1961 there was still no buildable solution — while the podium below was already being built.",
    "Yellow Book": "The Yellow Book (Jan 1962, 38 pages of shell drawings) fixes the spherical geometry. The roof is "
        "now known — and heavier than the podium was designed for.",
    # ---------------- D3 Consultants
    "Ove Arup & Partners engaged": "Arup become the structural engineers. Sources conflict on who engaged them: "
        "the archive guide says Utzon (in London); the brief says the client. It matters for CAA Schedule B.",
    "Steensen & Varming": "The Danish firm Steensen & Varming are appointed mechanical engineers in 1957 and stay on "
        "after 1966; they designed the harbour-water cooling system.",
    "Utzon develops plywood mullions": "From Oct 1961 Utzon's office works with plywood maker Ralph Symonds Ltd on "
        "glass-wall mullions and auditorium ceilings — a designer–manufacturer partnership the government later "
        "rejected.",
    "Ralph Symonds Ltd in receivership": "Symonds goes into receivership (one secondary source says 26 Feb 1964 — "
        "verify). Hughes would not award prototype work to a company in receivership; this fed the 1965–66 dispute.",
    "Problem found": "Scenario 1 starts here: once the roof is split into separate structures, its final loads "
        "exceed what the podium columns were designed for. Date and wording from the tutor's worked example; Murray's "
        "Saga (via Wikipedia) says the columns had to be re-built.",
    # ---------------- D4 Interior design
    "Cabinet approves new brief": "Cabinet approves Hall's changed brief (Mar 1967): the Major Hall becomes a "
        "2,800-seat concert hall and opera moves to a 1,500-seat theatre.",
    "Arup objects in writing": "Ove Arup writes to Minister Hughes (28 Mar 1967) objecting that dropping opera from "
        "the Major Hall undermines the reason for the shells. Stage machinery already made is scrapped.",
    "White Book": "Hall, Todd & Littlemore's first designs for the halls and glass walls (1967–69), known as the "
        "White Book. Design work starts from Utzon's sketches, not working drawings.",
    "Glass walls redesigned": "Hall and Arup redesign the glass walls on a steel-mullion frame (1968) instead of "
        "Utzon's plywood mullions.",
    "Glass-wall prototype specification": "A prototype specification for the glass walls (Jan 1969) — testing the "
        "design before building it.",
    "Grand Organ report": "Organ builder Ronald Sharp's report and specification for the Concert Hall organ (1969), "
        "the start of a ten-year separate contract.",
    "Acoustic reflector shape fixed": "Acoustician Vilhelm Lassen Jordan and Hall fix the final ring shape of the "
        "Concert Hall reflectors (Dec 1971).",
    "Coburn tapestry curtains": "John Coburn's Curtain of the Sun and Curtain of the Moon are hung in the Opera and "
        "Drama theatres for the 1973 opening — Hall interpreting Utzon's colour intent.",
    # ---------------- C1 Procurement + cost
    "Opera House Lottery starts": "The Opera House Lottery starts on 25 Nov 1957 so that building money does not "
        "come from other public works. Lotteries eventually paid for the whole $102m.",
    "Stage I tender documents": "Conditions of contract and bills of provisional quantities for Stage I are issued "
        "in Dec 1958 — the tender package for the podium.",
    "Tender return": "Tenders for Stage I come back. The Register gives only the year; Jan 1959 is assumed.",
    "Contractor selection": "Civil & Civic is selected for Stage I (podium). Month assumed from the Register's year.",
    "Simple Works Contract signed": "The building contract is signed with Civil & Civic (Register: 19 Feb 1959). In "
        "our file this is the ABIC Simple Works 2018 contract. Stage I value £1,397,878 (NSW Treasury).",
    "Stage machinery contract": "A contract with Waagner-Biro (Austria) for stage machinery is signed in Apr 1961 — "
        "machinery later scrapped from the Major Hall in 1967.",
    "Cost plan issued": "By 1962 the estimate has reached £13.7m (about A$27.4m), against the original £3.5m. This is "
        "the CP-06 cost plan in our Register; the month is assumed.",
    "Stage II agreement": "The Minister for Public Works signs the Stage II (roof) agreement with M.R. Hornibrook "
        "(NSW) Pty Ltd on 18 Oct 1962.",
    "Stage III agreement": "The Stage III (interiors) agreement with Hornibrook is signed in Nov 1966, after Utzon "
        "has left.",
    "A$22.9m spent": "By Oct 1966 only A$22.9m had been spent — less than a quarter of the final cost. Most of the "
        "money went on Stage III.",
    "New estimate": "The new architects reportedly advise a further $85m and completion by end 1972 (Sep 1968). "
        "Found only through a web search — find a primary source before citing.",
    "Final cost $102m": "Public Works states the final cost: $102 million, excluding the organ and car park "
        "(May 1974). The first estimate was £3.5m (about $7m).",
    # ---------------- C2 Construction works
    "Tram depot demolished": "The Fort Macquarie tram depot on Bennelong Point is demolished from Aug 1958 to clear "
        "the site.",
    "Site possession": "Cahill holds the construction ceremony on 2 Mar 1959; Civil & Civic starts Stage I. This is "
        "site possession under ABIC F1.",
    "Planned programme at signing": "The baseline: practical completion planned for 26 Jan 1963 when the contract was "
        "signed. The grey bar shows how far reality drifted from the plan.",
    "Stage I": "The podium, by Civil & Civic, finishes in Feb/Mar 1963 — two years late against the historical "
        "programme. Under our contract it reaches practical completion on 18 Mar 1963 (assumed day), 20 days after the "
        "adjusted date, so $20,000 of liquidated damages are deducted in SW-31. The ground needed about 700 bored "
        "concrete shafts nobody had planned for.",
    "Piers work on site": "Our scenario on site: the contractor strengthens columns and adds piers, taking the extra "
        "month granted by SW-14. Dates assumed from the tutor's example.",
    "Stage II contract drawings": "The Stage II contract drawings, dated with the Stage II agreement (Oct 1962).",
    "Stage II — roof shells": "Hornibrook builds the roof shells from Apr 1963 until the last (2,194th) segment is "
        "placed on 17 Jan 1967.",
    "Stage III — interiors": "Interiors and glass walls, by Hornibrook, from early 1967 to the opening (Oct 1973). "
        "Sources differ on the start: agreement Nov 1966, design from 1967, site work from 1968.",
    "Stage III working drawings": "The Stage III working drawings are dated Jul 1968 (bound in a Jun 1969 volume).",
    "Defects liability period": "Twelve months after practical completion for the contractor to fix defects "
        "(ABIC M13). Our assumption — not a recorded historical period.",
    # ---------------- C3 Contract administration
    "Instruction for a Variation": "SW-12: the architect instructs the contractor to strengthen the columns and add "
        "piers. This is the first form in our Scenario 1 chain.",
    "Contractor's details of claim": "SW-42 (optional): the contractor claims 1 month and $5,000 for the variation.",
    "Instruction to proceed": "SW-13 (optional): the architect tells the contractor to go ahead with the varied work.",
    "Adjustment of time": "SW-14: the architect grants 1 extra month, moving the date for practical completion.",
    "Contract Price Adjustment": "SW-11: the contract price goes up by $5,000. The final certificate (SW-31) must "
        "refer back to this.",
    "Notice to contractor": "After Utzon resigns, the client tells Civil & Civic in writing that Hall, Todd & Littlemore "
        "now administer the Stage I contract (20 Apr 1966, assumed day). This is why they can issue the final "
        "certificate (SW-31) in 1975.",
    "Practical completion": "The Queen opens the building on 20 Oct 1973. We treat this as practical completion; "
        "the defects period starts here.",
    "Final Certificate": "SW-31: the Architects' Certificate of Completion, 31 May 1975, issued by Hall, Todd & "
        "Littlemore. It must refer to SW-11. The Register says 1974 — update it if the group agrees.",
    # ---------------- C4 Interior works + fit-out
    "Waterproofing specification": "A waterproofing specification is issued in Mar 1967, as Stage III begins.",
    "Stage III interiors + glass walls on site": "Site work on the interiors and glass walls runs from 1968 to 1973 "
        "(SOH's own story).",
    "Glass walls built": "The glass walls go up on their steel frames and are nearly complete by 1971; over 6,200 m² "
        "of glass came from France.",
    "Light-fittings agreement": "The architects sign an agreement with GEC-Philips for light fittings (Aug 1969) — a "
        "separate supply package.",
    "Electronic services subcontract": "Hornibrook subcontracts electronic services to AWA (Mar 1970).",
    "Acoustic reflectors made": "21 clear-acrylic reflectors are made by K.F. Plastics and installed over the Concert "
        "Hall stage between Mar and 5 Sep 1972.",
    "Opera Theatre stage machinery drawings": "Waagner-Biro's assembly drawings for the new Opera Theatre's stage "
        "machinery (vol. 2, Dec 1972).",
    "First test concert": "The first test concert in the Concert Hall, for the builders, with the Sydney Symphony "
        "Orchestra (17 Dec 1972) — testing the acoustics before completion.",
    "First opera": "The Australian Opera performs War and Peace in the Opera Theatre on 28 Sep 1973 — the building "
        "is in use almost a month before the official opening.",
    "Opening festival": "A two-week festival of events around the opening, 17 Oct – 3 Nov 1973.",
    "First public Concert Hall concert": "Birgit Nilsson sings Wagner with the Sydney Symphony Orchestra in the "
        "first public Concert Hall concert (29 Sep 1973).",
    "Grand Organ": "The Grand Organ is built under a separate contract and finished on 30 May 1979. Its budget rose "
        "from $400,000 to $1.2m; it is excluded from the $102m.",
}

# ---------------------------------------------------------------- parties
# The six party categories from the group's Miro Parties panel, with its colours.
ROLE_COLOURS = {
    "Client": "C62828",
    "Architect": "2E9E44",
    "Builder": "5B3FD0",
    "Engineer": "3B8FE0",
    "Specialist consultant": "A0471B",
    "Supplier / manufacturer": "E08A1E",
}

# event name prefix maps to (party = who acts in this event, named party)
ROLES = {
    "A.1 Concept design": ("Architect", "Jørn Utzon"),
    "Gate: concept approved": ("Client", "NSW Government (Minister for Public Works)"),
    "A.2 Design development": ("Architect", "Jørn Utzon"),
    "A.4 Construction documentation": ("Architect", "Jørn Utzon"),
    "Gate SKIPPED": ("Client", "Premier Cahill / NSW Government"),
    "A.6 Contract administration": ("Architect", "Utzon to 1966; Hall, Todd & Littlemore from 1966"),
    "Competition announced": ("Client", "Premier J.J. Cahill"),
    "Introductory letter": ("Architect", "Jørn Utzon"),
    "CAA 2024 signed": ("Architect", "Jørn Utzon and NSW Government"),
    "Premier Cahill dies": ("Client", "Premier Cahill to Premier Heffron"),
    "Architect notifies client": ("Architect", "Jørn Utzon"),
    "Askin government": ("Client", "Premier Askin; Minister Davis Hughes"),
    "Sydney Opera House Act 1960": ("Client", "Minister for Public Works"),
    "Trust Act 1961": ("Client", "Sydney Opera House Trust"),
    "Utzon resigns": ("Architect", "Jørn Utzon"),
    "Hall / Todd / Littlemore appointed": ("Architect", "Hall, Todd, Littlemore + E.H. Farmer"),
    "Govt pays $160,000": ("Client", "NSW Government"),
    "Review of Program": ("Architect", "Hall, Todd & Littlemore"),
    "Opening Committee": ("Client", "Premier Askin"),
    "Hughes resigns": ("Client", "Davis Hughes to Leon Punch"),
    "Premier Askin formally invites Utzon": ("Client", "Premier Askin"),
    "Building handed to the Trust": ("Client", "SOH Trust; Minister George Freudenstein"),
    "Utzon declines": ("Architect", "Jørn Utzon"),
    "Askin resigns": ("Client", "Premier Askin to Premier Lewis"),
    "Competition design phase": ("Architect", "Competition entrants"),
    "Utzon wins first prize": ("Architect", "Jørn Utzon"),
    "Red Book sent": ("Architect", "Jørn Utzon"),
    "Roof / shell design": ("Architect", "Jørn Utzon (with Arup)"),
    "Yellow Book": ("Architect", "Jørn Utzon"),
    "Ove Arup & Partners engaged": ("Engineer", "Ove Arup & Partners"),
    "Steensen & Varming": ("Specialist consultant", "Steensen & Varming (mechanical)"),
    "Utzon develops plywood mullions": ("Supplier / manufacturer", "Ralph Symonds Ltd (with Utzon)"),
    "Ralph Symonds Ltd in receivership": ("Supplier / manufacturer", "Ralph Symonds Ltd"),
    "Problem found": ("Engineer", "Ove Arup & Partners"),
    "Cabinet approves new brief": ("Client", "NSW Cabinet"),
    "Arup objects in writing": ("Engineer", "Ove Arup"),
    "White Book": ("Architect", "Hall, Todd & Littlemore"),
    "Glass walls redesigned": ("Architect", "Peter Hall (with Arup)"),
    "Glass-wall prototype specification": ("Architect", "Hall, Todd & Littlemore"),
    "Grand Organ report": ("Supplier / manufacturer", "Ronald Sharp (organ builder)"),
    "Acoustic reflector shape fixed": ("Specialist consultant", "Dr Vilhelm Lassen Jordan (acoustics)"),
    "Coburn tapestry curtains": ("Supplier / manufacturer", "John Coburn (artist)"),
    "Opera House Lottery starts": ("Client", "NSW Government"),
    "Stage I tender documents": ("Architect", "Jørn Utzon"),
    "Tender return": ("Builder", "Tenderers"),
    "Contractor selection": ("Client", "NSW Government to Civil & Civic"),
    "Simple Works Contract signed": ("Client", "NSW Government and Civil & Civic"),
    "Stage machinery contract": ("Supplier / manufacturer", "Waagner-Biro"),
    "Cost plan issued": ("Specialist consultant", "Quantity surveyor (Rider Hunt & Partners [verify])"),
    "Stage II agreement": ("Client", "Minister for Public Works and Hornibrook"),
    "Stage III agreement": ("Client", "Minister for Public Works and Hornibrook"),
    "A$22.9m spent": ("Client", "NSW Government"),
    "New estimate": ("Architect", "Hall, Todd & Littlemore"),
    "Final cost $102m": ("Client", "Department of Public Works"),
    "Tram depot demolished": ("Client", "NSW Government"),
    "Site possession": ("Client", "NSW Government to Civil & Civic"),
    "Planned programme at signing": ("Builder", "Civil & Civic"),
    "Stage I": ("Builder", "Civil & Civic"),
    "Piers work on site": ("Builder", "Civil & Civic"),
    "Stage II contract drawings": ("Architect", "Jørn Utzon"),
    "Stage II — roof shells": ("Builder", "M.R. Hornibrook"),
    "Stage III — interiors": ("Builder", "M.R. Hornibrook"),
    "Stage III working drawings": ("Architect", "Hall, Todd & Littlemore"),
    "Defects liability period": ("Builder", "M.R. Hornibrook"),
    "Instruction for a Variation": ("Architect", "Jørn Utzon to Civil & Civic"),
    "Contractor's details of claim": ("Builder", "Civil & Civic"),
    "Instruction to proceed": ("Architect", "Jørn Utzon"),
    "Adjustment of time": ("Architect", "Jørn Utzon"),
    "Contract Price Adjustment": ("Architect", "Jørn Utzon"),
    "Notice to contractor": ("Client", "NSW Government to Civil & Civic"),
    "Practical completion": ("Architect", "Hall, Todd & Littlemore (opening by the Queen)"),
    "Final Certificate": ("Architect", "Hall, Todd & Littlemore"),
    "Waterproofing specification": ("Architect", "Hall, Todd & Littlemore"),
    "Stage III interiors + glass walls on site": ("Builder", "M.R. Hornibrook"),
    "Glass walls built": ("Builder", "M.R. Hornibrook"),
    "Light-fittings agreement": ("Supplier / manufacturer", "GEC-Philips"),
    "Electronic services subcontract": ("Supplier / manufacturer", "AWA (subcontractor to Hornibrook)"),
    "Acoustic reflectors made": ("Supplier / manufacturer", "K.F. Plastics"),
    "Opera Theatre stage machinery drawings": ("Supplier / manufacturer", "Waagner-Biro"),
    "First test concert": ("Client", "SOH Trust / Sydney Symphony Orchestra"),
    "First opera": ("Client", "SOH Trust / Australian Opera"),
    "Opening festival": ("Client", "SOH Trust"),
    "First public Concert Hall concert": ("Client", "SOH Trust / Sydney Symphony Orchestra"),
    "Grand Organ": ("Supplier / manufacturer", "Ronald Sharp (organ builder)"),
}

# The Parties panel (from the group's Miro board, corrected in 18-miro-board-verified.md)
# (party, named party, role on the project, years, source keys)
PARTIES = [
    ("Client", "NSW Government", "Owner; funds the build through the Opera House Lottery", "1954–75", "D, Z"),
    ("Client", "Minister for Public Works", "Constructing authority (from 1 Jan 1957); signs the building contracts",
     "1957–75", "D, E"),
    ("Client", "Opera House Committee to Sydney Opera House Trust",
     "Committee from 1954; the Trust (Act of 14 Mar 1961) operates the building", "1954–75", "D, V"),
    ("Client", "Premier J.J. (Joe) Cahill", "Champions the project; forces the early start", "1952 – 22 Oct 1959", "U"),
    ("Client", "Premier Bob Heffron", "Premier after Cahill", "23 Oct 1959 – 30 Apr 1964", "W"),
    ("Client", "Premier Jack Renshaw", "Premier before the 1965 election", "30 Apr 1964 – 13 May 1965", "W"),
    ("Client", "Premier Robert Askin (Miro board says 'Askill')", "Liberal–Country government; heads the Opening "
     "Committee", "13 May 1965 – 3 Jan 1975", "W, D"),
    ("Client", "Premier Tom Lewis", "Premier when the final certificate is issued", "from 3 Jan 1975", "W"),
    ("Client", "Norm Ryan", "Minister for Public Works; Trust president (1961)", "1961", "V"),
    ("Client", "Davis Hughes", "Minister for Public Works; takes over payments; the fee dispute",
     "13 May 1965 – 17 Jan 1973", "AD, G"),
    ("Client", "Leon Punch", "Minister for Public Works at completion", "from 17 Jan 1973", "AD"),
    ("Client", "George Freudenstein", "Minister for Cultural Activities; receives the building with the Trust",
     "1973", "D"),
    ("Architect", "Jørn Utzon", "Design architect; contract administration to 1966", "1957 – 28 Feb 1966", "D, G"),
    ("Architect", "Peter Hall", "Design architect (Stage III)", "from 19 Apr 1966", "D, G, L"),
    ("Architect", "Lionel Todd", "Contract documentation", "from 19 Apr 1966", "D, G"),
    ("Architect", "David Littlemore", "Supervision / contract administration", "from 19 Apr 1966", "D, G"),
    ("Architect", "E.H. (Ted) Farmer", "Government Architect, on the replacement panel", "from 19 Apr 1966", "D"),
    ("Builder", "Civil & Civic Pty Ltd", "Stage I — podium (missing from the Miro panel)", "1959–63", "A, D"),
    ("Builder", "M.R. Hornibrook (NSW) Pty Ltd", "Stages II (roof shells) and III (interiors)", "1962–73", "D, E, C"),
    ("Engineer", "Ove Arup & Partners", "Lead structural + civil engineer (who engaged them is a conflict)",
     "1957–73", "D, S"),
    ("Specialist consultant", "Steensen & Varming", "Mechanical engineers (harbour-water cooling)", "1957–73", "AA"),
    ("Specialist consultant", "Dr Vilhelm Lassen Jordan", "Acoustics (with Hall); Lothar Cremer advised Utzon",
     "1958–72", "M, AC"),
    ("Specialist consultant", "Rider Hunt & Partners", "Quantity surveyors [verify]", "from 1957", "AB"),
    ("Specialist consultant", "Geotechnical engineer", "No named firm found — the ground needed ~700 bored shafts",
     "1959", "A"),
    ("Supplier / manufacturer", "Ralph Symonds Ltd", "Plywood (mullions, ceilings) with Utzon; in receivership",
     "1961–65", "Y, X"),
    ("Supplier / manufacturer", "Waagner-Biro", "Stage machinery", "1961–72", "C, T"),
    ("Supplier / manufacturer", "GEC-Philips", "Light fittings", "1969", "C"),
    ("Supplier / manufacturer", "AWA", "Electronic services (subcontract to Hornibrook)", "1970", "C"),
    ("Supplier / manufacturer", "K.F. Plastics", "Acrylic acoustic reflectors", "1972", "M"),
    ("Supplier / manufacturer", "French glass maker", "6,200 m² of glass (name only in secondary sources)",
     "1968–71", "F"),
    ("Supplier / manufacturer", "Ronald Sharp", "Grand Organ (separate contract)", "1969–79", "O, P"),
    ("Supplier / manufacturer", "John Coburn", "Tapestry curtains (artist commission)", "1973", "N"),
]
