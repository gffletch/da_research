# Delegated Authorization for AI Agents — Research Corpus

A bibliography + knowledge graph tracking the IETF / OIDF / academic / industry
work on how authority delegates from humans to AI agents. Maintained as a living
research artifact; updated additively as new drafts and blog posts appear.

Maintainer is an IAM/delegated-authz expert. Date context: current entries
dated through Aug 2026 (last full sweep: 26 Aug 2026).

## Files

**Canonical (the source of truth — update these):**

- `delegated_authorization_research.xlsx` — the bibliography. **408 sources**
  across 7 tabs (Index + 6 content tabs).
- `agent_authz_graph.json` — RAG-ready knowledge graph: **438 nodes, 659 edges**,
  in sync with the workbook as of 26 Aug 2026. **Generated, not hand-edited** —
  `build_graph.py` derives it from the workbook. Every node and edge carries an
  `origin` field (`curated` / `mission-manifest` / `workbook` / `derived`); only
  `curated` survives a rebuild, so hand-written analysis is safe but derived
  content is regenerated each time.
- `agent_authz_graph.html` — interactive D3 force-directed viz of the JSON,
  D3 inlined for offline use (~391KB).

**Build scripts:**

- `build.py` — the workbook builder. Was named `build_v10.py` in the chat
  session that produced this bundle; renamed to drop the version suffix since
  git history now provides the audit trail. Monolithic (all data inline). Run
  `python build.py` after editing to regenerate the workbook.
- `build_graph.py` — the graph builder. Rewritten 11 Aug 2026 to derive from the
  workbook instead of carrying nodes inline (the old design is why it drifted
  270 sources behind). Also re-splices the JSON into `agent_authz_graph.html`
  between the `<script id="graph-data">` markers, leaving the inlined D3 bundle
  alone. Idempotent — re-running does not compound. Run `python build_graph.py`.

**Helper:**

- `validate.py` — quick sanity check. Run after every edit. Loads workbook,
  prints tab counts, confirms Index total equals row sum, lists any unparseable
  rows, sanity-checks every URL is well-formed.

**Explicitly out of scope for ongoing maintenance** (these are snapshots that
will not be updated as the corpus grows — do not regenerate unless asked):

- `IETF_individual_drafts_infographic.html` — editorial broadsheet (32 drafts)
- `drafting_authority_deck.pptx` — 11-slide presentation

Both still exist from the original session if needed.

## Tab structure

| Tab                        | Count | Notes                                                  |
| -------------------------- | ----- | ------------------------------------------------------ |
| Index                      | cover | Auto-summed; cell `C11` = TOTAL                        |
| Published RFCs             | 4     | Stable. Foundation primitives.                         |
| Active IETF Drafts         | 290   | **★ Where the action is.** WG + individual drafts.     |
| OpenID Foundation          | 11    | Final + draft OIDF specs.                              |
| Other Standards & Govt     | 7     | Kantara, W3C, NIST, EU AI Act, NSA MCP CSI.            |
| Academic Papers            | 12    | arXiv + IEEE.                                          |
| Industry & Implementations | 84    | Vendor blogs, reference impls, full Control Plane blog.|

Row schema:

- In `build.py`, each row is a 5-tuple: `(title, summary, url, standards_org, comments)`.
- In the rendered workbook, the builder prepends a `#` column (auto-numbered),
  so the actual layout is 6 columns: `# | Title | Summary | Link | Standards Org | Comments`.
- Headers live at row 1. Data starts at row 2.

## The five thematic clusters (within Active IETF Drafts)

The Active IETF Drafts tab informally groups individual-submission drafts
into five thematic clusters used by the original infographic and the graph.
Still useful as a mental model when placing new drafts:

1. **Delegation mechanics** (7) — actor profiles, chain mechanics, RAR-for-agents
2. **Agent identity** (7) — identity frameworks, instance assertion, three-way
   "AIP" name collision (singla, prakash, aip-protocol)
3. **Discovery & transport** (5) — well-known/.dawn discovery, mcp:// URI,
   agent transport protocols
4. **Audit & compliance** (3) — kuehlewind-audit-architecture is the HUB
   that composes 10+ other specs
5. **Adjacent / cross-cutting** (10) — hardt-aauth (OUTLIER, zero OAuth deps),
   framework documents, vertical-specific applicability statements

## Author voices to track

- **Karl McGuinness** (Independent, former Okta SVP & Chief Product Architect).
  Most concentrated single-author body of work in the corpus — currently:
  - **18 individual I-Ds** on Datatracker, incl. actor-profile, actor-proofs,
    ai-agent-instance, client-instance-assertion, deferred-code-processing,
    domain-authorized-issuer, id-assertion-framework, insufficient-claims,
    mission, mission-bound-minimum-profile, mission-bound-runtime-enforcement-profile,
    resource-token-resp, rfc9728bis, token-xchg-target-svc-disco,
    token-exchange-cnf (Jul 2026), id-continuation-assertion (Aug 2026)
  - **The 34-draft Mission-Bound Authorization family** at
    `github.com/mcguinness/mission-bound-authorization` — 33 are GitHub-only
    (marked "IETF (Pre-publication — GitHub)" in standards-org); only
    `draft-mcguinness-oauth-mission` is also on Datatracker. The repo ships a
    machine-readable `family-manifest.json` (group, maturity, adoption_rung,
    deps per draft) — **use it as the source of truth** for this family rather
    than re-deriving structure. Groups: architecture, core, approval-time,
    lifecycle, runtime-enforcement, bindings-substrate, agent-runtime,
    sub-agents, cross-domain-projection, proof-portability, security-model.
  - **1 OIDF profile** in OpenID Foundation tab: AuthZEN Access Request &
    Approval Profile (ARAP) — adopted as WG draft May 2026, Draft 1 published
    3 Jun 2026
  - **50 blog entries** at `notes.karlmcguinness.com` ("Control Plane"), all now
    in the Industry & Implementations tab. Major arcs: Agent Control Points
    (Aug 2026), the Mission-Bound Authorization handbook + 5 series indexes
    (Jul 2026), Open-World OAuth (Mar 2026), Least-Privilege MCP (Jun 2026).
    The site's `/index.xml` RSS feed is the reliable way to enumerate *posts* —
    scraping the paginated HTML index misses most of them and reports wrong dates.
    **But RSS is not the whole site (learned 26 Aug 2026).** The 27 chapters of
    the Mission-Bound Authorization handbook live under `/notes/` and are *not*
    in the feed; only the handbook's series landing pages are. To enumerate the
    full surface, union the RSS links with the hrefs scraped from
    `/mission-handbook/` and `/mission-handbook/read/`.
    **Karl also re-slugs.** Three corpus URLs 404'd by 26 Aug 2026 because the
    site renamed "Mission-Bound OAuth" to "Mission-Bound Authorization"
    throughout. `validate.py` only checks that URLs are well-formed, not that
    they resolve — so a link-liveness pass belongs in every blog sweep.
  - Co-author on `draft-ietf-oauth-identity-assertion-authz-grant` (ID-JAG)
  - **Pending I-Ds** referenced in his blogs but NOT yet on Datatracker —
    see Pending Watch List below

- **Kühlewind / Birkholz** (Ericsson / Fraunhofer SIT). `draft-kuehlewind-audit-architecture`
  is the integrator HUB — composes 10+ other specs into a single auditable
  architecture. When a new draft arrives, ask whether it belongs in that
  draft's composition graph.

- **Dick Hardt**. `draft-hardt-oauth-aauth-protocol` (slug gained the `oauth`
  infix at -09; now at -10, 6 Aug 2026) is the principled OUTLIER —
  zero OAuth dependencies; argues PoP-by-default, resource-signed challenges,
  and AS-to-AS federation are architectural changes, not extensions. Flag
  any new draft that echoes those design choices.

- **Larry Lewis**. `agent-trust-protocol/atp-core` (Industry tab, row 5).
  Acronym near-collision with `draft-sharif-attp` — different designs:
  discrete L0–L4 trust levels there, continuous 0.0–1.0 trust scoring here.

- **Morrison** (added 26 Aug 2026). A self-referential **six-draft family** built
  on a `~handle` identity primitive defined in its own `[MCPDNS]` draft, with an
  entity-class taxonomy of Sovereign / Bot / Instrument: `consent-settlement`,
  `identity-accord`, `solo-agent-earn-registration`, `agent-channel-fan-out`,
  `identity-pronouns`, `identity-attributed-commits`, plus the
  `mcp-tool-surface-names-registry` that exists only to create the IANA registry
  the others register into. Taken in full under the primary-body rule. Two things
  make it worth watching: it is the only body of work here that treats an
  **owner-less agent** as a first-class economic principal, and its three-tier
  actor taxonomy restates the actor-chain question in a non-OAuth substrate.

- **Sharif**. Now **four** drafts: `sharif-attp`, `sharif-agent-audit-trail`,
  `sharif-mcps-secure-mcp` (added 26 Aug 2026), and the SUPERSEDED
  `sharif-payment-trust`. Crossed the threshold from single draft to a body of
  work — treat as a primary author on the next sweep.

## How to add a new source

Standard workflow (Claude Code + git):

1. **Edit `build.py` in place.** Locate the right tab section (search for
   `# TAB N:`). Find the right placement within the tab — see Placement Rules
   below. Add the row as a 5-tuple.
2. **Update Index tab description** for the affected tab if the addition
   changes the cluster narrative.
3. **Run the build:** `python build.py`
4. **Validate:** `python validate.py`
5. **Commit:** the git history is now the version trail; no need for `build_v{N+1}.py`.
6. **Decide on graph sync.** Graph rebuild is deliberate, not automatic. If
   the addition is structurally significant (new dependency edge, new cluster
   member, new external composition), update `build_graph.py` and rerun.
   Otherwise leave the graph stale and batch the sync.

## Placement rules within tabs

- **Active IETF Drafts:** loose grouping by author cluster, then by submission
  date. Do NOT rely on absolute row numbers — the tab is 242 rows and they
  shift with every sweep; locate clusters by draft-name search instead. The
  early McGuinness cluster still sits near `draft-mw-oauth-actor-chain`, which
  is kept adjacent because it directly responds to his Actor Profile. The
  Aug 2026 sweep appended two labelled blocks at the end of the tab:
  the Mission-Bound Authorization family, then the general Datatracker sweep.
  New McGuinness drafts go with the relevant block.
- **Industry & Implementations:** 5 reference implementations lead (rows 1–5),
  then the McGuinness Mission-Bound blog series (rows 7–10, publication order:
  MVP first as the substrate post), then blogs and analyst articles.
- **OpenID Foundation:** AuthZEN cluster groups together (AuthZEN 1.0 →
  MCP Profile → ARAP), then CAEP/SSF, then FAPI, then HEART.

## Narration style (the `comments` column)

- State the maturity signal — revision number, date, WG adoption status.
- Note structural relationships to other drafts already in the corpus.
- Flag observations that matter — re-slugs, name collisions, supersession.
- Be honest about caveats — early-stage, GitHub-only, leaked credentials,
  unusual authorship signals.
- Don't editorialize the technical content — that's what the `summary`
  column is for.

## Tagging conventions (used in graph + derivatives)

- **HUB** — composes 5+ other drafts. Currently: `kuehlewind-audit-architecture`.
- **OUTLIER** — deliberately depends on nothing else in the corpus.
  Currently: `hardt-oauth-aauth-protocol` (note the `oauth` infix added at -09).
- **COLLISION** — name conflict with another draft. Currently **four** "AIP"
  drafts: singla, prakash, aip-agent-identity-protocol, and
  `fane-opena2a-aip` (-02, 6 Aug 2026). Note its companion `fane-opena2a-aap`
  also collides acronym-wise with the unrelated `draft-aap-oauth-profile`
  (Agent Authorization Profile) added in the Aug 2026 sweep.
- **SUPERSEDED** — replaced by a re-slug. Currently: `sharif-payment-trust`
  (replaced by `sharif-attp`).

## Pending watch list

**McGuinness watch list — RESOLVED as of the 11 Aug 2026 sweep.** All five
previously-pending drafts are now filed and in the corpus (two under shorter
slugs than originally watched: `domain-authorized-issuer`, `id-assertion-framework`).
Two further drafts appeared and were added: `token-exchange-cnf` (-00, 19 Jul 2026)
and `id-continuation-assertion` (-00, 3 Aug 2026).

Still worth periodic checking: whether any of the 33 GitHub-only Mission-Bound
family drafts get filed on Datatracker. Only `draft-mcguinness-oauth-mission`
has been so far. Re-check with the family-manifest slugs.

**Graph — REBUILT 26 Aug 2026.** Now 438 nodes / 659 edges, in sync with the
workbook. `build_graph.py` derives it; adding a source no longer requires
touching that file. Edge provenance: 116 curated (the original hand-written
analysis, preserved), 373 `composes` from the Mission-Bound family manifest,
155 auto-derived `references` from bibliography text.

Notes for future graph work:

- 30 nodes are **curated substrate** (`in_workbook: false`) — foundational RFCs
  like 7519/7521/7523/9068/9334 that the bibliography cites but doesn't track as
  its own sources. They are preserved across rebuilds because curated edges hang
  off them. Don't "clean them up".
- `MISSION_FAMILY` in `build_graph.py` mirrors the upstream `family-manifest.json`
  (snapshot 11 Aug 2026). Re-sync it if the family changes shape.
- The HTML shell's filter pills, `TYPE_COLOR`/`CAT_COLOR`, and `nodeRadius` maps
  are hand-maintained. **If you add a new node type or category, add a matching
  filter pill** — `applyFilters()` hides any node whose type has no checked pill,
  so a missing pill silently makes nodes invisible.

**Fixed 11 Aug 2026:** the two duplicate Industry rows from commit `612bb30`
(Defakto IETF 122, Rock Lambros RockCyber) were removed, keeping the richer
narration of each pair.

**26 Aug 2026 sweep — findings that change the corpus's shape:**

- **`draft-ietf-oauth-browser-based-apps` became RFC 10017** (state flipped
  21 Aug 2026; `became_rfc` relation confirmed on Datatracker). Its row is still
  in the Active IETF Drafts tab with a note. **Open placement question for the
  maintainer:** move it to the Published RFCs tab (which would make that tab 5)
  or leave it annotated in place.
- **`draft-aap-oauth-profile` is now EXPIRED.** Kept, annotated. It is half of
  the AAP/AIP acronym tangle recorded under COLLISION.
- **`draft-ietf-oauth-transaction-tokens` advanced past WGLC** to
  "WG Consensus: Waiting for Write-Up" (21 Aug 2026). `identity-chaining` and
  `rfc7523bis` are both sitting in the RFC Editor queue; neither has an RFC
  number yet. `wimse-workload-identity-practices` reached IESG AD Evaluation.
- **The candidate decision/policy cluster is now seven drafts**, not six —
  `gazitt-oauth-authzen-claims` (a third Gazitt AuthZEN draft) and
  `li-oauth-policy-based-anonymous-tokens` joined; still no OAuth wiki cluster
  fits them. This strengthens the case for raising it upstream.
- **`draft-ietf-oauth-rar-metadata-remediation` is the first new WG-level draft
  in this space since the recharter.** RAR is the primitive the Mission-Bound
  family builds on, so this is the closest thing yet to Complex Delegation
  machinery arriving in chartered WG work. Watch it.

**Other deferred items:**

- **Open curation decision — the 27 Mission-Bound handbook chapters.** Surfaced
  26 Aug 2026. Karl's handbook chapters (all dated 22 Jul 2026) each have their
  own `/notes/` URL but are **absent from the RSS feed**, which is why the
  11 Aug sweep missed them. Three of them were already tracked under their
  pre-handbook slugs and have now been repointed; **24 chapters plus 5
  handbook-only `/series/` indexes remain untracked.** The argument for adding
  them is the primary-body rule (all 50 blog entries are tracked). The argument
  against is that they are a re-issued edition of material already in the
  corpus rather than new sources. Adding all 29 would take Industry from 84 to
  113. Maintainer has not ruled.

- **Open curation decision — Vauban x402 pair.** `draft-vauban-x402-stark-receipts`
  and `draft-vauban-x402-pqc-receipts` were surfaced in the Aug 2026 sweep but
  deliberately left out: they are x402 *receipts* (which the corpus now tracks,
  via the Hopley cluster) but their subject is STARK / post-quantum proof
  discipline rather than payment authorization. Maintainer has not ruled. Add
  them if the corpus decides cryptographic proof systems are in scope.
- User has deferred adding a "maturity/readiness" column to the Active Drafts
  tab. The Mission-Bound family now carries maturity + adoption_rung inline in
  its comments column, which is a partial precedent — revisit.
- **OAuth cluster taxonomy — use "Complex Delegation".** The official OAuth spec
  clustering lives at https://wiki.ietf.org/group/oauth/OAuthSpecClusters
  (presented at IETF 126). Ten clusters; the tenth, "Complex Delegation", is
  present but `(TBD)` — no documents assigned. Maintainer settled 11 Aug 2026 on
  using that name rather than coining "Delegated Authorization".
  - **The name is now chartered, not just a wiki heading** (confirmed 26 Aug
    2026, see recharter entry below). Charter rev 06 lists "Complex Delegation"
    as one of five work-program items. This retires any doubt about the naming
    choice — the corpus and the WG use the same term for the same thing.
  - The wiki currently lists **only RFCs and WG drafts** — no individual drafts
    anywhere. Assignment of individual drafts is underway upstream; publication
    venue not yet decided. **Don't assign clusters per-draft in the corpus yet.**
  - A mapping of the corpus's 77 OAuth-named individual drafts against the ten
    clusters found roughly 35 already fit existing clusters — notably ~5 in
    Proof of Possession, which currently shows "Active Drafts: (none)". Agent
    drafts should be filed by *mechanism*, not by being agent-flavoured.
  - **Open observation worth raising upstream:** six drafts fit no current
    cluster — gazitt-oauth-authzen-issuance, gazitt-oauth-authzen-token-exchange,
    liu-oauth-rego-policy, vicente-oauth-apm, liu-oauth-authorization-evidence,
    fulz-oauth-trust-binding. These concern *who decides, on what evidence*
    rather than how authority moves, and may warrant a distinct
    decision/policy cluster.
- **OAuth WG recharter — SUCCESSFUL. Resolved 26 Aug 2026** (maintainer
  reported; verified against Datatracker). `charter-ietf-oauth` **rev 06**,
  timestamped `2026-06-04T16:32:25Z` — the 4 Jun 2026 IESG telechat — is in
  state **Approved** ("The charter is approved by the IESG").
  - **Why this matters to the corpus:** the new charter adds an explicit framing
    sentence — *"As automated agents increasingly act on behalf of users,
    organizations, or both, these delegation patterns become increasingly
    involved and complex."* — and charters **Complex Delegation** as work:
    *"Developing new mechanisms or/and extensions for authorization of automated
    agents working on behalf of users, including addressing scenarios where
    automated agents act across multiple administrative domains."* The corpus's
    entire subject is now in-charter for the OAuth WG, and cross-domain agent
    delegation is called out by name.
  - The other four work-program items: Consolidation (OAuth 2.1),
    Digital Credentials (SD-JWT / SD-JWT VC / Token Status List),
    First-Party Integration, Security Maintenance (browser-based + native BCPs).
    Chartered coordination with **WIMSE** (token exchange + DPoP for
    service-to-service and multi-hop workload identity), SPICE, and the
    EU Digital Identity Wallet.
  - **But there is no Complex Delegation milestone yet.** The WG's only three
    active milestones are SD-JWT VC (due 31 Jul 2026), OAuth 2.1 and
    Transaction Tokens (both 31 Dec 2026). Chartered scope without a deliverable
    is consistent with the wiki cluster still reading `(TBD)` — the WG has taken
    the *mandate* but not yet committed to a document. **Watch for the first
    Complex Delegation milestone or WG adoption; that is the signal that turns
    the corpus's individual-draft tail into WG work.**

**Curation bar for the general draft tail** (set 11 Aug 2026, applies to routine
sweeps — don't re-ask): keep delegation, agent identity, authorization, consent,
and receipt drafts. Drop networking/transport (IPv6, multicast, network
management), generic browser-flow and JWT-BCP drafts, and non-agent supply-chain
work. Payments-infra *is* in scope as of this decision (Skyfire KYA/KYAPay and
Hopley x402 clusters were reinstated). Primary/authored bodies of work — a single
author's draft family or blog — are taken in full rather than sampled.

## Things NOT to do

- **Don't add placeholder rows** for drafts that don't exist yet. If a draft
  is referenced in a blog but Datatracker returns nothing, note it in the
  Pending Watch List above instead.
- **Don't update the snapshot derivatives** (infographic, deck) unless
  explicitly asked. They were one-time deliverables, not living documents.
- **Don't search for `draft-mcguinness-authzen-access-request` on Datatracker.**
  AuthZEN is an OIDF working group, not IETF; the spec lives at
  `openid.github.io/authzen/...` and is the ARAP entry in the OIDF tab.
- **Don't hand-edit `agent_authz_graph.json` or the graph data inside
  `agent_authz_graph.html`.** Both are generated; edits are overwritten on the
  next `python build_graph.py`. To change curated analysis, edit the node in the
  JSON *and* keep its `origin: "curated"` — that is the only content a rebuild
  preserves. The old advice to batch graph syncs no longer applies: the rebuild
  is now a single cheap command, so run it whenever the workbook changes.
- **Don't create `build_v11.py`, `build_v12.py`, etc.** That pattern was an
  artifact of working without git. Edit `build.py` in place and commit.
