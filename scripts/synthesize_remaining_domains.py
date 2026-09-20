#!/usr/bin/env python3
"""Synthesize remaining 35 domains across applied engineering, business, humanities, trades, and governance."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"

REMAINING_DOMAINS: Dict[str, Dict[str, List[Tuple[str, str, str]]]] = {
    "biomedical-engineering": {
        "title": "Biomedical Engineering & Medical Devices",
        "skills": [
            ("medical-imaging", "Image reconstruction, MRI, CT, ultrasound algorithms, DICOM formats, and segmentation.", "low"),
            ("biomedical-signal-processing", "ECG, EEG, EMG filtering, wavelets, artifact removal, and physiological feature extraction.", "low"),
            ("prosthetics", "Upper/lower limb prosthetic design, socket mechanics, myoelectric control, and gait analysis.", "low"),
            ("orthotics", "Custom orthotic design, load redistribution, bracing biomechanics, and kinematic alignment.", "low"),
            ("medical-devices", "Design controls (ISO 13485, FDA 21 CFR 820), verification/validation, and risk management.", "medium"),
            ("biomaterials", "Biocompatibility testing (ISO 10993), surface biofunctionalization, titanium implants, and polymers.", "low"),
            ("biomechanics", "Musculoskeletal modeling, joint kinematics, finite element analysis of bone-implant interfaces.", "low"),
            ("rehabilitation-engineering", "Assistive robotics, neurorehabilitation devices, functional electrical stimulation (FES).", "low"),
            ("tissue-engineering", "Decellularized scaffolds, bioprinting, bioreactor cultivation, and stem cell differentiation.", "low"),
            ("neural-engineering", "Brain-computer interfaces (BCI), neural spike sorting, microelectrode arrays, and neurostimulation.", "low"),
            ("biosensors", "Enzymatic biosensors, lateral flow assays, surface plasmon resonance (SPR), and optical detection.", "low"),
            ("wearable-health", "Photoplethysmography (PPG), continuous glucose monitors, accelerometer metrics, and firmware.", "low"),
            ("clinical-engineering", "Hospital medical equipment lifecycle management, electrical safety testing, and calibration.", "medium"),
            ("medical-device-software", "SaMD development, IEC 62304 software lifecycle, cybersecurity, and clinical decision support.", "medium"),
            ("medical-device-regulation", "FDA 510(k), PMA submissions, CE mark under EU MDR, technical documentation, and post-market surveillance.", "low"),
        ]
    },
    "materials-science": {
        "title": "Materials Science & Advanced Engineering Materials",
        "skills": [
            ("metals", "Phase diagrams (Fe-C), heat treatment, dislocation theory, grain boundary strengthening, and alloys.", "low"),
            ("ceramics", "Sintering kinetics, fracture toughness, thermal shock resistance, and advanced structural ceramics.", "low"),
            ("polymers", "Glass transition temperature (Tg), viscoelasticity, rheology, polymer degradation, and thermoplastics.", "low"),
            ("composites", "Fiber-reinforced polymers (CFRP/GFRP), laminate theory, lay-up schedules, and failure criteria (Tsai-Wu).", "low"),
            ("biomaterials", "Bioinert vs bioactive ceramics (hydroxyapatite), biodegradable polymers (PLA/PGA), and blood contact.", "low"),
            ("nanomaterials", "Carbon nanotubes, graphene, quantum dots, 2D materials, and chemical vapor deposition (CVD).", "low"),
            ("semiconductors", "Direct/indirect bandgaps, doping profiles, silicon wafers, GaN/SiC wide-bandgap materials.", "low"),
            ("superconductors", "Type I and II superconductors, Cooper pairs, Meissner effect, high-Tc cuprates, and critical fields.", "low"),
            ("materials-characterization", "XRD diffraction, Rietveld refinement, DSC/TGA thermal analysis, and nanoindentation.", "low"),
            ("microscopy", "Scanning electron microscopy (SEM), transmission electron microscopy (TEM), AFM, and EDX spectroscopy.", "low"),
            ("crystallography", "Bravais lattices, Miller indices, space groups, reciprocal space, and X-ray crystallographic analysis.", "low"),
            ("corrosion", "Galvanic corrosion, pitting, stress corrosion cracking (SCC), passivation, and cathodic protection.", "low"),
            ("surface-engineering", "PVD, CVD, plasma spraying, anodizing, nitriding, and tribological wear resistance coatings.", "low"),
            ("additive-manufacturing-materials", "Metal powder atomization, polymer filaments, photopolymer resins, and defect porosity analysis.", "low"),
            ("computational-materials", "Density functional theory, molecular dynamics of lattices, CALPHAD phase equilibria modeling.", "low"),
        ]
    },
    "robotics": {
        "title": "Robotics, Autonomy & Cyber-Physical Systems",
        "skills": [
            ("robot-kinematics", "Forward and inverse kinematics, Denavit-Hartenberg parameters, Jacobians, and singular configurations.", "low"),
            ("robot-dynamics", "Euler-Lagrange and Newton-Euler dynamic equations, inertia matrices, Coriolis forces, and joint torques.", "low"),
            ("motion-planning", "Rapidly-exploring Random Trees (RRT*), Probabilistic Roadmaps (PRM), and trajectory generation.", "low"),
            ("path-planning", "A* search, Dijkstra on costmaps, potential fields, collision avoidance, and dynamic replanning.", "low"),
            ("localization", "Extended Kalman Filters (EKF), particle filters (Monte Carlo Localization), and wheel odometry fusion.", "low"),
            ("slam", "Simultaneous Localization and Mapping: visual SLAM, LiDAR SLAM, loop closure, and pose graph optimization.", "low"),
            ("computer-vision", "Camera calibration, stereo disparity, optical flow, YOLO object detection, and 3D bounding boxes.", "low"),
            ("robot-perception", "Point cloud filtering, plane segmentation, Euclidean clustering, and sensor synchronization.", "low"),
            ("sensor-fusion", "Multi-sensor integration (IMU, wheel encoders, GPS, LiDAR) with error-state Kalman filtering.", "low"),
            ("manipulation", "Pick-and-place pipelines, operational space control, impedance control, and contact force modeling.", "low"),
            ("grasping", "Grasp affordance estimation, Antipodal grasps, force closure, soft grippers, and tactile feedback.", "low"),
            ("humanoid-robots", "Bipedal gait synthesis, Zero Moment Point (ZMP), whole-body control, and balance stabilization.", "low"),
            ("mobile-robots", "Differential drive, Ackermann steering, omnidirectional kinematics, and local trajectory rollouts.", "low"),
            ("drones", "Quadrotor dynamics, attitude control, rotor aerodynamics, PX4 integration, and autonomous waypoints.", "medium"),
            ("industrial-robots", "6-axis articulated arms, SCARA, Delta robots, teach pendant workflows, and safety enclosures.", "low"),
            ("cobots", "Collaborative robots: power and force limiting (ISO/TS 15066), hand-guiding, and human-robot safety.", "low"),
            ("ros", "Robot Operating System 1: roscore, nodes, topics, services, catkin workspaces, and TF transformations.", "low"),
            ("ros2", "ROS2 architecture: DDS middleware, executors, composition, actions, lifecycle nodes, and colcon builds.", "low"),
            ("reinforcement-learning-robotics", "Sim-to-real transfer, domain randomization, policy gradients (PPO/SAC), and reward design.", "low"),
            ("robot-control", "Computed torque control, computed acceleration, sliding mode control, and active vibration suppression.", "low"),
            ("robot-simulation", "Gazebo, Isaac Sim, Webots, MuJoCo physical modeling, friction contacts, and sensor rendering.", "low"),
            ("robot-safety", "Emergency stop architectures, safety PLCs, light curtains, ISO 10218 certification compliance.", "medium"),
            ("robot-maintenance", "Joint harmonic drive inspection, cable harness checks, backlash calibration, and servo tuning.", "low"),
        ]
    },
    "social-science": {
        "title": "Social Sciences & Societal Research",
        "skills": [
            ("sociology", "Social stratification, institutional analysis, social capital, deviance, and sociological theory.", "low"),
            ("anthropology", "Cultural ethnography, kinship systems, linguistic anthropology, and participant observation.", "low"),
            ("economics", "Market equilibrium, consumer choice, institutional economics, and welfare theorems.", "low"),
            ("political-science", "Comparative politics, governance structures, electoral systems, power dynamics, and constitutionalism.", "low"),
            ("geography", "Human geography, spatial demographics, urban-rural divides, spatial segregation, and place analysis.", "low"),
            ("demography", "Cohort survival, fertility rates, mortality schedules, life expectancy, and population projections.", "low"),
            ("international-relations", "Realism, liberalism, constructivism, multilateral diplomacy, treaties, and geopolitical strategy.", "low"),
            ("public-policy", "Policy cycle, stakeholder analysis, policy formulation, regulatory impact analysis, and evaluation.", "low"),
            ("public-administration", "Bureaucratic organization, civil service governance, public budgeting, and administrative law.", "low"),
            ("development-studies", "Poverty metrics (MPI), sustainable development goals, foreign aid effectiveness, and rural development.", "low"),
            ("urban-studies", "Urbanization patterns, spatial zoning, transit-oriented development, housing affordability, and gentrification.", "low"),
            ("migration-studies", "Forced migration, labor immigration, assimilation theories, remittances, and asylum policies.", "low"),
            ("labor-studies", "Collective bargaining, labor union history, wage dispersion, precarious labor, and employment law.", "low"),
            ("gender-studies", "Intersectionality frameworks, gender wage gaps, social reproduction theory, and institutional analysis.", "low"),
            ("cultural-studies", "Subcultures, media representation, hegemonic culture, consumerism, and semiotic interpretation.", "low"),
            ("social-research", "Survey methodology, sampling theory, qualitative coding, grounded theory, and mixed-method design.", "low"),
        ]
    },
    "humanities": {
        "title": "Humanities, History & Cultural Heritage",
        "skills": [
            ("history", "Historical method, primary source corroboration, periodization, contextual analysis, and causal chains.", "low"),
            ("archaeology", "Stratigraphic excavation, typological sequencing, radiocarbon dating, and material culture analysis.", "low"),
            ("anthropology", "Anthropological theory, structuralism, cultural relativism, and cross-cultural ethnographic accounts.", "low"),
            ("classics", "Ancient Greek and Roman civilization, classical literature analysis, epic poetry, and political philosophy.", "low"),
            ("cultural-history", "Mentalities, intellectual movements, history of everyday life, material culture, and print culture.", "low"),
            ("art-history", "Iconography, stylistic attribution, formal visual analysis, art historical movements, and provenance.", "low"),
            ("historiography", "Schools of historical thought (Annales, Marxist, subaltern), narrative construction, and source bias.", "low"),
            ("archival-research", "Archival finding aids, paleographic transcription, manuscript collections, and archival ethics.", "low"),
            ("paleography", "Historical script identification, ductus analysis, ligatures, abbreviations, and textual transmission.", "low"),
            ("epigraphy", "Inscriptional analysis, stone and bronze monument decipherment, squeezing techniques, and lacunae.", "low"),
            ("heritage-preservation", "Architectural conservation, preventive monument preservation, UNESCO World Heritage guidelines.", "low"),
            ("museum-studies", "Curatorial practice, exhibit narrative design, collections accessioning, and visitor experience.", "low"),
            ("folklore", "Oral storytelling motifs, Aarne-Thompson-Uther index, folk rituals, and traditional vernacular culture.", "low"),
            ("cultural-heritage", "Intangible cultural heritage documentation, repatriation ethics, and cultural asset registries.", "low"),
        ]
    },
    "philosophy": {
        "title": "Philosophy & Ethical Systems",
        "skills": [
            ("epistemology", "Justified true belief, foundationalism vs coherentism, skepticism, epistemic virtue, and testimony.", "low"),
            ("metaphysics", "Ontology, modality (possible worlds), persistence over time, causality, free will, and constitution.", "low"),
            ("logic", "Formal syllogisms, propositional and predicate proofs, modal logic, fallacies, and soundness vs completeness.", "low"),
            ("ethics", "Deontology (Kantian ethics), consequentialism (utilitarianism), virtue ethics, and metaethics.", "low"),
            ("political-philosophy", "Social contract theory, theories of justice (Rawls, Nozick), liberty, legitimacy, and rights.", "low"),
            ("philosophy-of-science", "Falsificationism (Popper), paradigm shifts (Kuhn), scientific realism, and underdetermination.", "low"),
            ("philosophy-of-mind", "Dualism, physicalism, functionalism, qualia, intentionality, and the hard problem of consciousness.", "low"),
            ("philosophy-of-language", "Sense and reference (Frege), definite descriptions (Russell), speech acts, and language games.", "low"),
            ("aesthetics", "Theories of beauty, aesthetic judgement (Kant), ontology of artworks, and critical artistic interpretation.", "low"),
            ("applied-ethics", "Practical moral dilemmas in law, business, journalism, professional conduct, and animal rights.", "low"),
            ("bioethics", "Autonomy, beneficence, non-maleficence, justice, clinical trial ethics, and gene editing ethics.", "medium"),
            ("technology-ethics", "Surveillance ethics, algorithmic bias, technological determinism, digital rights, and transhumanism.", "low"),
            ("ai-ethics", "Value alignment, autonomous weapon systems, agent transparency, accountability, and AI moral status.", "low"),
            ("moral-reasoning", "Thought experiments (trolley problem), reflective equilibrium, moral dilemmas, and ethical deliberation.", "low"),
        ]
    },
    "economics": {
        "title": "Economics & Quantitative Econometrics",
        "skills": [
            ("microeconomics", "Consumer utility maximization, production functions, cost curves, market structures, and deadweight loss.", "low"),
            ("macroeconomics", "IS-LM framework, AD-AS models, monetary/fiscal policy transmission, inflation, and growth models (Solow).", "low"),
            ("econometrics", "OLS regression, endogeneity, instrumental variables (2SLS), difference-in-differences, and panel data.", "low"),
            ("development-economics", "Poverty traps, microcredit, institutional quality, land tenure, and randomized controlled trials.", "low"),
            ("labor-economics", "Human capital theory, wage determination, search and matching models (Mortensen-Pissarides), and minimum wages.", "low"),
            ("international-economics", "Ricardian comparative advantage, Heckscher-Ohlin model, trade tariffs, quotas, and exchange rates.", "low"),
            ("monetary-economics", "Central bank interest rate setting (Taylor rule), quantity theory of money, open market operations, and liquidity.", "low"),
            ("public-economics", "Public goods, externalities, Pigouvian taxes, optimal taxation theory (Mirrlees), and government expenditure.", "low"),
            ("behavioral-economics", "Bounded rationality, prospect theory, hyperbolic discounting, nudges, and behavioral market anomalies.", "low"),
            ("environmental-economics", "Cap-and-trade carbon markets, carbon taxes, contingent valuation, and cost of carbon abatement.", "low"),
            ("health-economics", "Health insurance moral hazard, adverse selection, QALY calculations, and healthcare cost containment.", "low"),
            ("industrial-organization", "Monopoly pricing, Cournot and Bertrand competition, market concentration (HHI), and antitrust analysis.", "low"),
            ("economic-forecasting", "ARIMA models, vector autoregression (VAR), leading economic indicators, and business cycle prediction.", "low"),
            ("economic-policy", "Macroeconomic stabilization plans, supply-side reforms, structural adjustments, and deficit management.", "low"),
            ("game-theory", "Repeated games, folk theorem, imperfect information, signaling games, and subgame perfect equilibria.", "low"),
            ("cost-benefit-analysis", "Net present value (NPV), social discount rates, economic internal rate of return (EIRR), and sensitivity testing.", "low"),
        ]
    },
    "accounting": {
        "title": "Accounting & Financial Auditing",
        "skills": [
            ("bookkeeping", "Double-entry bookkeeping, debit/credit journal entries, chart of accounts, and trial balance verification.", "low"),
            ("general-ledger", "GL account reconciliations, journal vouchers, subledger posting, and balance sheet integrity.", "low"),
            ("accounts-payable", "Vendor invoice processing, 3-way matching, payment batch scheduling, and 1099 compliance.", "low"),
            ("accounts-receivable", "Customer invoicing, credit limits, aging schedules, bad debt provisioning (CECL), and collections.", "low"),
            ("payroll-accounting", "Gross-to-net payroll journalizing, statutory employer taxes, benefits accruals, and deductions.", "low"),
            ("bank-reconciliation", "Matching bank statement feeds against general ledger cash accounts, identifying unposted items.", "low"),
            ("month-end-close", "Accruals, prepayments, depreciation schedules, intercompany eliminations, and close checklists.", "low"),
            ("financial-statements", "Preparation of Balance Sheet, Income Statement, Cash Flow Statement (indirect/direct), and Equity notes.", "low"),
            ("management-accounting", "Variance analysis, budget vs actual performance, contribution margin, and departmental allocations.", "low"),
            ("cost-accounting", "Activity-Based Costing (ABC), standard costing, overhead absorption, process costing, and inventory valuation.", "low"),
            ("forensic-accounting", "Detecting financial statement fraud, Benford law analysis, transaction tracing, and litigation support.", "low"),
            ("audit", "Audit planning, materiality thresholds, substantive testing, sampling methodologies, and audit workpapers.", "low"),
            ("internal-audit", "COSO internal controls framework, operational audits, risk-based audit programs, and remediation plans.", "low"),
            ("external-audit", "Independent statutory audit procedures, confirmation letters, going concern evaluation, and audit opinions.", "low"),
            ("revenue-recognition", "ASC 606 / IFRS 15 five-step framework: performance obligations, transaction price allocation, and timing.", "low"),
            ("fixed-assets", "Capital expenditure vs expense policies, depreciation methods (MACRS, straight-line), and asset disposal.", "low"),
            ("consolidation", "Multi-entity consolidations, intercompany balance eliminations, currency translation (CTA), and minority interest.", "low"),
            ("budgeting", "Zero-based budgeting, rolling quarterly forecasts, operational expense budgeting, and capital planning.", "low"),
            ("financial-reporting", "SEC filing disclosures (10-K, 10-Q), footnote drafting, MD&A analysis, and non-GAAP reconciliations.", "low"),
            ("ifrs", "International Financial Reporting Standards application, IFRS 16 lease accounting, and impairment testing.", "low"),
            ("gaap", "US GAAP rules, technical accounting memorandums, codification topic research (ASC), and compliance.", "low"),
        ]
    },
    "banking": {
        "title": "Banking, Payments & Financial Technology",
        "skills": [
            ("retail-banking", "Demand deposit accounts, certificates of deposit, consumer checking, branch operations, and overdrafts.", "low"),
            ("commercial-banking", "Commercial real estate lending, working capital credit facilities, syndicated loans, and covenants.", "low"),
            ("investment-banking", "Underwriting debt and equity offerings, IPO execution, fairness opinions, and valuation comps.", "low"),
            ("central-banking", "Monetary policy implementation, reserve requirements, discount window lending, and systemic stability.", "low"),
            ("lending", "Loan underwriting, debt service coverage ratio (DSCR), loan-to-value (LTV), and amortizing loan schedules.", "low"),
            ("credit-analysis", "Financial statement spread analysis, borrower capacity evaluation, and credit risk memorandum drafting.", "low"),
            ("credit-scoring", "FICO scoring models, probability of default (PD) estimation, loss given default (LGD), and scorecard rules.", "low"),
            ("trade-finance", "Letters of credit (LC), bank guarantees, documentary collections, export financing, and Incoterms.", "low"),
            ("treasury", "Cash positioning, daily liquidity management, money market investments, and foreign exchange hedging.", "low"),
            ("payments", "Automated Clearing House (ACH), Fedwire, CHIPS, real-time payments (FedNow, RTP), and SWIFT messaging.", "low"),
            ("payment-processing", "Merchant acquiring, payment gateways, interchange fees, card brand authorization, and settlement.", "low"),
            ("cards", "Credit, debit, prepaid card issuance, EMV chip specifications, PCI-DSS compliance, and chargebacks.", "low"),
            ("digital-banking", "Mobile banking UX flows, core banking APIs, neo-bank architectures, and biometric step-up authentication.", "low"),
            ("open-banking", "PSD2 compliance, Open Banking APIs, Account Information Service (AISP), and Payment Initiation (PISP).", "low"),
            ("fintech", "Embedded finance, Buy Now Pay Later (BNPL) mechanics, alternative credit data, and banking-as-a-service.", "low"),
            ("digital-lending", "Instant algorithmic loan decisioning, automated document verification, and digital promissory notes.", "low"),
            ("fraud-detection", "Card transaction fraud rules, velocity checks, device fingerprinting, and behavioral anomaly detection.", "medium"),
            ("aml", "Anti-Money Laundering transaction monitoring, suspicious activity reporting (SAR), and threshold reporting.", "medium"),
            ("kyc", "Know Your Customer identity verification, beneficial ownership validation, PEP screening, and sanction lists.", "medium"),
            ("financial-crime", "Sanctions evasion detection, terror financing investigations, bribery/FCPA screening, and risk scoring.", "medium"),
        ]
    },
    "entrepreneurship": {
        "title": "Entrepreneurship & Venture Creation",
        "skills": [
            ("idea-validation", "Smoke testing demand, landing page validation, problem-solution fit interviews, and willingness-to-pay.", "low"),
            ("customer-discovery", "The Mom Test interview framework, customer archetype profiling, and pain point quantification.", "low"),
            ("market-research", "TAM, SAM, SOM market sizing, competitor matrix positioning, and industry growth headwinds.", "low"),
            ("startup-business-model", "Business Model Canvas mapping, revenue models, cost structures, and network effect dynamics.", "low"),
            ("lean-startup", "Build-Measure-Learn feedback loops, pivot vs persevere criteria, and validated learning milestones.", "low"),
            ("mvp", "Scoping Minimum Viable Products, feature prioritization (MoSCoW), non-code prototype rapid deployment.", "low"),
            ("product-market-fit", "Sean Ellis 40% PMF metric, net retention cohorts, viral coefficients, and PMF scorecards.", "low"),
            ("pricing", "Value-based pricing strategies, tier packaging, freemium conversion mechanics, and annual discount sizing.", "low"),
            ("fundraising", "Venture capital rounds (Pre-Seed to Series B), investor pipeline CRM management, and deal timelines.", "low"),
            ("pitch-deck", "10-slide venture pitch deck design, narrative storytelling, market traction proof, and vision.", "low"),
            ("venture-capital", "Term sheet negotiation, liquidation preferences, pro-rata rights, drag-along, and valuation mechanics.", "low"),
            ("cap-table", "Capitalization table modeling, fully diluted shares, convertible notes, SAFEs, and option pool sizing.", "low"),
            ("startup-finance", "Burn rate calculation, zero-cash date runway projection, unit economics (LTV/CAC), and SaaS magic number.", "low"),
            ("hiring", "Early team compensation (equity vs cash), technical talent sourcing, culture fit screening, and offer closes.", "low"),
            ("go-to-market", "GTM channel selection, inbound vs outbound sales playbooks, early adopter acquisition, and launch PR.", "low"),
            ("founder-operations", "Co-founder alignment, board meeting preparation, corporate cadence (OKRs), and investor updates.", "low"),
            ("startup-legal", "Incorporation (Delaware C-Corp), founder stock vesting (83(b) election), IP assignment agreements.", "low"),
            ("startup-metrics", "Monthly Recurring Revenue (MRR), churn rate, quick ratio, customer acquisition cost, and gross margins.", "low"),
            ("exit-strategy", "M&A target acquisition positioning, strategic buyer courting, due diligence preparation, and IPO readiness.", "low"),
        ]
    },
    "public-relations": {
        "title": "Public Relations & Strategic Communications",
        "skills": [
            ("media-relations", "Building journalist relationships, press list curation, embargoes, and news hook alignment.", "low"),
            ("press-release", "Standard AP style press release drafting, compelling headlines, boilerplate copy, and wire submission.", "low"),
            ("press-kit", "Electronic press kit (EPK) compilation: high-res executive headshots, fact sheets, logos, and b-roll.", "low"),
            ("media-pitch", "Concise 150-word email pitches to reporters, customized angles, trending news tie-ins, and follow-ups.", "low"),
            ("crisis-communications", "Rapid response holding statements, crisis communication protocols, internal alignment, and damage control.", "medium"),
            ("reputation-management", "Brand sentiment tracking, search engine reputation management (SERM), and stakeholder trust rebuilding.", "low"),
            ("executive-communications", "CEO thought leadership bylines, LinkedIn long-form commentary, keynote speeches, and op-eds.", "low"),
            ("stakeholder-communications", "Town hall messaging, shareholder letters, partner notifications, and regulatory disclosures.", "low"),
            ("public-affairs", "Legislative advocacy communications, community outreach programs, and policy positioning papers.", "low"),
            ("community-relations", "Local philanthropic partnerships, community advisory councils, open houses, and sponsorship ROI.", "low"),
            ("spokesperson-preparation", "Media training, bridging techniques, message framing, tough question preparation, and broadcast readiness.", "low"),
            ("media-monitoring", "Tracking print, digital, and broadcast mentions, share of voice (SOV) calculation, and sentiment analysis.", "low"),
            ("communications-strategy", "Integrated corporate communications calendar, multi-channel narrative messaging architectures.", "low"),
        ]
    },
    "advertising": {
        "title": "Advertising & Paid Media Acquisition",
        "skills": [
            ("ad-copy", "High-converting direct response ad copy, hook generation, headline formulas, and CTA optimization.", "low"),
            ("campaign-planning", "Media mix modeling, budget pacing, campaign flighting schedules, and target reach/frequency goals.", "low"),
            ("media-buying", "Upfront negotiations, insertion orders (IO), rate cards, remnant inventory acquisition, and make-goods.", "low"),
            ("programmatic-advertising", "Demand-Side Platforms (DSP), Supply-Side Platforms (SSP), Real-Time Bidding (RTB), and header bidding.", "low"),
            ("search-advertising", "Google Ads search campaigns: keyword match types, negative keywords, Quality Score, and bid strategies.", "low"),
            ("display-advertising", "Banner ad sizes (IAB standards), HTML5 rich media creatives, audience remarketing, and viewability.", "low"),
            ("social-ads", "Paid Meta, TikTok, LinkedIn, YouTube ad architectures: custom audiences, lookalikes, and ad fatigue mitigation.", "low"),
            ("creative-testing", "Multivariate creative testing, dynamic creative optimization (DCO), asset iteration, and fatigue tracking.", "low"),
            ("audience-targeting", "First-party data segmentation, demographic/behavioral layering, and contextual targeting.", "low"),
            ("attribution", "Multi-touch attribution models (first-click, linear, time-decay, data-driven) and MMM calibration.", "low"),
            ("ad-analytics", "Return on Ad Spend (ROAS), Customer Acquisition Cost (CAC), Click-Through Rate (CTR), and Cost per Mille (CPM).", "low"),
            ("conversion-tracking", "Server-side Conversions API (CAPI), Google Tag Manager event tags, offline conversion uploads.", "low"),
            ("landing-page-optimization", "Pre-click to post-click messaging congruence, mobile page speed, form friction removal, and A/B tests.", "low"),
            ("advertising-compliance", "FTC endorsement guidelines, ad disclosure standards, privacy regulations, and platform ad policies.", "low"),
        ]
    },
    "social-media": {
        "title": "Social Media Strategy & Community Growth",
        "skills": [
            ("social-strategy", "Cross-platform brand voice positioning, content pillars, audience demographic alignment, and channel mix.", "low"),
            ("content-calendar", "Editorial scheduling, batch content production workflows, posting cadence, and seasonal campaign hooks.", "low"),
            ("community-management", "Daily comment engagement, direct message reply protocols, brand advocacy cultivation, and super-fan recognition.", "low"),
            ("moderation", "Automated profanity filtering, troll mitigation, brand safety guardrails, and community guidelines enforcement.", "low"),
            ("social-listening", "Brand keyword monitoring, sentiment tracking, industry hashtag trends, and competitor social benchmarking.", "low"),
            ("influencer-management", "Influencer discovery, contract agreements, creative briefs, affiliate codes, and campaign deliverables.", "low"),
            ("creator-collaboration", "Co-marketing content, live audio/video guest spots, takeover campaigns, and creator compensation.", "low"),
            ("social-analytics", "Engagement rate calculations, video retention curves, organic impressions, and viral reach metrics.", "low"),
            ("short-form-video", "Reels/TikTok/Shorts scriptwriting, 3-second hook design, audio trending integration, and text overlay.", "low"),
            ("platform-strategy", "Platform-specific algorithmic nuances for LinkedIn, X (Twitter), Instagram, TikTok, Threads, and YouTube.", "low"),
            ("hashtag-research", "High-volume vs niche hashtag clustering, hashtag count testing, and discovery reach expansion.", "low"),
            ("audience-growth", "Organic engagement strategies, giveaways, collaborative posting, and audience retention tactics.", "low"),
            ("social-commerce", "TikTok Shop, Instagram Shopping integration, live-stream shopping workflows, and product tag tracking.", "low"),
            ("crisis-response", "Social media crisis escalation protocols, pause-publishing triggers, and approved public statements.", "low"),
        ]
    },
    "presentation": {
        "title": "Presentation Design & Executive Storytelling",
        "skills": [
            ("slide-design", "Visual hierarchy, grid layouts, whitespace balance, typography pairings, and clean slide design.", "low"),
            ("powerpoint", "Advanced Microsoft PowerPoint: master slides, custom color themes, animation triggers, and morph transitions.", "low"),
            ("google-slides", "Google Slides collaboration, add-ons, shared templates, and cloud presentation distribution.", "low"),
            ("keynote", "Apple Keynote presentation effects, Magic Move transitions, vector shape editing, and export workflows.", "low"),
            ("presentation-storytelling", "Three-act narrative structure, McKinsey pyramid principle, problem-complication-resolution arcs.", "low"),
            ("executive-presentations", "Boardroom presentation decks: appendix heavy, high signal-to-noise ratio, and decision slides.", "low"),
            ("technical-presentations", "Translating complex architectural diagrams, code snippets, and benchmark metrics for broad audiences.", "low"),
            ("academic-presentations", "Research seminar slides, methodology defense, statistical visualization, and conference presentations.", "low"),
            ("pitch-decks", "Venture capital investor pitch deck flow, traction proof, unit economics visualization, and exit potential.", "low"),
            ("conference-presentations", "Keynote address slides, stage visibility considerations, large-format font sizing, and visual impact.", "low"),
            ("speaker-notes", "Concise speaker cue cards, transition prompts, timing reminders, and audience interaction triggers.", "low"),
            ("public-speaking", "Vocal variety, pacing, eye contact techniques, stage presence, and overcoming public speaking anxiety.", "low"),
            ("speech-delivery", "Teleprompter reading, conversational speech delivery, Q&A handling, and pacing under pressure.", "low"),
            ("presentation-rehearsal", "Dry run evaluation protocols, timing check gates, slide transition practice, and feedback scoring.", "low"),
            ("presentation-accessibility", "Color contrast checking (WCAG), alt text on presentation graphics, and screen-reader accessible decks.", "low"),
        ]
    },
    "documentation": {
        "title": "Technical Documentation & Information Architecture",
        "skills": [
            ("technical-writing", "Clear, concise technical prose, active voice, task-based documentation, and style guide adherence.", "low"),
            ("api-documentation", "OpenAPI (Swagger) specification drafting, endpoint descriptions, request/response JSON schemas.", "low"),
            ("developer-documentation", "Quickstart guides, SDK documentation, code walkthroughs, error reference tables, and interactive sandboxes.", "low"),
            ("user-guides", "Step-by-step end-user onboarding guides, annotated UI screenshots, and feature tutorials.", "low"),
            ("manuals", "Comprehensive hardware and software system operator manuals, installation guides, and safety warnings.", "low"),
            ("runbooks", "Operational runbooks: incident troubleshooting trees, service restart procedures, and alert mitigation steps.", "low"),
            ("standard-operating-procedures", "ISO compliant Standard Operating Procedures (SOP): scope, responsibilities, step workflows, and revision history.", "low"),
            ("knowledge-bases", "Help center information architecture, topic taxonomy, article interlinking, and maintenance cycles.", "low"),
            ("wikis", "Internal engineering wiki structuring (Confluence, Notion), team spaces, and onboarding playbooks.", "low"),
            ("architecture-documents", "Architecture Decision Records (ADR), C4 model diagrams, system context, and component diagrams.", "low"),
            ("requirements-documents", "Product Requirement Documents (PRD), functional specifications, acceptance criteria, and user stories.", "low"),
            ("specifications", "Formal engineering specifications, interface control documents (ICD), and contractual deliverable specs.", "low"),
            ("changelogs", "Keep a Changelog standard format: Added, Changed, Deprecated, Removed, Fixed, and Security categories.", "low"),
            ("release-notes", "Customer-facing release summaries, benefit highlights, migration warnings, and bug fix announcements.", "low"),
            ("documentation-auditing", "Reviewing documentation freshness, verifying code sample execution, and dead link auditing.", "low"),
        ]
    },
    "training": {
        "title": "Corporate Training & Instructional Design",
        "skills": [
            ("corporate-training", "Workforce learning strategy, training needs analysis (TNA), and learning management system (LMS) deployment.", "low"),
            ("employee-training", "Skill gap assessments, job-specific training modules, interactive workshops, and skill tracking.", "low"),
            ("onboarding", "30-60-90 day employee onboarding roadmaps, culture assimilation, tool setup, and buddy programs.", "low"),
            ("compliance-training", "Mandatory regulatory training: anti-harassment, data privacy, cybersecurity awareness, and tracking.", "low"),
            ("technical-training", "Engineering bootcamps, hands-on coding labs, system architecture workshops, and tooling upskilling.", "low"),
            ("leadership-training", "Management fundamentals, coaching frameworks (GROW model), performance reviews, and conflict mediation.", "low"),
            ("sales-training", "Sales methodology enablement (MEDDIC, Challenger), pitch practice, objection handling roleplays.", "low"),
            ("customer-training", "Customer education programs, customer LMS academy design, onboarding webinars, and certifications.", "low"),
            ("instructor-led-training", "Facilitation techniques, breakout room coordination, audience engagement, and whiteboarding exercises.", "low"),
            ("train-the-trainer", "Coaching subject matter experts to deliver engaging instructional content, pacing, and feedback rubrics.", "low"),
            ("competency-frameworks", "Defining role proficiency levels (Novice to Master), skill rubrics, and promotion readiness criteria.", "low"),
            ("certification-programs", "Designing professional certification exams, question banks, proctoring standards, and recertification.", "low"),
            ("training-evaluation", "Kirkpatrick four-level training evaluation model: Reaction, Learning, Behavior, and Business Results.", "low"),
        ]
    },
    "tutoring": {
        "title": "Academic Tutoring & Adaptive Learning",
        "skills": [
            ("math-tutoring", "Socratic math coaching, breaking complex equations into conceptual steps, and visual proofs.", "low"),
            ("science-tutoring", "Physics and chemistry intuition building, laboratory concept review, and scientific method drills.", "low"),
            ("programming-tutoring", "Code walkthroughs, debugging coaching, algorithmic mental models, and syntax correction drills.", "low"),
            ("language-tutoring", "Target language conversational practice, grammar correction in context, and listening comprehension.", "low"),
            ("homework-support", "Guiding students to find answers independently without solving problems directly.", "low"),
            ("exam-preparation", "Standardized test strategy (SAT, GRE, AP), time management drills, and error review logs.", "low"),
            ("concept-explanation", "Feynman technique, intuitive analogies, multi-modal explanations, and checking for comprehension.", "low"),
            ("practice-generation", "Generating tailored problem sets with step-by-step difficulty scaling and varied contexts.", "low"),
            ("feedback", "Formative educational feedback: highlighting successes, diagnosing conceptual errors, and encouragement.", "low"),
            ("adaptive-learning", "Dynamic learning path adjustments based on student error patterns and cognitive readiness.", "low"),
            ("study-planning", "Spaced repetition study schedules, Pomodoro session structures, and exam countdown milestones.", "low"),
        ]
    },
    "ai-governance": {
        "title": "AI Governance, Safety & Risk Management",
        "skills": [
            ("ai-risk-management", "NIST AI RMF (Map, Measure, Manage, Govern), ISO/IEC 42001 AI management system implementation.", "medium"),
            ("model-cards", "Standardized model cards: intended use cases, training data provenance, evaluation metrics, and limitations.", "low"),
            ("data-cards", "Dataset documentation: collection methodology, demographic representation, consent, and licensing.", "low"),
            ("ai-inventory", "Enterprise AI asset cataloging, risk tier classification, deployment tracking, and dependency mapping.", "low"),
            ("model-governance", "Model approval boards, validation checklists, lifecycle stage transitions, and decommission policies.", "low"),
            ("ai-policy", "Drafting corporate acceptable use policies for generative AI, proprietary data safeguards, and third-party tools.", "low"),
            ("responsible-ai", "Operationalizing fairness, accountability, transparency, safety, and human-in-the-loop oversight.", "low"),
            ("ai-compliance", "EU AI Act compliance: prohibited systems, high-risk conformity assessments, CE marking, and post-market logs.", "medium"),
            ("algorithmic-impact-assessment", "Assessing societal impact, disparate impact on protected classes, and fundamental rights risks.", "low"),
            ("human-oversight", "Designing human-in-the-loop (HITL), human-on-the-loop, and human-in-command operational safeguards.", "low"),
            ("ai-audit", "Independent technical audits of AI pipelines, training log verification, and bias assessment.", "medium"),
            ("provenance", "C2PA content credentials, synthetic media watermarking, cryptographic signing of model outputs.", "low"),
            ("transparency", "Clear user disclosures of AI interactions, system capabilities, and uncertainty calibration.", "low"),
            ("explainability", "SHAP, LIME, counterfactual explanations, attention heatmaps, and feature importance interpretations.", "low"),
            ("fairness", "Disparate impact ratio, equalized odds, demographic parity, and bias mitigation algorithms.", "low"),
            ("model-retirement", "Decommissioning legacy AI models: data purging, downstream dependency re-routing, and archiving.", "low"),
        ]
    },
    "privacy": {
        "title": "Privacy Engineering & Data Protection",
        "skills": [
            ("privacy-engineering", "Architecting systems for privacy: encryption at rest/transit, zero-knowledge proofs, and secure enclaves.", "low"),
            ("data-minimization", "Designing schemas that collect only strictly necessary attributes, tokenization, and field omission.", "low"),
            ("consent-management", "Consent collection UX, granular preferences, CMP integration, and withdrawal audit trails.", "low"),
            ("privacy-impact-assessment", "Data Protection Impact Assessments (DPIA): processing risk evaluation, necessity checks, and mitigation.", "low"),
            ("anonymization", "k-anonymity, l-diversity, t-closeness, record suppression, and k-factor calculations.", "low"),
            ("pseudonymization", "Deterministic and randomized tokenization, keyed hashing, and separate re-identification tables.", "low"),
            ("differential-privacy", "Epsilon-delta differential privacy, Laplace/Gaussian noise mechanisms, and privacy budget management.", "low"),
            ("privacy-by-design", "Integrating Cavoukian 7 foundational principles of Privacy by Design into software development lifecycles.", "low"),
            ("data-retention", "Automated data expiration policies, hard vs soft deletion, database purging jobs, and compliance.", "low"),
            ("data-subject-rights", "Executing DSAR requests: right to access, right to rectification, right to erasure ('right to be forgotten').", "low"),
            ("cookie-compliance", "ePrivacy Directive rules, script blocking prior to consent, and cookie categorization.", "low"),
            ("tracking-privacy", "Limiting fingerprinting, third-party pixel governance, and mobile App Tracking Transparency (ATT).", "low"),
            ("privacy-program-management", "Building privacy governance teams, record of processing activities (ROPA / Article 30), and audits.", "low"),
            ("data-mapping", "Creating comprehensive data lineage diagrams, cross-border transfer mapping, and vendor data flows.", "low"),
            ("privacy-auditing", "Auditing database access logs, verifying encryption key rotation, and privacy policy compliance checks.", "low"),
        ]
    },
    "compliance": {
        "title": "Regulatory Compliance & Risk Frameworks",
        "skills": [
            ("regulatory-compliance", "Mapping legal statutes to operational controls, maintaining compliance registers, and audits.", "low"),
            ("policy-management", "Drafting, reviewing, approving, and distributing corporate policy documents with version control.", "low"),
            ("control-frameworks", "Implementing NIST CSF, CIS Controls, COSO, and mapping controls across multiple frameworks.", "low"),
            ("internal-controls", "Segregation of duties (SoD), access approvals, dual authorization, and preventive/detective controls.", "low"),
            ("compliance-testing", "Sample testing of internal controls, walk-through tests, and deficiency remediation plans.", "low"),
            ("compliance-monitoring", "Continuous compliance monitoring, SIEM alerts, automated configuration drift detection.", "low"),
            ("risk-assessment", "Qualitative and quantitative risk matrices, threat likelihood x impact, and risk treatment registers.", "low"),
            ("audit-preparation", "Gathering audit evidence artifacts, population lists, sampling packages, and PBC lists.", "low"),
            ("regulatory-reporting", "Preparing and filing mandatory disclosures to regulatory bodies (SEC, FINRA, FTC, FCA).", "low"),
            ("gdpr", "General Data Protection Regulation: legal bases for processing, DPO obligations, 72-hour breach notices.", "low"),
            ("hipaa", "Health Insurance Portability and Accountability Act: Security Rule, Privacy Rule, BAA agreements.", "medium"),
            ("pci-dss", "Payment Card Industry Data Security Standard (v4.0): cardholder data environment (CDE) segmentation.", "medium"),
            ("soc2", "System and Organization Controls (SOC 2 Type I/II): Trust Services Criteria (Security, Availability, Confidentiality).", "low"),
            ("iso-27001", "Information Security Management System (ISMS): Statement of Applicability (SoA), risk assessment, and Annex A.", "low"),
            ("iso-9001", "Quality Management Systems (QMS): process approach, continuous improvement (PDCA), and customer focus.", "low"),
            ("industry-compliance", "Vertical compliance standards: Sarbanes-Oxley (SOX), GLBA, FERC/NERC, and FDA cGMP.", "low"),
        ]
    },
    "integration": {
        "title": "Systems Integration & Middleware",
        "skills": [
            ("api-integration", "Consuming third-party REST/GraphQL APIs, OAuth2 authentication, rate limiting, and response parsing.", "low"),
            ("webhook-integration", "Receiving, verifying HMAC signatures, deduplicating, and acknowledging async webhook events.", "low"),
            ("etl-integration", "Connecting heterogeneous data sources, schema transformation, and database syncing.", "low"),
            ("middleware", "Message brokers, enterprise service bus (ESB) routing, request transformations, and protocol bridging.", "low"),
            ("enterprise-integration", "Enterprise Integration Patterns (EIP): splitter, aggregator, content-based router, and message filters.", "low"),
            ("erp-integration", "Connecting modern cloud apps to SAP, Oracle, NetSuite via BAPI, OData, and intermediate tables.", "low"),
            ("crm-integration", "Bi-directional syncing between Salesforce, HubSpot, and internal databases with conflict resolution.", "low"),
            ("identity-integration", "SAML 2.0, OpenID Connect (OIDC), SCIM user provisioning with Okta, Azure AD, and Ping.", "low"),
            ("payment-integration", "Integrating Stripe, Adyen, PayPal SDKs, webhooks, idempotency keys, and payment intents.", "low"),
            ("messaging-integration", "Integrating Slack, Microsoft Teams, WhatsApp Business API for operational alerts and chat.", "low"),
            ("event-driven-integration", "Publish-subscribe architectures using AWS SNS/SQS, Google Pub/Sub, and EventBridge.", "low"),
            ("data-synchronization", "Two-way data sync, optimistic concurrency, conflict resolution timestamps, and tombstones.", "low"),
            ("system-interoperability", "Data format interchange (JSON, XML, Protocol Buffers, FlatBuffers) and standards compliance.", "low"),
        ]
    },
    "migration": {
        "title": "System Migration & Modernization",
        "skills": [
            ("database-migration", "Zero-downtime database schema migrations, expand-contract pattern, and rollback scripts.", "medium"),
            ("cloud-migration", "Rehosting (lift-and-shift), replatforming, and refactoring on-premise workloads to AWS/Azure/GCP.", "low"),
            ("application-modernization", "Decomposing legacy monoliths into microservices, containerization, and 12-factor architecture.", "low"),
            ("legacy-migration", "Migrating COBOL, mainframe, or legacy VB systems to modern, modular cloud microservices.", "low"),
            ("data-migration", "Large-scale bulk data extraction, schema mapping, staging verification, and reconciliation counts.", "low"),
            ("platform-migration", "Switching infrastructure providers, PaaS migrations, Kubernetes cluster migrations with cutover plans.", "low"),
            ("cms-migration", "Migrating structured content, assets, redirects (301s), and authoring permissions between CMS platforms.", "low"),
            ("crm-migration", "Migrating customer history, opportunity pipelines, lead assignments, and activity logs without data loss.", "low"),
            ("erp-migration", "Enterprise resource planning cutovers: master data cleansing, parallel runs, and go-live checklists.", "low"),
            ("identity-migration", "Migrating user passwords, hashed credentials, MFA tokens, and directory roles seamlessly.", "medium"),
            ("email-migration", "Migrating corporate email accounts, MX record DNS cutovers, PST migrations, and DKIM/SPF setups.", "low"),
            ("repository-migration", "Migrating Git histories, tags, pull requests, CI pipelines from GitLab/Bitbucket to GitHub.", "low"),
            ("migration-validation", "Data integrity checksumming, shadow production traffic testing, and automated smoke test validation.", "low"),
        ]
    },
    "archiving": {
        "title": "Archival Science & Records Management",
        "skills": [
            ("records-management", "Records lifecycle management: creation, active use, inactive storage, and final disposition.", "low"),
            ("digital-preservation", "OAIS reference model, file format obsolescence mitigation (PDF/A, TIFF), and bit preservation.", "low"),
            ("document-retention", "Drafting and enforcing corporate record retention schedules by record category and legal mandate.", "low"),
            ("metadata-management", "Dublin Core, EAD, PREMIS metadata standards, cataloging rules, and provenance tracking.", "low"),
            ("archival-description", "ISAD(G) hierarchical archival description: fonds, series, files, and items.", "low"),
            ("records-classification", "Developing business classification schemes, functional taxonomy trees, and file plans.", "low"),
            ("retention-schedules", "Statutory audit retention, tax record lifespans, employee record preservation, and legal time limits.", "low"),
            ("legal-holds", "Issuing, tracking, and releasing litigation holds to suspend routine destruction of evidence.", "low"),
            ("information-governance", "Policy frameworks balancing corporate data value, storage costs, and legal compliance risks.", "low"),
            ("digital-forensics-preservation", "Forensic disk imaging (E01), write blockers, SHA-256 chain of custody logging.", "medium"),
            ("historical-archives", "Special collections appraisal, deacidification, climate-controlled storage, and finding aid access.", "low"),
            ("repository-management", "Digital asset repository software (DSpace, Fedora), ingest pipelines, and accession registers.", "low"),
        ]
    },
    "emergency": {
        "title": "Emergency & Disaster Management",
        "skills": [
            ("emergency-planning", "All-hazards emergency operations plans (EOP), threat vulnerability assessments, and annexes.", "medium"),
            ("disaster-preparedness", "Community preparedness campaigns, emergency kit supplies, drills, and early warning systems.", "low"),
            ("evacuation-planning", "Evacuation route mapping, contraflow traffic plans, transit-dependent population transport.", "medium"),
            ("crisis-communications", "Public emergency alert systems (EAS, WEA), bilingual emergency broadcasts, and media briefings.", "medium"),
            ("business-continuity", "Business Continuity Plans (BCP), Business Impact Analysis (BIA), and alternate operating facilities.", "low"),
            ("disaster-recovery", "IT disaster recovery plans, Recovery Time Objective (RTO), Recovery Point Objective (RPO), failovers.", "low"),
            ("emergency-logistics", "Staging areas, points of distribution (POD), critical supply chain mobilization, and mutual aid.", "medium"),
            ("incident-command", "FEMA Incident Command System (ICS 100/700/800): unified command, incident action plans (IAP).", "medium"),
            ("emergency-operations-center", "EOC activation levels, ESF (Emergency Support Functions) coordination, and situational reports.", "medium"),
            ("disaster-assessment", "Preliminary Damage Assessments (PDA), FEMA public/individual assistance declarations, and GIS mapping.", "low"),
            ("humanitarian-response", "Sphere standards for disaster response: water supply, sanitation, food, and shelter minimums.", "medium"),
            ("search-and-rescue", "Urban search and rescue (USAR) marking systems, triage categories, search grids, and canine teams.", "medium"),
            ("shelter-management", "Mass care shelter operations, American Red Cross shelter guidelines, registration, and accessibility.", "medium"),
            ("recovery-planning", "Long-term disaster recovery frameworks, hazard mitigation grants (HMGP), and community rebuilding.", "low"),
        ]
    },
    "accessibility": {
        "title": "Accessibility & Inclusive Design",
        "skills": [
            ("wcag", "Web Content Accessibility Guidelines (WCAG 2.2 AA/AAA) success criteria, normative requirements.", "low"),
            ("screen-readers", "Testing with NVDA, JAWS, VoiceOver, and TalkBack: virtual cursor navigation and announcement flow.", "low"),
            ("keyboard-accessibility", "Logical tab order, visible focus indicators, skip navigation links, and trap-free focus management.", "low"),
            ("aria", "Accessible Rich Internet Applications (WAI-ARIA): roles, states, properties, and live regions.", "low"),
            ("low-vision", "Color contrast ratios (4.5:1 / 3:1), 200% text resize without loss of content, and high-contrast modes.", "low"),
            ("deaf-hard-of-hearing", "Synchronized closed captions, transcript availability, and visual audio alerts.", "low"),
            ("cognitive-accessibility", "Plain language guidelines, consistent navigation, error prevention, and distraction-free modes.", "low"),
            ("motor-accessibility", "Target touch sizes (minimum 24x24 / 44x44 px), pointer gestures, and switch access compatibility.", "low"),
            ("accessible-documents", "Creating accessible Word, Excel, and EPUB files: heading structure, reading order, and alt text.", "low"),
            ("accessible-pdfs", "PDF/UA standards, Acrobat Pro tag trees, reading order verification, and artifact tagging.", "low"),
            ("accessible-presentations", "Accessible slide layouts, unique slide titles, color contrast, and descriptive visuals.", "low"),
            ("accessible-video", "Closed captions (CC), open captions, audio description tracks, and media player accessibility.", "low"),
            ("captions", "Subtitle timing, speaker identification, ambient noise notation, and formatting standards.", "low"),
            ("audio-description", "Narrating essential visual elements, actions, facial expressions, and scene changes during audio pauses.", "low"),
            ("assistive-technology", "Compatibility testing with braille displays, sip-and-puff switches, eye-tracking devices, and speech input.", "low"),
            ("accessible-design", "Inclusive design systems: accessible typography, color tokens, semantic iconography, and focus rings.", "low"),
            ("accessible-software", "Section 508 and EN 301 549 software compliance, OS accessibility API integration (MSAA, UI Automation).", "low"),
            ("accessible-web", "Semantic HTML5 elements (main, nav, article), accessible form controls, and aria-describedby.", "low"),
            ("accessible-mobile", "iOS Accessibility APIs (UIAccessibility) and Android AccessibilityNodeInfo implementations.", "low"),
            ("accessibility-testing", "Automated accessibility scanners (axe-core, Lighthouse), manual testing checklists, and VPAT drafting.", "low"),
        ]
    },
    "3d": {
        "title": "3D Graphics, Modeling & Animation",
        "skills": [
            ("3d-modeling", "Polygon modeling, subdivision surfaces, edge flow topology, quad-based geometry, and beveling.", "low"),
            ("3d-animation", "Keyframing, graph editor curves, principles of animation (squash/stretch, anticipation), and timing.", "low"),
            ("rendering", "Path tracing, ray tracing, global illumination, ambient occlusion, PBR shaders, and render engines.", "low"),
            ("texturing", "Substance Painter workflows, PBR metallic/roughness maps, diffuse, normal, and displacement maps.", "low"),
            ("uv-mapping", "UV unwrapping, seam placement, texel density consistency, minimizing distortion, and packing islands.", "low"),
            ("rigging", "Forward and Inverse Kinematics (FK/IK), bone hierarchies, weight painting, constraints, and control rigs.", "low"),
            ("character-modeling", "Anatomical proportions, facial topology for animation, hair card generation, and clothing simulation.", "low"),
            ("environment-modeling", "Modular environment kit creation, architectural trim sheets, foliage generation, and landscape dressing.", "low"),
            ("sculpting", "Digital clay sculpting (ZBrush, Blender), dynamesh, alpha brushes, detailing wrinkles, and retopology.", "low"),
            ("procedural-modeling", "Node-based geometry generation, procedural building systems, scatter tools, and algorithmic shapes.", "low"),
            ("cad", "Precision parametric solids, NURBS curves, boundary representation (B-Rep), and STEP/IGES exports.", "low"),
            ("3d-printing", "STL mesh repair, slicing configurations (infill, supports, layer height), bed adhesion, and print orientation.", "low"),
            ("photogrammetry", "Mesh reconstruction from multi-angle photographs, texture baking, and reality capture cleanup.", "low"),
            ("motion-capture", "Optical and inertial MoCap data cleanup, retargeting onto character skeletons, and smoothing.", "low"),
            ("blender", "Blender geometry nodes, Cycles/Eevee rendering, Python scripting API, and open-source production pipelines.", "low"),
            ("maya", "Autodesk Maya production rigging, MASH procedural animation, Arnold rendering, and MEL/Python scripting.", "low"),
            ("3ds-max", "Autodesk 3ds Max architectural visualization, modifier stack workflows, and V-Ray/Corona rendering.", "low"),
            ("houdini", "SideFX Houdini procedural VEX programming, pyro/liquid simulation, VDB volumes, and digital assets (HDA).", "low"),
            ("unreal-engine", "Unreal Engine 5 Nanite geometry, Lumen real-time lighting, Blueprint scripting, and Niagara VFX.", "low"),
            ("digital-twins", "High-fidelity real-time 3D digital replicas of physical assets with live telemetry overlays.", "low"),
        ]
    },
    "branding": {
        "title": "Branding & Visual Identity Systems",
        "skills": [
            ("brand-strategy", "Defining brand mission, vision, values, value proposition, and overarching strategic brand positioning.", "low"),
            ("brand-positioning", "Perceptual mapping, competitive differentiation, category creation, and distinctive brand assets.", "low"),
            ("naming", "Company and product naming frameworks: linguistic screening, trademark availability, and domain vetting.", "low"),
            ("logo-design", "Logomark and wordmark craft: silhouette testing, scalability checks, vector perfection, and iconography.", "low"),
            ("visual-identity", "Cohesive visual language: primary/secondary colors, geometric systems, image treatments, and layout rules.", "low"),
            ("brand-guidelines", "Authoring comprehensive brand style guides (brand books): do's and don'ts, logo clearance, and usage.", "low"),
            ("typography", "Typeface hierarchy: pairing display and body typefaces, kerning, leading, tracking, and licensing.", "low"),
            ("color-systems", "Harmonious brand color palettes: digital hex/RGB, print CMYK, Pantone matching, and color psychology.", "low"),
            ("tone-of-voice", "Defining verbal identity, brand personality dimensions, writing samples, and editorial voice guidelines.", "low"),
            ("brand-messaging", "Brand narrative, elevator pitch, taglines, customer benefit pillars, and messaging matrices.", "low"),
            ("brand-architecture", "Masterbrand (monolithic), endorsed brand, and house of brands (freestanding) portfolio structuring.", "low"),
            ("rebranding", "Managing brand evolution or overhaul, stakeholder management, rollout communication, and asset migration.", "low"),
            ("brand-audits", "Evaluating touchpoint consistency, brand recognition metrics, market perception surveys, and equity gaps.", "low"),
            ("employer-branding", "Employee value proposition (EVP), recruitment marketing materials, and internal culture branding.", "low"),
            ("personal-branding", "Individual professional positioning, executive bios, LinkedIn profile optimization, and thought leadership.", "low"),
        ]
    },
    "film-tv": {
        "title": "Film, Television & Video Production",
        "skills": [
            ("screenwriting", "Industry-standard screenplay formatting, 3-act structure, dialogue rhythm, scene headings, and character arcs.", "low"),
            ("storyboarding", "Visual framing, shot progression, camera angle annotations, aspect ratio framing, and animatics.", "low"),
            ("pre-production", "Script breakdowns, production schedules, day-out-of-days (DOOD), call sheets, and location scouting.", "low"),
            ("casting", "Casting breakdown notices, audition sides, callback evaluation, and talent deal memorandums.", "low"),
            ("directing", "Blocking actors, visual style execution, performance coaching, shot lists, and coverage strategy.", "low"),
            ("cinematography", "Lens selection (focal lengths), camera sensor formats, exposure triangle, camera movement, and composition.", "low"),
            ("lighting", "Three-point lighting, motivated lighting, color temperature (Kelvin), CRI ratings, and light modifier control.", "low"),
            ("sound-recording", "Boom microphone technique, wireless lavaliers, room tone recording, gain staging, and field sound mixers.", "low"),
            ("production-management", "Line producing, production budget tracking (Movie Magic), permits, unions (SAG-AFTRA, DGA, IATSE).", "low"),
            ("location-management", "Location agreements, permit acquisition, insurance certificates, logistics, and tech scouts.", "low"),
            ("editing", "Nonlinear editing (Premiere, DaVinci Resolve, Final Cut): J/L cuts, pacing, match cuts, and montage editing.", "low"),
            ("color-grading", "Log-to-Rec.709 conversions, color balance, skin tone lines, creative LUT application, and HDR mastering.", "low"),
            ("visual-effects", "Chroma keying (green screen), planar tracking, rotoscoping, clean plating, and composite integration.", "low"),
            ("motion-graphics", "Title sequences, kinetic typography, lower thirds, 2D vector animation in After Effects.", "low"),
            ("post-production", "Post-production pipeline: offline/online edit conforming, sound design (foley, ADR), and picture lock.", "low"),
            ("subtitling", "Closed and open caption delivery, SRT/XML formats, line-by-line reading speed constraints.", "low"),
            ("dubbing", "Foreign language dub script adaptation, voice actor direction, and sync mixing.", "low"),
            ("distribution", "DCP (Digital Cinema Package) creation, streaming delivery specs (Netflix, Apple TV), and theatrical deliveries.", "low"),
            ("film-marketing", "Theatrical trailer cutting, key art posters, film festival submission strategies, and press kits.", "low"),
            ("film-rights", "Option purchase agreements, chain of title verification, music clearances, and synchronization licenses.", "low"),
        ]
    },
    "music": {
        "title": "Music Theory, Audio Engineering & Music Business",
        "skills": [
            ("music-theory", "Scale modes (Dorian, Mixolydian), chord progressions (circle of fifths), voice leading, and intervals.", "low"),
            ("composition", "Motif development, thematic variation, song structure (verse-chorus-bridge), counterpoint, and harmony.", "low"),
            ("songwriting", "Lyrical rhyme schemes, prosody, melodic hooks, emotional resonance, and collaborative songwriting.", "low"),
            ("arrangement", "Instrument voicing, frequency spacing, dynamic buildups, transitions, and ensemble arrangement.", "low"),
            ("orchestration", "Orchestral instrument ranges, timbral blending, woodwind/brass/string section balance, and score engraving.", "low"),
            ("vocal-production", "Vocal comping, manual pitch correction (Melodyne), formant tuning, de-essing, and vocal harmonies.", "low"),
            ("recording", "Microphone polar patterns, mic placement on drums/acoustic instruments, pre-amp saturation, and impedance.", "low"),
            ("mixing", "Gain staging, EQ carving, dynamic range compression (VCA, Opto, FET), stereo imaging, and reverb sends.", "low"),
            ("mastering", "Linear phase EQ, multi-band compression, stereo widening, true peak limiting, and LUFS loudness targets.", "low"),
            ("sound-design", "Foley creation, cinematic impacts, risers, atmospheric drones, and sound synthesis for media.", "low"),
            ("synthesis", "Subtractive, additive, FM (frequency modulation), wavetable, and granular synthesis parameters.", "low"),
            ("sampling", "Sample chopping, zero-crossing editing, loop creation, time-stretching, and MIDI sampler mapping.", "low"),
            ("live-sound", "Front of House (FOH) mixing, monitor mixes, feedback elimination, stage snakes, and PA system tuning.", "low"),
            ("music-production", "Digital Audio Workstation (DAW) workflows (Ableton, Logic, Pro Tools), beat making, and creative direction.", "low"),
            ("music-publishing", "Mechanical royalties, performance rights organizations (ASCAP, BMI), and sheet music publishing.", "low"),
            ("music-distribution", "Digital service provider (DSP) distribution, ISRC and UPC codes, release schedules, and playlist pitching.", "low"),
            ("music-business", "Artist management agreements, 360 deals, tour budgeting, merchandise revenue, and contract audits.", "low"),
            ("music-licensing", "Sync licensing for film/TV/commercials, master vs publishing rights clearance, and cue sheets.", "low"),
            ("music-education", "Pedagogical frameworks for instrumental instruction, ear training, sight reading, and rhythm drills.", "low"),
        ]
    },
    "photography": {
        "title": "Professional Photography & Digital Imaging",
        "skills": [
            ("portrait", "Posing direction, catchlights, depth of field (bokeh), focal length selection (85mm/105mm), and rapport.", "low"),
            ("landscape", "Golden/blue hour timing, hyperfocal distance calculations, ND filters, leading lines, and panoramas.", "low"),
            ("street", "Decisive moment capture, zone focusing, unobtrusive composition, and street photography ethics.", "low"),
            ("wildlife", "Telephoto lens handling (400mm+), fast shutter speeds, continuous autofocus tracking, and animal behavior.", "low"),
            ("sports", "Action freeze techniques, burst mode buffering, predictive tracking, and capturing peak athletic motion.", "low"),
            ("product", "Seamless background cycloramas, table-top lighting, polarization to eliminate glare, and focus stacking.", "low"),
            ("architecture", "Perspective control tilt-shift lenses, vertical alignment, architectural twilight shooting, and bracketed HDR.", "low"),
            ("real-estate", "Interior wide-angle composition (16-24mm), window pull flash blends, ambient light balance, and staging.", "low"),
            ("fashion", "Editorial lighting concepts, high-fashion posing, working with stylists, and garment detail rendering.", "low"),
            ("food", "Food styling, artificial steam/condensation, backlight texture enhancement, and macro food presentation.", "low"),
            ("macro", "1:1 reproduction ratios, extension tubes, micro-contrast, focus stacking software, and ring flashes.", "low"),
            ("astrophotography", "Rule of 500 for star trails, tracking equatorial mounts, deep-sky stacking, and dark frame subtraction.", "low"),
            ("drone-photography", "FAA Part 107 compliance, top-down grid mapping, composition from altitude, and aerial gimbal control.", "medium"),
            ("studio-lighting", "Strobe lighting setups: key, fill, rim, and hair lights, softboxes, beauty dishes, and flash meters.", "low"),
            ("flash", "On-camera bounce flash, high-speed sync (HSS), first/second curtain sync, and off-camera speedlights.", "low"),
            ("color-management", "Color calibration pucks, ICC profiles, Adobe RGB vs sRGB color spaces, and calibrated monitor setup.", "low"),
            ("retouching", "Frequency separation, dodge and burn, skin smoothing, dust removal, and non-destructive Photoshop layers.", "low"),
            ("photo-organization", "Lightroom catalog management, keyword tagging, metadata schemas (EXIF/IPTC), and star rating filters.", "low"),
            ("photo-archiving", "3-2-1 backup strategy for RAW files, redundant RAID arrays, and long-term digital negative preservation.", "low"),
        ]
    },
    "skilled-trades": {
        "title": "Skilled Trades, Construction Crafts & Facilities Maintenance",
        "skills": [
            ("electrical", "Residential and commercial wiring: conduit bending, circuit breaker panels, GFCI circuits, and NEC compliance.", "medium"),
            ("plumbing", "DWV drainage, PEX and copper water supply lines, pipe sweating, water heaters, and fixture installation.", "medium"),
            ("carpentry", "Framing (studs, joists, rafters), finish carpentry (trim, crown molding), cabinet installation, and squaring.", "low"),
            ("masonry", "Mortar mixing ratios, bricklaying bond patterns, concrete block (CMU) walls, rebar grouting, and tuckpointing.", "low"),
            ("welding", "MIG, TIG, Stick welding parameters, shielding gases, joint preparation, weld penetration, and weld inspection.", "medium"),
            ("machining", "Manual and CNC lathe/mill operation, cutting speeds, drill bit sharpening, dial indicators, and tolerances.", "low"),
            ("hvac", "Refrigerant recovery, vacuum pump evacuation, manifold gauges, compressor troubleshooting, and duct static pressure.", "medium"),
            ("refrigeration", "Commercial walk-in coolers, thermostatic expansion valves (TXV), defrost cycles, and subcooling calculations.", "medium"),
            ("roofing", "Asphalt shingle installation, flashing details, underlayment, drip edges, flat roof membranes (TPO/EPDM).", "medium"),
            ("painting", "Surface prep (sanding, scraping), primer selection, airless paint sprayer operation, and cutting in clean lines.", "low"),
            ("drywall", "Hanging drywall sheets, tape and joint compound feathering (Levels 1-5 finish), and patching drywall.", "low"),
            ("flooring", "Subfloor leveling, hardwood installation, luxury vinyl plank (LVP), ceramic tile laying, and grout sealing.", "low"),
            ("glazing", "Window glass replacement, storefront glazing, insulated glass units (IGU), caulking, and glazing putty.", "low"),
            ("woodworking", "Joinery techniques (dovetails, mortise and tenon), wood turning, planing, table saw safety, and finishes.", "low"),
            ("metal-fabrication", "Sheet metal shearing, press brake bending, plasma cutting, deburring, and structural steel assembly.", "medium"),
            ("appliance-repair", "Diagnostic fault codes, multimeters testing heating elements, pump motors, and compressor relays.", "low"),
            ("automotive-repair", "Engine diagnostics (OBD-II), brake rotor/pad replacement, alternator testing, and suspension repair.", "medium"),
            ("motorcycle-repair", "Carburetor synchronization, chain tension adjustment, motorcycle valve clearance, and fork seal repair.", "medium"),
            ("bicycle-repair", "Derailleur indexing, wheel truing, hydraulic disc brake bleeding, bottom bracket replacement, and tuning.", "low"),
            ("solar-installation", "Photovoltaic panel mounting, micro-inverter wiring, string sizing, roof penetration flashing, and rapid shutdown.", "medium"),
            ("telecommunications-installation", "Structured cabling (Cat6/Fiber), punchdown blocks, optical fiber splicing, and OTDR testing.", "low"),
            ("equipment-maintenance", "Preventive maintenance checklists, lubrication schedules, hydraulic fluid checks, and belt tensioning.", "low"),
        ]
    },
    "agriculture": {
        "title": "Agricultural Sciences, Agronomy & Farming",
        "skills": [
            ("agronomy", "Crop rotation schedules, soil fertility management, planting density, and tillage practices.", "low"),
            ("soil-science", "Soil texture analysis, soil organic matter, pH neutralization with lime, and micronutrient balancing.", "low"),
            ("crop-science", "Seed germination, phenological growth stages, weed management, and yield component analysis.", "low"),
            ("horticulture", "Fruit and vegetable cultivation, grafting, pruning techniques, propagation, and nursery management.", "low"),
            ("irrigation", "Drip irrigation design, center pivot operation, evapotranspiration (ET) calculations, and soil moisture sensors.", "low"),
            ("precision-agriculture", "Variable rate application (VRA), GPS autosteer, yield monitor data mapping, and spatial soil sampling.", "low"),
            ("remote-sensing-agriculture", "Drone NDVI imagery for crop stress, canopy vigor assessment, and targeted spraying zones.", "low"),
            ("farm-robotics", "Autonomous weeding robots, automated harvesting machines, robotic milking parlors, and autonomous tractors.", "low"),
            ("greenhouse-management", "Climate computer control (temperature, humidity, CO2), supplemental grow lighting, and ventilation.", "low"),
            ("hydroponics", "Nutrient Film Technique (NFT), deep water culture (DWC), EC/pH nutrient solution monitoring, and clean water.", "low"),
            ("aquaponics", "Recirculating aquaculture coupled with hydroponic biofilters, nitrogen conversion, and fish feed ratios.", "low"),
            ("livestock", "Beef and swine management: herd health protocols, stocking density, animal welfare, and feedlot nutrition.", "low"),
            ("dairy", "Dairy cow lactation cycles, somatic cell count (SCC) reduction, automated milking systems, and milk quality.", "low"),
            ("poultry", "Broiler and layer flock management, biosecurity protocols, ventilation curves, and feed conversion ratios.", "low"),
            ("veterinary-agriculture", "Livestock vaccination schedules, herd health surveillance, parasite management, and biosecurity.", "medium"),
            ("agricultural-economics", "Commodity futures hedging, farm enterprise budgeting, cost per bushel calculation, and price elasticity.", "low"),
            ("farm-finance", "Agri-lending cash flow projections, equipment leasing, USDA FSA programs, and land valuation.", "low"),
            ("agricultural-insurance", "Multi-Peril Crop Insurance (MPCI), revenue protection policies, and crop loss assessment.", "low"),
            ("food-processing", "Post-harvest handling, cold chain logistics, grain storage drying, and food safety standards (HACCP).", "low"),
            ("agricultural-supply-chain", "Grain elevator logistics, bulk transport, seed distribution networks, and fertilizer procurement.", "low"),
        ]
    },
    "mining": {
        "title": "Mining Engineering & Mineral Extraction",
        "skills": [
            ("exploration", "Greenfield exploration, geochemical anomaly mapping, trenching, target generation, and geological models.", "low"),
            ("geology", "Ore deposit geology (porphyry, epithermal, VMS), structural controls, alteration mapping, and lithology.", "low"),
            ("geophysics", "Induced Polarization (IP), magnetics, electromagnetic surveys, and radiometric prospecting for ores.", "low"),
            ("drilling", "Diamond core drilling, reverse circulation (RC), core logging, sample recovery, and deviation surveys.", "medium"),
            ("blasting", "Explosives selection (ANFO), blast pattern geometry (burden, spacing), timing delays, and vibration limits.", "medium"),
            ("open-pit-mining", "Pit slope stability, pushback design, bench height, stripping ratio, and haul truck fleet dispatch.", "medium"),
            ("underground-mining", "Underground stoping methods (sublevel, cut-and-fill, block caving), mine ventilation, and ground support.", "medium"),
            ("mine-planning", "Long-term life of mine (LOM) planning, short-term production sequencing, and ultimate pit limit optimization.", "low"),
            ("mine-scheduling", "Mine production scheduling, equipment utilization, blend constraints, and stockpile management.", "low"),
            ("resource-estimation", "Exploratory data analysis, 3D block modeling, variography, and ordinary kriging interpolation.", "low"),
            ("reserve-estimation", "Applying cut-off grades, economic modifying factors, and reporting reserves under JORC / NI 43-101.", "low"),
            ("mineral-processing", "Comminution circuits, ore liberation analysis, beneficiation flowsheets, and mass balancing.", "low"),
            ("flotation", "Froth flotation cells, collector/frother chemistry, pulp density, and concentrate grade-recovery curves.", "low"),
            ("crushing", "Jaw, cone, and gyratory crusher operations, closed circuit screens, and circulating load calculations.", "low"),
            ("milling", "SAG and ball mill grinding circuits, bond work index (BWi), grinding media charge, and cyclone classification.", "low"),
            ("tailings", "Tailings storage facility (TSF) engineering, dry stacking, dam stability monitoring, and acid rock drainage.", "medium"),
            ("mine-safety", "MSHA compliance, ground control plans, emergency refuge chambers, and mine rescue protocols.", "medium"),
            ("mine-reclamation", "Environmental remediation, land contouring, topsoil replacement, revegetation, and mine closure bonds.", "low"),
            ("mining-economics", "Cash cost per ounce/tonne (AISC), net smelter return (NSR) royalties, discount cash flow valuation.", "low"),
            ("mining-environmental-impact", "Environmental impact statements (EIS), water management, dust mitigation, and biodiversity offsets.", "low"),
        ]
    },
    "marine": {
        "title": "Marine Engineering, Naval Architecture & Oceanography",
        "skills": [
            ("naval-architecture", "Ship hydrostatic curves, intact and damage stability, cross curves of stability, and hull lines fairing.", "low"),
            ("marine-engineering", "Marine diesel propulsion, shaft alignment, auxiliary boilers, seawater cooling, and bilge separators.", "medium"),
            ("ship-design", "General arrangement drafting, cargo hold sizing, structural midship section scantlings, and class rules.", "low"),
            ("shipbuilding", "Block assembly methods, shipyard crane logistics, welding distortion control, and sea trial protocols.", "medium"),
            ("maritime-navigation", "COLREGS rules of the road, passage planning, ECDIS electronic charting, radar plotting (ARPA).", "medium"),
            ("maritime-logistics", "Container liner schedules, charter party agreements (voyage/time), stowage planning, and demurrage.", "low"),
            ("port-operations", "Berth allocation, ship-to-shore gantry crane productivity, container yard stacking, and pilotage.", "low"),
            ("offshore-engineering", "Floating production storage (FPSO), jacket platforms, catenary mooring lines, and metocean design criteria.", "medium"),
            ("subsea-engineering", "Subsea trees, flowlines, umbilical cables, ROV intervention tooling, and subsea manifold systems.", "medium"),
            ("ocean-engineering", "Ocean wave energy converter modeling, coastal seawall dynamics, and underwater acoustic telemetry.", "low"),
            ("marine-safety", "SOLAS and MARPOL international conventions, life-saving appliances (LSA), firefighting appliances (FFA).", "medium"),
            ("maritime-law", "Admiralty jurisdiction, bill of lading disputes, maritime liens, general average, and salvage claims.", "low"),
            ("marine-surveying", "Vessel condition surveys, bunker surveys, draft surveys, non-destructive testing of hulls, and class surveys.", "low"),
            ("marine-environment", "Ballast water treatment systems (BWTS), hull biofouling prevention, and greenhouse gas EEXI/CII metrics.", "low"),
        ]
    },
    "aerospace": {
        "title": "Aerospace, Aviation & Space Systems",
        "skills": [
            ("aircraft-systems", "Hydraulic flight controls, pneumatic bleed air, environmental control systems, and fuel distribution.", "medium"),
            ("avionics", "ARINC 429/664 data buses, flight management systems (FMS), primary flight displays, and navigation transponders.", "low"),
            ("flight-operations", "Standard operating procedures (SOP), weight and balance calculations, dispatch releases, and NOTAMs.", "medium"),
            ("airline-operations", "Crew scheduling pairing algorithms, fleet routing, ground handling turnaround, and irregular operations.", "low"),
            ("airport-operations", "Runway friction testing, taxiway lighting (FAA/ICAO), gate assignment, and airport baggage handling.", "low"),
            ("air-traffic-management", "Air traffic control separation minimums, ADS-B surveillance, arrival/departure sequencing (AMAN/DMAN).", "medium"),
            ("flight-safety", "Safety Management Systems (SMS), flight data monitoring (FDM), bird strike mitigation, and incident reporting.", "medium"),
            ("aviation-maintenance", "Part 145 repair station procedures, Airworthiness Directives (AD), continuous airworthiness maintenance.", "medium"),
            ("aviation-regulation", "FAA FAR Part 25/121/135 rules, EASA airworthiness regulations, type certification, and bilateral agreements.", "low"),
            ("orbital-mechanics", "Keplerian orbital elements, Hohmann transfer orbits, delta-v budgets, Lagrange points, and perturbation theory.", "low"),
            ("spacecraft", "Satellite bus architecture, structural frames, thermal louvers and heat pipes, radiation hardening.", "low"),
            ("satellites", "Payload design (communications, optical, SAR), link budgets, power budgets, and solar array sizing.", "low"),
            ("propulsion", "Liquid rocket engines (turbopumps, combustion chambers), solid rocket motors, and electric propulsion (Hall thrusters).", "medium"),
            ("attitude-control", "Attitude Determination and Control Systems (ADCS): reaction wheels, magnetorquers, star trackers, and Kalman filters.", "low"),
            ("mission-design", "Launch window calculation, planetary trajectory design, ground track coverage, and end-of-life deorbiting.", "low"),
            ("ground-stations", "Antenna tracking systems, telecommand uplink, telemetry downlink, and mission control center software.", "low"),
            ("space-communications", "Consultative Committee for Space Data Systems (CCSDS) protocols, Doppler shift compensation, and DSN.", "low"),
            ("earth-observation", "Radiometric calibration, optical and SAR sensor geometries, ground sample distance (GSD), and swaths.", "low"),
            ("space-operations", "Launch countdown operations, LEOP (Launch and Early Orbit Phase), orbit raising maneuvers, and station-keeping.", "medium"),
        ]
    }
}


def create_skill_markdown(slug: str, title_text: str, desc: str, cat: str, risk: str) -> str:
    display_title = title_text.replace("-", " ").title()
    content = f"""---
name: {slug}
description: "{desc}"
category: {cat}
version: 1.0.0
disable-model-invocation: false
risk: {risk}
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/{cat}/{slug}/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# {display_title}

## Overview & Domain Scope
`{slug}` provides operational playbooks, validated heuristics, and expert methodologies in **{cat.replace('-', ' ').title()}**.
{desc}

## Core Capabilities & Operational Playbooks
- Execute structured analysis and implementation workflows adhering to industry standards.
- Formulate quantitative models, specifications, and verified domain outputs.
- Verify constraints, edge cases, error conditions, and lifecycle safety requirements.
- Produce documented, reproducible artifacts compatible with multi-agent orchestration.

## Standards & Reference Frameworks
- Conforms to foundational domain standards, international guidelines, and best practices.
- Implements rigorous validation gates before finalizing technical recommendations.
- Ensures cross-system interoperability across AI agent platforms (Antigravity, Claude Code, Cursor, Codex).

## Verification & Quality Gates
1. Baseline Verification: Confirm all required inputs, parameters, and contextual boundaries are established.
2. Methodological Execution: Apply domain-specific procedures with verifiable intermediate checks.
3. Output Validation: Review calculations, assertions, safety guardrails, and compliance requirements.
"""
    return content


def synthesize_remaining_domains():
    print("=" * 60)
    print("   REMAINING DOMAINS SYNTHESIS ENGINE (35 DOMAINS)")
    print("=" * 60)

    total_created = 0
    total_existing = 0

    for cat, data in REMAINING_DOMAINS.items():
        cat_dir = AWESOME_DIR / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        print(f"Synthesizing domain: {cat} ({data['title']})...")

        for slug, desc, risk in data["skills"]:
            skill_dir = cat_dir / slug
            skill_md = skill_dir / "SKILL.md"

            if skill_md.exists():
                total_existing += 1
                continue

            skill_dir.mkdir(parents=True, exist_ok=True)
            content = create_skill_markdown(slug, slug, desc, cat, risk)
            skill_md.write_text(content, encoding="utf-8")
            total_created += 1

    print("\n" + "=" * 60)
    print("                 SYNTHESIS SUMMARY")
    print("=" * 60)
    print(f"Domains Processed:       {len(REMAINING_DOMAINS)}")
    print(f"New Skills Synthesized:  {total_created}")
    print(f"Existing Maintained:     {total_existing}")
    print("=" * 60)


if __name__ == "__main__":
    synthesize_remaining_domains()
