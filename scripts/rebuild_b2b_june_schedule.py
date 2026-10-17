#!/usr/bin/env python3
"""
Rebuilds B2B campaign articles: ~5 min read each, filenames from June 2027 onward.
Copies hero PNGs to new dated names, removes legacy article HTML + old PNGs.
"""
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ART_DIR = REPO / "docs" / "b2b" / "article"
IMG_DIR = ART_DIR / "assets" / "img"

# (article_num, new_date, old_img_date_prefix, title, search_keywords, data_subject)
SPECS: list[tuple[int, str, str, str, str, str]] = [
    (1, "2027_06_02", "2026_04_13", "The hidden risk of cloud-only systems",
     "cloud dependency continuity retail", "continuity architecture"),
    (2, "2027_06_09", "2026_04_20", "What really happens when the internet goes down in a business",
     "outage isp branch operations", "continuity"),
    (3, "2027_06_16", "2026_04_27", "Why most POS and ERP systems are not built for failure",
     "pos erp failure design retail", "architecture continuity"),
    (4, "2027_06_23", "2026_05_04", "Downtime is not a bug — it is a design decision",
     "downtime sla architecture strategy", "architecture strategy"),
    (5, "2027_06_30", "2026_05_11", "What is offline-first architecture and why it matters",
     "offline first sync queue", "offline-first architecture"),
    (6, "2027_07_07", "2026_05_18", "Local-first vs cloud-first: a practical comparison",
     "local first cloud comparison", "offline-first architecture"),
    (7, "2027_07_14", "2026_05_25", "Designing systems that survive disconnection",
     "disconnection sync conflict retail", "continuity architecture"),
    (8, "2027_07_21", "2026_06_01", "Edge computing for real businesses",
     "edge latency branch iot", "edge architecture"),
    (9, "2027_07_28", "2026_06_08", "How we build systems that never stop",
     "always on continuity pdv hub", "continuity architecture"),
    (10, "2027_08_04", "2026_06_15", "Where offline-first systems make the biggest impact",
     "impact inventory field service", "offline-first strategy"),
    (11, "2027_08_11", "2026_06_22", "Partnering with IT firms: how we work together",
     "partner integrator delivery model", "partnership strategy"),
    (12, "2027_08_18", "2026_06_29", "Why resilience is becoming a competitive advantage",
     "competitive advantage trust b2b", "strategy continuity"),
]

# Section bodies: short paragraphs (~5 min total read at ~200 wpm English business prose)
BODIES: dict[int, dict[str, list[str]]] = {}


def register(
    n: int,
    hook: list[str],
    problem: list[str],
    explain: list[str],
    solution: list[str],
    application: list[str],
    closing: list[str],
) -> None:
    BODIES[n] = {
        "Hook": hook,
        "Real Problem": problem,
        "Explanation": explain,
        "Solution": solution,
        "Application": application,
        "Closing": closing,
    }


register(
    1,
    [
        "Cloud-only workflows look efficient until the first serious outage. Then sales, approvals, and reporting stall at the same time.",
        "This article is a five-minute read for leaders who need plain language, not slides: why dependency on distant services is a continuity risk, and what to do first.",
    ],
    [
        "When connectivity drops, the visible failure is “the system is down.” The hidden failure is improvised spreadsheets, duplicate entries, and delayed decisions.",
        "Retail and distributed teams feel this first: the branch keeps serving people, but digital process stops. That mismatch creates chaos cost and audit stress.",
    ],
    [
        "The root issue is an assumption that the network is a constant. Field reality includes latency spikes, ISP maintenance, and human mistakes under pressure.",
        "Resilient design separates what must execute locally from what can wait for synchronization, without giving up governance.",
    ],
    [
        "Start with a one-page map: which steps must never stop, which can pause, and which can degrade without harming customers.",
        "Add local execution or queued operations for the “never stop” steps, with clear conflict rules when the network returns. Train the first ten minutes of outage response in plain language.",
    ],
    [
        "In Cara Core patterns (for example PDV and Hub contexts), continuity is treated as a product requirement: predictable behavior under stress, not only uptime charts.",
        "Partners win when reliability is observable: fewer emergency calls, cleaner records after incidents, and renewals based on evidence.",
    ],
    [
        "Pick one critical workflow this week, remove a single hidden cloud-only dependency, and measure the outcome. Small wins compound.",
        "If you want a practical collaboration path, bring your continuity map—we are open to integrator-friendly delivery with clear responsibilities.",
    ],
)

register(
    2,
    [
        "Internet outages are not rare edge cases. They are normal infrastructure weather—and businesses still behave surprised every time.",
        "Here is what actually happens inside teams during the first hour, and why “we will fix the line” is not a complete response.",
    ],
    [
        "Queues grow, payments stall, and managers ask for numbers nobody can trust because half the data is offline and half is in the cloud.",
        "The organization optimizes for survival, not for process integrity. That is how technical debt becomes operational debt overnight.",
    ],
    [
        "Outages expose coupling: every critical action that requires a round trip to a distant service is a single point of failure.",
        "Good continuity preserves customer-facing motion with local or queued execution, then reconciles with discipline instead of heroics.",
    ],
    [
        "Publish a short playbook: who decides, what sells without connectivity, what waits, and how records reconcile when service returns.",
        "Run a thirty-minute tabletop exercise quarterly. The goal is muscle memory, not documentation weight.",
    ],
    [
        "Branches, desks, and finance teams stop improvising when the routine is rehearsed. That reduces fraud risk and customer-visible inconsistency.",
        "Partners can sell calmer operations because the story is measurable, not aspirational.",
    ],
    [
        "Schedule one drill before peak season. Afterward, fix the top friction you discovered—do not file it under “later.”",
        "Cara Core aligns editorial and engineering around execution reality: less noise, more routines that survive bad days.",
    ],
)

register(
    3,
    [
        "POS and ERP systems are sold as “always available,” but many are architected for happy-path connectivity, not for branch reality.",
        "This note explains the failure gap in practical terms for buyers and integrators.",
    ],
    [
        "Failure is not only server downtime. It is partial degradation: slow auth, flaky printers, intermittent timeouts, and silent retries that corrupt totals.",
        "Most vendors report availability of components, not end-to-end transaction success under weak networks.",
    ],
    [
        "Retail-grade reliability requires deterministic local behavior, explicit sync boundaries, and operator-visible states—not optimistic UI assumptions.",
        "When failure modes are unnamed, teams invent unsafe workarounds that look productive in the moment.",
    ],
    [
        "Ask vendors for offline behavior in writing: what sells, what queues, what conflicts, and how reconciliation is audited.",
        "Pilot in one stressed branch, not only in headquarters Wi-Fi. Measure transaction completion, not ping time.",
    ],
    [
        "Strong POS discipline improves inventory truth, cash control, and partner trust. ERP alignment then becomes simpler because facts match reality.",
        "Cara Core product thinking treats continuity as part of product quality, not as an add-on module.",
    ],
    [
        "If your roadmap ignores failure design, you are planning for a demo environment, not for customers on Tuesday afternoon.",
        "Start with one honest failure map; it pays back faster than another feature checklist.",
    ],
)

register(
    4,
    [
        "Downtime is often treated as an accident. In mature systems, availability is a consequence of explicit design choices—including acceptable degradation.",
        "This article reframes downtime as a policy signal, not only as an incident metric.",
    ],
    [
        "If every feature requires live services, downtime becomes binary: all-or-nothing. That creates brittle operations and expensive emergency culture.",
        "Leaders see SLA charts, but customers see inconsistent service and staff stress.",
    ],
    [
        "Resilience budgets time and architecture for partial operation: what continues, what pauses, and what operators can see while degraded.",
        "That requires product discipline: fewer hidden dependencies and clearer state machines in critical flows.",
    ],
    [
        "Define “good enough service” states for peak hours. Implement them as first-class modes, not as undocumented exceptions.",
        "Measure recovery quality: record consistency and reconciliation time, not only minutes offline.",
    ],
    [
        "When degradation is designed, teams stop improvising dangerous shortcuts. Finance and compliance get calmer narratives after incidents.",
        "Partners can differentiate with honest engineering stories backed by metrics.",
    ],
    [
        "Pick one customer journey and design its degraded mode on purpose. That single exercise usually reveals three hidden dependencies.",
        "Cara Core publishes in Sala tone: strategy must survive contact with reality.",
    ],
)

register(
    5,
    [
        "Offline-first means your default execution path does not assume perfect connectivity. Sync becomes a scheduled responsibility, not a prayer.",
        "Five minutes, plain English: why it matters for B2B buyers who operate outside headquarters.",
    ],
    [
        "Without offline-first patterns, teams oscillate between “cannot work” and “working twice” after outages—neither is acceptable at scale.",
        "The cost shows up as shrinkage risk, angry customers, and delayed closes.",
    ],
    [
        "Offline-first is not “no cloud.” It is “cloud is not in the critical path for every keystroke.” Queues, idempotency, and operator clarity are the toolkit.",
        "Local-first is a sibling idea: authority and truth live where work happens, then synchronize.",
    ],
    [
        "Prototype one flow with explicit queues and conflict rules. Validate with real devices on a throttled network profile.",
        "Document operator-visible states so support can diagnose without escalating to engineering every time.",
    ],
    [
        "Retail and field operations gain predictable throughput. IT partners reduce weekend war rooms after storms or fiber cuts.",
        "Cara Core messaging stays consistent: continuity is hygiene, not heroics.",
    ],
    [
        "Choose one pilot workflow, ship it, measure reconciliation errors weekly for a month, then expand.",
        "If you want a partner-ready narrative, anchor claims in those measured outcomes.",
    ],
)

register(
    6,
    [
        "Cloud-first optimizes for centralized control and fast iteration. Local-first optimizes for autonomy and predictable execution under stress.",
        "This comparison is practical, not ideological: where each model wins in real B2B delivery.",
    ],
    [
        "Pure cloud-first fails when latency, compliance, or outages block revenue moments. Pure local-first can drift without governance if sync is weak.",
        "Most healthy systems are hybrid with a clear “source of truth” strategy per entity.",
    ],
    [
        "Decide per data type: what must be local authoritative, what can be cloud authoritative, and what must be mergeable with rules.",
        "If you cannot explain merge rules on one page, you will pay for that ambiguity in incidents.",
    ],
    [
        "Run a decision workshop with business and engineering: ten entity types, ten decisions, done. Then align the roadmap to those decisions.",
        "Avoid “we will sync somehow” as an architecture statement.",
    ],
    [
        "Hybrid clarity reduces vendor finger-pointing and speeds audits because ownership is explicit.",
        "Partners can propose phased migration paths that respect revenue risk windows.",
    ],
    [
        "Pick one entity type this month and write its truth rules. That document becomes your compass for the next quarter.",
        "Cara Core favors readable engineering that integrators can implement without guessing intent.",
    ],
)

register(
    7,
    [
        "Disconnection is not only “no internet.” It is intermittent loss, captive portals, DNS issues, and saturated uplinks during peak hours.",
        "Systems that survive disconnection are designed for partial truth temporarily, then converge cleanly.",
    ],
    [
        "Teams without a disconnection strategy revert to paper, shadow spreadsheets, and verbal promises—then spend weeks reconciling.",
        "That is expensive, risky, and demoralizing for frontline staff.",
    ],
    [
        "Survival design uses bounded queues, idempotent operations, and operator prompts that remain truthful when offline.",
        "Synchronization is a controlled process with measurable backlog, not a silent background hope.",
    ],
    [
        "Define maximum queue depth and operator actions when limits approach. Add drills that include partial connectivity, not only full blackout.",
        "Test conflict scenarios with finance before production, not after customers complain.",
    ],
    [
        "Retail networks gain calmer peaks and fewer “unknown totals” moments. Partners ship fewer emergency patches.",
        "Cara Core ties narrative to evidence: drills, metrics, and post-incident reviews that improve the next quarter.",
    ],
    [
        "Run one disconnection drill focused on reconciliation quality, not only on “did the UI load.”",
        "If you want help framing drills for partner delivery, start with your riskiest branch profile.",
    ],
)

register(
    8,
    [
        "Edge computing moves selected processing closer to where events happen: stores, warehouses, clinics, and field teams.",
        "This article grounds edge in business outcomes latency, autonomy, and controlled bandwidth—not buzzwords.",
    ],
    [
        "Without edge discipline, you get duplicated logic, security sprawl, and “snowflake” devices nobody can patch consistently.",
        "The edge is not a free performance button; it is an operations responsibility.",
    ],
    [
        "Good edge patterns define what runs locally, how updates roll out, and how telemetry returns without drowning uplinks.",
        "Security and observability must be designed for distributed failure, not copied from a single data center checklist.",
    ],
    [
        "Start with one high-churn workflow where latency hurts revenue. Measure before/after with the same devices and hours.",
        "Centralize policy, decentralize execution; do not decentralize policy accidentally.",
    ],
    [
        "Real businesses see fewer timeouts during peaks and clearer accountability when something misbehaves on site.",
        "Partners can propose phased edge scope with measurable KPIs instead of big-bang rollouts.",
    ],
    [
        "Pick one workflow, one edge boundary, one month pilot. Review with finance and security on week four.",
        "Cara Core prefers honest scope: edge helps when the problem is truly local.",
    ],
)

register(
    9,
    [
        "“Never stop” is a product claim only if you define what continues, what queues, and what operators see under stress.",
        "Here is how we think about always-on execution without magical thinking.",
    ],
    [
        "Organizations confuse high availability of servers with continuity of business process. Those are related, not identical.",
        "Process continuity needs human-readable states and safe partial progress.",
    ],
    [
        "We bias toward local execution for revenue-critical steps, deterministic retries, and transparent backlog metrics for managers.",
        "Reliability is engineered as a loop: observe, tighten, drill again—editorial and engineering stay aligned on what “good” means.",
    ],
    [
        "Ship continuity playbooks with owners, not anonymous wiki pages. Measure drill outcomes and reconciliation defects monthly.",
        "Treat incident reviews as product inputs, not as blame ceremonies.",
    ],
    [
        "Customers experience fewer “come back later” moments. Internal teams argue less about whose number is correct.",
        "Partners inherit clearer acceptance criteria and fewer surprise gaps at go-live.",
    ],
    [
        "Commit to one measurable continuity KPI next quarter—for example time-to-safe-sale under degraded mode.",
        "Cara Core stands for execution language that integrators can implement and clients can verify.",
    ],
)

register(
    10,
    [
        "Offline-first pays off fastest where work happens away from stable headquarters networks: inventory walks, pop-up sales, rural branches, and traveling technicians.",
        "This article names the highest-impact zones so roadmap prioritization is easier.",
    ],
    [
        "If you optimize only HQ, you optimize the wrong bottleneck when most revenue or risk is distributed.",
        "Impact mapping prevents “platform for everything” waste.",
    ],
    [
        "Evaluate impact by revenue exposure, compliance sensitivity, rework cost after outages, and frequency of weak connectivity.",
        "Weight operational pain from frontline managers higher than convenience for central reporting.",
    ],
    [
        "Rank ten candidate workflows, pilot the top two, and stop expanding until reconciliation metrics stabilize.",
        "Share results with partners so scope stays disciplined.",
    ],
    [
        "Focused offline-first investment reduces chaos cost where it hurts most, without boiling the ocean.",
        "Cara Core uses the same prioritization language in editorial planning: fewer promises, clearer delivery.",
    ],
    [
        "Pick your top distributed workflow and score it with the four impact factors above. If it fails two or more, it belongs in the pilot lane.",
        "We are open to joint assessments with IT firms that want evidence-backed roadmaps.",
    ],
)

register(
    11,
    [
        "IT firms need predictable interfaces: responsibilities, environments, acceptance tests, and escalation paths.",
        "This article summarizes how Cara Core prefers to collaborate with integrators in B2B contexts.",
    ],
    [
        "Partnership fails when scope is fuzzy, success is subjective, and production surprises become relationship debt.",
        "Clarity is a respect signal for both sides.",
    ],
    [
        "We favor written boundaries for environments, security expectations, release cadence, and who owns which monitoring signals.",
        "Documentation is kept operational: checklists, test evidence, and change logs that survive staff rotation.",
    ],
    [
        "Start engagements with a shared risk register and a pilot milestone that proves integration reality, not slide reality.",
        "Use joint drills for continuity scenarios that matter to the end client.",
    ],
    [
        "Partners ship faster when acceptance criteria map to measurable business moments, not only to technical endpoints.",
        "Customers feel fewer gaps between sales promise and field behavior.",
    ],
    [
        "If you are an integrator, bring your standard delivery pack—we will align ours. If you are a client, ask both sides for the same evidence format.",
        "Cara Core grows with partners who value execution receipts, not narrative alone.",
    ],
)

register(
    12,
    [
        "Resilience is moving from IT hygiene to buying criteria: clients compare how vendors behave under stress, not only feature lists.",
        "This closing piece ties continuity discipline to competitive positioning in B2B export markets.",
    ],
    [
        "Buyers fear hidden fragility more than missing features. A clean incident story with metrics beats a perfect demo that cracks in week two.",
        "Trust compounds when behavior is consistent across quarters.",
    ],
    [
        "Competitive advantage shows up as fewer discounts given to compensate for outages, faster renewals, and stronger references.",
        "It also shows up internally: less firefighting means more roadmap capacity.",
    ],
    [
        "Invest in evidence: drills, reconciliation metrics, and public-facing reliability notes that sales can use ethically.",
        "Align marketing claims with engineering test boundaries—oversell creates brittle trust.",
    ],
    [
        "Cara Core treats resilience messaging as accountable: what we claim, we can show in partner-friendly artifacts.",
        "That discipline supports premium positioning without gimmicks.",
    ],
    [
        "Pick one claim your sales team makes today and attach a single measurable proof artifact to it this month.",
        "If you want to compare notes on partner-ready evidence packs, the B2B hub is the right entry point.",
    ],
)

# Third paragraph per section (~5 min total at ~200 wpm after merge)
_DEPTH: dict[int, tuple[str, str, str, str, str, str]] = {
    1: (
        "Export-facing teams should treat connectivity like weather: plan for seasonal peaks, construction work, and regional instability, not only for total blackout.",
        "Finance often discovers the true cost months later, when audits uncover inconsistent stock counts, duplicated invoices, or approvals that happened outside the controlled workflow.",
        "A useful mental model is tiers: Tier A must run locally with audit trail; Tier B can queue safely; Tier C can pause without customer harm. Most organizations never classify work this plainly.",
        "Operationalize the map with owners: who validates queued transactions, who signs off reconciliation, and which monitoring signals prove recovery quality—not only that servers are green again.",
        "Cara Core documentation in Sala de Operacoes tone favors checklists and drills because resilience decays when it lives only in architecture diagrams.",
        "Send one continuity improvement to your integration partner this month; alignment beats perfect theory when calendars are tight.",
    ),
    2: (
        "The first hour is where habits form: if people learn that outages mean chaos, they will optimize for personal survival instead of process integrity.",
        "Customer-facing staff often choose the fastest workaround—personal phones, paper receipts, manual discounts—because KPIs still demand throughput during the outage window.",
        "Continuity architecture should assume partial connectivity: flaky DNS, captive portals, and asymmetric packet loss are common in retail Wi-Fi and mobile failover paths.",
        "Add explicit decision rights for degraded modes so managers do not contradict each other while the network is unstable.",
        "Measure post-incident cleanup time; if reconciliation takes days, your continuity design is still too cloud-centered for real operations.",
        "Treat the next maintenance window as rehearsal: throttle bandwidth in a pilot branch and observe what breaks before customers do.",
    ),
    3: (
        "POS failures are social as well as technical: cashiers improvise, supervisors override, and inventory truth diverges within minutes.",
        "ERP modules often assume synchronous validation for steps that could be deferred with explicit business rules—especially tax and identity checks.",
        "Resilience is a contract item: response-time envelopes, offline sell rules, and maximum queue depth should be testable acceptance criteria, not marketing adjectives.",
        "Demand test evidence from vendors under constrained network profiles, not only LAN demos.",
        "Integrators protect margin when failure design is explicit: fewer emergency trips and fewer weekend releases driven by panic.",
        "If you maintain a POS catalog, rank ten integrations by revenue impact and validate failure behavior for the top three first.",
    ),
    4: (
        "SLA dashboards can hide user-visible failure when micro-outages fragment sessions but never breach formal downtime thresholds.",
        "Product teams feel pressure to ship features faster than they can harden failure paths, which increases coupling without increasing safety.",
        "Design reviews should include a degradation column: what the operator sees, what the customer sees, and what finance can still prove.",
        "Publish internal “good degradation” examples so sales and delivery share the same vocabulary with engineering.",
        "Clients reward vendors who explain honest trade-offs instead of promising infinite availability.",
        "Choose one service and document its degraded mode this sprint; repeat monthly until the catalog is honest.",
    ),
    5: (
        "Offline-first is compatible with cloud analytics: the separation is about critical path, not about rejecting centralized insight.",
        "Teams fear offline-first because they imagine conflict resolution is impossible; in practice, bounded queues and idempotent commands make it manageable.",
        "The hardest part is data ownership rules: who wins when two edits disagree, and how is that communicated to operators in plain language?",
        "Pilot with a workflow that already generates support tickets today; success should reduce tickets, not increase clever exceptions.",
        "Cara Core messaging stays grounded: offline-first is discipline for field reality, not a slogan against modernization.",
        "Schedule a one-hour workshop with business and IT to write truth rules for a single entity; that document becomes your pilot contract.",
    ),
    6: (
        "Hybrid clarity reduces rework during migrations because teams know which subsystem is authoritative during each phase.",
        "Cloud-first shines for collaboration and fast iteration on non-critical workflows; local-first shines where latency and autonomy decide revenue.",
        "Security models differ: centralized policy with distributed enforcement is workable; accidental policy sprawl at the edge is not.",
        "Document rollback triggers before migration, not after the first production surprise.",
        "Partners can phase budgets when hybrid rules are explicit: less all-or-nothing capital risk for clients.",
        "Revisit the ten decisions quarterly; architecture drift happens when rules live only in chat threads.",
    ),
    7: (
        "Intermittent failures are harder than blackouts because monitoring tools disagree and operators lose trust in dashboards.",
        "Training should include “slow internet day” scenarios, not only total offline drills.",
        "Conflict resolution must be finance-aware: discounts, voids, and returns need deterministic rules when sync is delayed.",
        "Add operator-visible queue depth so frontline staff can explain delays honestly to customers.",
        "Retailers reduce shrinkage when reconciliation is fast; delays invite risky shortcuts.",
        "Instrument one branch with realistic throttling profiles and review logs weekly for a month.",
    ),
    8: (
        "Edge without governance becomes shadow IT: unmanaged devices, stale certificates, and unknown data flows.",
        "Choose edge scope where latency materially changes conversion or safety, not everywhere by default.",
        "Patching strategy must be realistic for distributed footprints: staged rollouts beat heroic manual updates.",
        "Central observability should answer: which edge node is unhealthy and what customer workflow is impacted?",
        "Partners differentiate with runbooks clients can audit.",
        "Cap edge scope to one bounded domain until operations prove patching and monitoring discipline.",
    ),
    9: (
        "“Always on” marketing language creates legal and commercial risk if engineering tests do not match the claim.",
        "Internal alignment matters: sales, support, and engineering should share the same definition of a successful degraded day.",
        "Instrument customer-visible moments: time-to-ticket, time-to-payment, and time-to-truth after recovery.",
        "Post-incident reviews should produce one structural improvement, not only a blame narrative.",
        "Cara Core prefers receipts: drill notes, metrics, and change logs that survive staff turnover.",
        "Publish one continuity KPI internally next quarter and review it in the leadership cadence.",
    ),
    10: (
        "Field technicians, pop-up stores, and traveling sales teams experience connectivity variance that headquarters Wi-Fi never reproduces.",
        "Prioritize workflows where mistakes become cash or compliance incidents, not only where complaints are loudest.",
        "Use a simple scoring sheet: revenue exposure, compliance sensitivity, rework cost, connectivity variance.",
        "Pilot in the worst branch you trust for honest feedback, not in the flagship showroom.",
        "Evidence from pilots beats slide decks in B2B procurement cycles.",
        "Score your top five distributed workflows this week and pick one pilot owner.",
    ),
    11: (
        "Joint success metrics should include continuity drills, not only go-live dates and velocity charts.",
        "Security reviews should be repeatable templates, not bespoke heroics each engagement.",
        "Change management is part of delivery: operators need training artifacts that match the production UI states.",
        "Escalation paths should name people and backups, not only mailboxes.",
        "Clients stay calmer when integrators and vendors share evidence in the same format.",
        "Add a shared risk register line item for degraded-mode behavior before contract signature.",
    ),
    12: (
        "Procurement teams increasingly ask for incident narratives and recovery evidence, not only SOC 2 checklists.",
        "Resilience investments reduce discount pressure after outages and protect brand reputation in competitive bids.",
        "Internally, fewer emergencies unlock roadmap time for differentiation instead of constant repair.",
        "Sales enablement should include honest boundaries: what the system does under stress, and what it refuses to do unsafely.",
        "Cara Core treats claims as inventory: each promise should map to a test or drill artifact.",
        "Pick one customer reference story and align it with measurable continuity outcomes before the next proposal cycle.",
    ),
}

_KEYS = ("Hook", "Real Problem", "Explanation", "Solution", "Application", "Closing")

for _n, _paras in _DEPTH.items():
    for _k, _p in zip(_KEYS, _paras):
        BODIES[_n][_k].append(_p)

_DEPTH2: dict[int, tuple[str, str, str, str, str, str]] = {
    1: (
        "Regulators and large buyers increasingly ask for continuity evidence during renewal cycles; screenshots of uptime are weaker than drill logs and reconciliation metrics.",
        "Dependency mapping should include third-party SaaS chains: one identity outage can disable five downstream systems that each look healthy in isolation.",
        "Treat vendor maintenance windows as part of your threat model: scheduled downtime should not become an unplanned business holiday.",
        "Budget for rehearsal time the same way you budget for QA: continuity is a quality gate, not an insurance footnote.",
        "When Cara Core discusses PDV and Hub patterns publicly, the emphasis stays on operator clarity and audit-friendly trails, not on buzzwords.",
        "If leadership time is constrained, delegate mapping to a cross-functional pair (IT + operations) and review only the Tier A list in the executive cadence.",
    ),
    2: (
        "Communication discipline matters: customers should hear one coherent message, not conflicting explanations from departments using different data snapshots.",
        "Legal and finance teams often become involved late because the technical team treated the outage as “short,” while business impact was already material.",
        "Document which approvals can be deferred versus which must be immediate; ambiguity creates both risk and interpersonal conflict during stress.",
        "Use simple status pages for internal staff that reflect operational reality, not optimistic green checks tied to partial subsystem health.",
        "Partners who rehearse together reduce blame cycles and speed recovery because responsibilities were agreed before adrenaline spikes.",
        "Capture one real incident timeline anonymously and use it as a training story; narrative memory beats abstract policy for frontline retention.",
    ),
    3: (
        "Inventory drift during POS incidents is a classic shrinkage vector; continuity design should make abnormal states visible, not silent.",
        "ERP integrations that batch overnight can hide latency problems until month-end close exposes inconsistencies that are expensive to unwind.",
        "Ask for failure injection tests in vendor demos: skipped steps should produce operator-safe states, not cryptic stack traces.",
        "Create a partner checklist for go-live that includes degraded-mode sign-off, not only happy-path user acceptance.",
        "Retail chains that standardize failure behavior across branches reduce training load and improve internal audits.",
        "Commit to publishing your top five failure scenarios internally; secrecy does not create resilience, rehearsal does.",
    ),
    4: (
        "Architects should pair degradation design with capacity planning: a system that degrades gracefully still needs headroom for queued work when connectivity returns.",
        "Customer contracts sometimes include availability language that engineering never reviewed; align legal clauses with testable behavior.",
        "Degraded modes should be productized features with pricing and support implications, not hidden switches only engineers know.",
        "Use post-incident metrics in quarterly business reviews so continuity improvements compete fairly with feature roadmap items.",
        "B2B buyers compare vendor maturity by how calmly vendors respond to their own incidents in public channels and partner comms.",
        "Add a “degradation owner” role to major services so accountability survives reorganizations.",
    ),
    5: (
        "Offline-first does not eliminate cloud value; it sequences it so analytics and collaboration enhance decisions without blocking transactions.",
        "Conflict handling should be explainable to a non-developer auditor; if only engineers understand merge rules, governance is fragile.",
        "Telemetry from offline queues helps prioritize which integrations deserve investment versus which should be removed as low value.",
        "Operators need confidence that queued actions will not silently disappear; visible counters and audit IDs reduce panic.",
        "Cara Core keeps editorial examples grounded in retail and distributed operations because that is where ambiguity becomes cash risk fastest.",
        "After pilot success, publish an internal one-pager: what changed, what metrics moved, and what you refuse to regress on next release.",
    ),
    6: (
        "Data residency and sovereignty concerns often push toward local-first controls even when teams prefer cloud collaboration ergonomics.",
        "Migration plans should include a temporary dual-write window with explicit exit criteria; otherwise hybrid becomes permanent confusion.",
        "Testing should validate rollback paths as thoroughly as forward migration; rollback is a continuity event.",
        "Partners should document assumptions about latency and packet loss; export markets vary widely in infrastructure quality.",
        "Hybrid clarity improves onboarding for new engineers because the system’s truth model is explicit.",
        "Run a quarterly architecture review focused only on authority drift: where did a new integration quietly change who owns truth?",
    ),
    7: (
        "Security teams worry disconnection encourages offline credential caching; design token lifetimes and device posture checks deliberately rather than banning practicality.",
        "Customer empathy improves when staff can explain delays honestly using visible queue metrics instead of vague “system problems.”",
        "Finance should pre-approve discount and void rules for degraded periods to prevent ad hoc overrides that become audit findings.",
        "Engineering should log partial failures with correlation IDs that survive sync so support can reconstruct timelines quickly.",
        "Retailers that reconcile faster reduce the window where fraud and mistakes hide in noisy data.",
        "Add one “slow day” drill per quarter with store managers present; their feedback will reshape priorities faster than remote-only reviews.",
    ),
    8: (
        "Edge AI inference is attractive but increases governance load; decide whether models at the edge are versioned with the same rigor as server deployments.",
        "Bandwidth caps mean telemetry must be sampled and prioritized; not every log line should traverse the WAN during incidents.",
        "Hardware diversity at the edge requires a small supported device matrix; infinite choice becomes infinite breakage.",
        "Disaster recovery plans should include edge node replacement playbooks with time-to-restore targets.",
        "Clients respect vendors who admit edge limits early instead of discovering them during peak season.",
        "Instrument customer-visible latency at the edge and tie improvements to revenue moments, not only to technical percentiles.",
    ),
    9: (
        "Support teams burn out when “always on” promises force permanent crisis mode; honest boundaries protect people and quality.",
        "Engineering metrics should include time-to-recover-truth, not only time-to-restore-service; inconsistent data is a silent outage.",
        "Executives should see continuity drills as brand protection, not as IT hobbies.",
        "Vendors should publish maintenance communications with customer-impact language, not only internal component names.",
        "Cara Core uses the same language in engineering and editorial because misaligned vocabulary becomes misaligned expectations in B2B delivery.",
        "If you can only fund one initiative next quarter, fund measurement: you cannot improve continuity you do not quantify.",
    ),
    10: (
        "Warehouses and distribution centers often mix Wi-Fi dead zones with high scan volume; offline-first scanning patterns reduce ripple errors.",
        "Healthcare-style consent and traceability contexts amplify the cost of inconsistent records; prioritize those workflows early.",
        "Mobile sales teams in emerging markets may face expensive data; local-first reduces cost and increases reliability simultaneously.",
        "Impact scoring should include partner effort: if a workflow is rare but extremely painful, it may still deserve early investment.",
        "Cara Core recommends publishing pilot results internally to build organizational confidence before external claims.",
        "Revisit impact scores after each peak season; seasonality changes which workflows dominate risk.",
    ),
    11: (
        "Contracts should define evidence formats for handoffs: test reports, drill logs, and change records reduce disputes at renewal.",
        "Joint backlog grooming prevents “surprise scope” that destroys trust between vendor, integrator, and client.",
        "Security exceptions should be time-bound with owners; permanent exceptions become institutional debt.",
        "Training materials should be versioned alongside releases so operators are never learning outdated screens.",
        "Partners who align on continuity drills create a shared story that helps clients justify premium budgets.",
        "Start every major milestone with a fifteen-minute risk review using the shared register; consistency beats intensity.",
    ),
    12: (
        "Reference selling becomes easier when resilience proof is packaged: one-page summaries with metrics beat long architecture decks in early-stage meetings.",
        "Churn risk often spikes after a bad incident; proactive continuity investment is cheaper than win-back discounts.",
        "Engineering morale improves when firefighting decreases; retention becomes a second-order competitive benefit.",
        "Procurement should reward vendors who disclose limitations clearly; transparency correlates with safer delivery in long programs.",
        "Cara Core treats B2B export editorial as accountable marketing: what we publish, we intend to defend with evidence.",
        "End the quarter with a resilience retro: what broke, what held, what proof you collected—and what you will fund next.",
    ),
}

for _n2, _paras2 in _DEPTH2.items():
    for _k2, _p2 in zip(_KEYS, _paras2):
        BODIES[_n2][_k2].append(_p2)

_DEPTH3: dict[int, tuple[str, str, str, str, str, str]] = {
    1: (
        "When you inventory cloud dependencies, include scheduled jobs, background sync, and “invisible” microservices invoked by macros—those fail quietly until month-end.",
        "Executives should ask for a single-page continuity narrative tied to revenue: which customer journeys stop, which degrade, and which continue unchanged.",
        "Architects should validate that authentication paths do not create circular cloud dependencies during partial outages.",
        "Run a tabletop exercise with finance present so discount and approval rules during outages are lawful and traceable.",
        "Publish a short internal memo after each drill: what worked, what broke, and the next funded fix—continuity improves when learning loops are short.",
        "If you export software or services, align public claims with drill evidence before the next major trade cycle.",
    ),
    2: (
        "Outage communications should distinguish customer impact from internal IT status; customers forgive delays they understand.",
        "Keep a printed fallback for Tier A steps only if it is controlled, numbered, and reconciled—uncontrolled paper creates worse risk than downtime.",
        "Measure how long it takes to restore managerial confidence, not only service green lights; confidence drives behavior.",
        "Integrators can differentiate by packaging rehearsal agendas and scorecards for clients.",
        "Avoid “hero engineer” dependency: if only one person can recover the system, continuity is still fragile.",
        "Share anonymized timelines with new hires during onboarding so culture learns from history.",
    ),
    3: (
        "POS peripherals (scales, scanners, printers) often fail first; continuity includes peripheral states, not only server uptime.",
        "ERP batch windows interact badly with daylight-saving and regional holidays; test calendar edge cases deliberately.",
        "Ask vendors how they handle split-brain risk when two registers believe they own the same transaction number.",
        "Document cash-handling rules explicitly for offline periods to reduce shrinkage and disputes.",
        "Standardize operator prompts across branches so training scales and audits simplify.",
        "Treat vendor roadmaps as inputs, not guarantees: your continuity model must survive vendor delays.",
    ),
    4: (
        "Degraded UX should still meet accessibility obligations; stress modes are not an excuse for unusable screens.",
        "Include customer notification templates pre-approved by legal so communications can go out quickly.",
        "Capacity for queued work should include storage growth projections; queues are a database problem as much as a network problem.",
        "Finance should model outage cost using both direct revenue loss and recovery labor—not only SLA credits.",
        "Sales should avoid promising synchronous miracles for workflows that physics and geography make fragile.",
        "Revisit degradation assumptions after every major feature release; new code paths reintroduce coupling quietly.",
    ),
    5: (
        "Offline-first pairs well with progressive enhancement in customer-facing flows: start usable, then enrich when connectivity allows.",
        "Operator training should include how to explain delays to customers without blaming unnamed “systems.”",
        "Engineering should expose safe limits: maximum offline duration, maximum queue size, and operator actions at thresholds.",
        "Analytics teams should not punish branches for honest offline usage; otherwise operators hide reality.",
        "Cara Core recommends naming a single product owner for continuity behavior so decisions do not fragment across squads.",
        "Capture before/after support ticket rates as a simple pilot success signal.",
    ),
    6: (
        "Hybrid systems need consistent observability: the same trace IDs should work across edge and cloud where possible.",
        "Document data retention differences between local caches and cloud warehouses to avoid compliance surprises.",
        "Partners should align on incident severity definitions so Sev-1 means the same thing to everyone.",
        "Include contract clauses for cooperative debugging during outages; finger-pointing delays recovery.",
        "Architecture diagrams should show authority arrows, not only boxes and lines.",
        "Celebrate small hybrid wins publicly inside the organization to build patience for longer migrations.",
    ),
    7: (
        "Disconnection playbooks should include customer compensation policies pre-approved within bounds to avoid chaotic ad hoc discounts.",
        "Engineering should test DNS failure modes explicitly; many “mystery” outages are resolver issues, not application bugs.",
        "Retail peaks (holidays) deserve rehearsed degraded modes because errors are most expensive when volume is highest.",
        "Keep reconciliation SLAs realistic and monitored; silent backlog is a liability.",
        "Partners should rehearse handoffs: who owns customer comms during vendor maintenance overlaps.",
        "Log operator decisions during drills; those logs reveal where UX misleads staff under stress.",
    ),
    8: (
        "Edge security should assume physical access risks: locked ports, tamper evidence, and device attestation where feasible.",
        "Consider energy resilience for edge nodes: short outages at the outlet look like mysterious “software” failures.",
        "Update channels must be resilient too; a broken update mechanism bricks the field fleet.",
        "Telemetry backhaul should degrade gracefully with sampling when uplinks saturate.",
        "Clients appreciate edge roadmaps that include retirement and refresh budgeting.",
        "Pair edge pilots with a support readiness review so help desks are not surprised by new failure signatures.",
    ),
    9: (
        "Define “never stop” with customer-language milestones: payment captured, ticket issued, prescription logged—whatever matches your domain.",
        "Avoid metric theater: fewer KPIs with clear ownership beats dashboards nobody acts on.",
        "Include continuity in vendor scorecards alongside velocity and defect counts.",
        "Reward teams for calm incident execution, not only for preventing incidents—prevention is not always controllable.",
        "Cara Core emphasizes evidence in partner reviews: show drill notes, not intentions.",
        "If marketing and engineering disagree on claims, resolve it before the next public release—not after social media notices.",
    ),
    10: (
        "Pop-up retail and events create extreme Wi-Fi contention; design scanning and payment flows accordingly.",
        "Inventory cycle counts are continuity-sensitive; inaccurate counts propagate through replenishment algorithms.",
        "Field service fleets need offline-capable work orders with parts accountability.",
        "Prioritize workflows where mistakes create regulatory exposure, not only where managers complain loudest.",
        "Use pilot metrics to decide whether to expand offline-first scope or invest elsewhere.",
        "Communicate pilot boundaries clearly so operators do not assume unlimited offline capability.",
    ),
    11: (
        "Define a shared definition of done that includes degraded-mode acceptance, not only happy-path UAT.",
        "Joint retrospectives after drills strengthen relationships more than joint celebrations after launches alone.",
        "Integrators should bring standard test data packs; clients should bring realistic dirty data samples.",
        "Agree on communication channels during incidents: one war room, one log, one timeline owner.",
        "Document vendor versus integrator versus client responsibilities for patching and certificates.",
        "Start small: one pilot, one workflow, one measurable continuity outcome—then scale the collaboration pattern.",
    ),
    12: (
        "Resilience becomes a moat when competitors still sell fragile demos as production-ready promises.",
        "Insurance and risk teams increasingly ask technical questions; prepare answers that engineers can defend.",
        "Long-term contracts benefit from continuity appendices with measurable review points.",
        "Brand teams should coordinate claims with engineering test coverage to avoid social-media corrections.",
        "Cara Core treats export editorial as part of product integrity: words and systems should match.",
        "Commit publicly to one resilience improvement per quarter; steady progress beats occasional heroics.",
    ),
}

for _n3, _paras3 in _DEPTH3.items():
    for _k3, _p3 in zip(_KEYS, _paras3):
        BODIES[_n3][_k3].append(_p3)

_DEPTH4: dict[int, tuple[str, str, str, str, str, str]] = {
    1: (
        "If you only remember one sentence: design so revenue-critical work can continue with clear rules when the cloud is slow, absent, or inconsistent.",
        "Measure twice on dependencies that touch money, identity, and inventory; those are where outages become legal and commercial exposure, not only IT tickets.",
        "Resilience budgets should include operator time: rehearsing and reconciling is real labor that must be planned, not squeezed into nights and weekends forever.",
        "Prefer small, verifiable reductions in cloud-only coupling over large rewrites that stall after the first executive workshop.",
        "When in doubt, choose boring technology with explicit failure behavior over clever automation nobody can explain during an incident.",
        "Forward this article to your program manager with one question: which Tier A workflow still dies when DNS flickers?",
    ),
    2: (
        "The goal is not zero outages—it is controlled behavior during outages that customers and auditors can still trust.",
        "Write the customer script for hour one: what you say, what you offer, and what you refuse to do unsafely—even under revenue pressure.",
        "Keep incident timelines lightweight but honest; they become training gold and protect the organization from mythology after the fact.",
        "If your playbook is longer than two pages, operators will not read it under stress; split reference detail into appendices.",
        "Partners should rehearse joint comms: mismatched vendor and integrator messages erode client confidence faster than downtime itself.",
        "End every outage with a single structural action item funded within thirty days, or lessons will evaporate.",
    ),
    3: (
        "POS and ERP buyers should reward vendors who demonstrate failure behavior, not only happy-path feature velocity.",
        "Ask for video evidence of offline sell paths, not only architecture slides—execution matters more than intent.",
        "If a vendor cannot show reconciliation after forced failures, assume you will pay for that discovery in production.",
        "Integrators should standardize a POS hardening checklist and reuse it across clients to amortize learning.",
        "Finance should track shrink and rework deltas after POS incidents; those numbers justify continuity investment.",
        "Pick one branch for honest failure testing next month; comfort with ugly results early prevents expensive surprises later.",
    ),
    4: (
        "Degradation design is a product skill: it needs UX, legal, finance, and engineering in the same room early.",
        "If degraded modes feel embarrassing to demo, that is a signal you are closer to real operations than a glossy keynote.",
        "Publish internal examples of good degradation to align sales promises with engineering truth.",
        "Treat incident blameless reviews as product inputs; recurring themes belong on the roadmap with dates.",
        "Clients should ask vendors for degradation acceptance tests as part of procurement scoring.",
        "Make degradation visible in demos on purpose; trust grows when vendors show honesty, not only sunshine paths.",
    ),
    5: (
        "Offline-first is a journey: start with one workflow, prove reconciliation quality, then expand scope with evidence.",
        "Do not let perfect conflict resolution block pragmatic progress; start with bounded queues and clear operator prompts.",
        "Invest in training artifacts that match real UI states, including offline banners and queue counters.",
        "Celebrate reconciliation improvements as loudly as feature launches; they protect margin.",
        "Cara Core recommends writing truth rules in business language first, then translating to technical schemas.",
        "Send operators a one-page cheat sheet after each pilot; laminated beats forgotten wiki pages.",
    ),
    6: (
        "Hybrid clarity is a negotiation tool: it reduces hidden assumptions between business, IT, and vendors.",
        "Document temporary dual-write rules with sunset dates or hybrid becomes permanent confusion.",
        "Align procurement milestones to hybrid reality: some benefits arrive late by design; plan cash flow accordingly.",
        "Partners should publish a joint migration risk register template and reuse it.",
        "Engineering should track authority drift quarterly; silent changes are how hybrids fail.",
        "If hybrid debates stall, prototype the smallest end-to-end slice instead of arguing abstractly for months.",
    ),
    7: (
        "Disconnection survival is also a leadership communication exercise: calm tone reduces operational mistakes.",
        "Engineers should verify behavior under captive portals and DNS failures separately; symptoms differ.",
        "Retailers should rehearse holiday peaks with realistic traffic and staffing levels, not only quiet Tuesday mornings.",
        "Finance should pre-approve bounded compensation policies for outage periods to reduce chaotic discounts.",
        "Partners should align on customer ownership during overlapping maintenance windows.",
        "Keep drill logs short: timestamp, scenario, outcome, one improvement—repeat monthly.",
    ),
    8: (
        "Edge success requires disciplined scope: expand only where latency or autonomy truly changes outcomes.",
        "Security and patching must be designed for distributed reality, not copied from a single data center checklist.",
        "Telemetry should be budgeted like bandwidth: sampling and prioritization prevent observability from becoming an outage cause.",
        "Hardware refresh plans belong next to edge roadmaps; aged devices become silent risk.",
        "Clients should demand edge failure drills with replacement time targets.",
        "Pair edge adoption with help-desk training so new failure signatures are diagnosable quickly.",
    ),
    9: (
        "Never-stop claims need never-stop evidence: drills, metrics, and post-incident improvements on a calendar.",
        "Reduce KPI noise: fewer metrics with owners beats dashboards nobody acts on.",
        "Continuity should appear on vendor scorecards beside velocity and defect rates.",
        "Reward calm execution during incidents; prevention is not always controllable, behavior is.",
        "Cara Core aligns public editorial language with engineering tests to protect partner trust.",
        "Pick one KPI, publish it internally, review it monthly for two quarters—that is how culture shifts.",
    ),
    10: (
        "Impact mapping prevents vanity pilots: choose workflows where mistakes become money, compliance, or reputation risk.",
        "Field reality beats HQ assumptions; listen to branch and technician feedback when scoring impact.",
        "Pilot metrics should include support tickets, reconciliation time, and shrink signals—not only uptime.",
        "Communicate pilot limits clearly to prevent operators assuming infinite offline capability.",
        "Cara Core recommends publishing internal pilot summaries to build organizational confidence before external claims.",
        "Re-score workflows after each peak season; risk shifts with volume and promotions.",
    ),
    11: (
        "Partnerships improve when evidence formats match across vendor, integrator, and client artifacts.",
        "Joint backlog grooming reduces surprise scope that destroys trust late in programs.",
        "Security exceptions need expiry dates and named owners or they become permanent debt.",
        "Training materials must version with releases or operators learn outdated screens.",
        "Joint continuity drills create a shared story that helps clients justify premium budgets.",
        "Use a fifteen-minute risk review at major milestones; consistency beats occasional heroics.",
    ),
    12: (
        "Resilience as advantage shows up in calmer renewals, fewer win-back discounts, and stronger references.",
        "Prepare procurement answers engineers can defend; risk teams ask harder questions now.",
        "Long contracts benefit from continuity appendices with measurable review points.",
        "Coordinate brand claims with engineering tests to avoid public corrections after incidents.",
        "Cara Core treats export editorial as accountable product communication.",
        "Close the quarter with a resilience retro and fund the top structural fix—steady progress compounds.",
    ),
}

for _n4, _paras4 in _DEPTH4.items():
    for _k4, _p4 in zip(_KEYS, _paras4):
        BODIES[_n4][_k4].append(_p4)


def render_html(num: int, date_iso: str, title: str, img_prefix: str) -> str:
    body = BODIES[num]
    parts: list[str] = []
    for section, paras in body.items():
        parts.append(f"      <h2>{section}</h2>")
        for p in paras:
            parts.append(f"      <p>{p}</p>")
    inner = "\n".join(parts)
    fn = f"{img_prefix}_article_{num:02d}_.html"
    return textwrap.dedent(
        f"""\
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Article {num:02d} — {title}</title>
          <meta name="description" content="B2B export campaign article (~5 min read). Editorial schedule from June 2027.">
          <link rel="stylesheet" href="assets/css/sala-doc.css">
        </head>
        <body>
          <header class="sala-header">Cara Core Informatica · B2B Export · Article {num:02d}</header>
          <main class="container">
            <div class="breadcrumb"><a href="../index.html">B2B Export</a> / <span>Article</span></div>
            <article class="panel">
              <h1>{title}</h1>
              <p><strong>Publish date:</strong> {date_iso}</p>
              <p><strong>Estimated reading time:</strong> about 5 minutes</p>

              <figure class="article-hero-image">
                <picture>
                  <source media="(max-width: 600px)" srcset="assets/img/{img_prefix}_mobile.webp" width="800" height="1000">
                  <img src="assets/img/{img_prefix}_desktop.webp" alt="{title}" width="1200" height="630" loading="lazy" decoding="async">
                </picture>
              </figure>
              <p class="image-note"><strong>About this image:</strong> Campaign visual carried forward for this article slot; update asset if you refresh the creative.</p>

        {inner}
        </article>
          </main>
          <script src="assets/js/article.js" defer></script>
        </body>
        </html>
        """
    )


def main() -> None:
    ART_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    # Write new HTML + copy images
    for num, new_date, old_prefix, title, _kw, _subj in SPECS:
        img_prefix = new_date.replace("-", "_")
        for kind in ("desktop", "mobile"):
            if not (IMG_DIR / f"{img_prefix}_{kind}.webp").is_file():
                raise SystemExit(f"Missing hero image {img_prefix}_{kind}.webp in {IMG_DIR}")
        html_name = f"{img_prefix}_article_{num:02d}_.html"
        html_path = ART_DIR / html_name
        y, m, d = new_date.split("_", 2)
        display_iso = f"{y}-{m}-{d}"
        html_path.write_text(
            render_html(num, display_iso, title, img_prefix),
            encoding="utf-8",
            newline="\n",
        )

    # Remove legacy article HTML and old PNGs
    legacy_dates = [
        "2026_04_13", "2026_04_20", "2026_04_27", "2026_05_04", "2026_05_11", "2026_05_18",
        "2026_05_25", "2026_06_01", "2026_06_08", "2026_06_15", "2026_06_22", "2026_06_29",
    ]
    for d in legacy_dates:
        for p in ART_DIR.glob(f"{d}_article_*.html"):
            p.unlink(missing_ok=True)
        png = IMG_DIR / f"{d}_IMAGE_01.png"
        png.unlink(missing_ok=True)

    print("Wrote 12 new articles + images; removed legacy April–June filenames.")


if __name__ == "__main__":
    main()
