# Delegated Authorization for AI Agents — Research Corpus

A bibliography + knowledge graph tracking the IETF / OIDF / academic / industry
work on how authority delegates from humans to AI agents. Maintained as a living
research artifact; updated additively as new drafts and blog posts appear.

Maintainer is an IAM/delegated-authz expert. Date context: current entries
dated through Sep 2026 (last full sweep: 29 Sep 2026).

## Files

**Canonical (the source of truth — update these):**

- `delegated_authorization_research.xlsx` — the bibliography. **695 sources**
  across 8 tabs (Index + 7 content tabs).
- `agent_authz_graph.json` — RAG-ready knowledge graph: **725 nodes, 952 edges**,
  in sync with the workbook as of 29 Sep 2026. **Generated, not hand-edited** —
  `build_graph.py` derives it from the workbook. Every node and edge carries an
  `origin` field (`curated` / `mission-manifest` / `workbook` / `derived`); only
  `curated` survives a rebuild, so hand-written analysis is safe but derived
  content is regenerated each time.
- `agent_authz_graph.html` — interactive D3 force-directed viz of the JSON,
  D3 inlined for offline use (~391KB).

**⚠ Use `./.venv/bin/python`, not bare `python`.** The commands below are written
as `python build.py` etc., but the system interpreter has no `openpyxl` — every
build/validate/graph script dies with `ModuleNotFoundError`. The project `.venv`
at the repo root has it.

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
  rows, sanity-checks every URL is well-formed. **Rewritten 26 Aug 2026 to be
  tab-agnostic**: it discovers content tabs from the workbook and finds the
  TOTAL row by its label instead of hardcoding a tab list and cell `C11`. Both
  assumptions broke the moment a tab was added. Note it still checks only that
  URLs are *well-formed*, never that they resolve — that gap let three dead
  blog links sit unnoticed for a full cycle.

**Explicitly out of scope for ongoing maintenance** (these are snapshots that
will not be updated as the corpus grows — do not regenerate unless asked):

- `IETF_individual_drafts_infographic.html` — editorial broadsheet (32 drafts)
- `drafting_authority_deck.pptx` — 11-slide presentation

Both still exist from the original session if needed.

## Tab structure

| Tab                        | Count | Notes                                                  |
| -------------------------- | ----- | ------------------------------------------------------ |
| Index                      | cover | Auto-summed; TOTAL row moves when tabs are added       |
| Published RFCs             | 5     | Stable primitives, plus RFC 10017 for WG completeness. |
| Active IETF Drafts         | 465   | **★ Where the action is.** WG + individual drafts.     |
| Mission-Bound (Pre-pub)    | 46    | McGuinness GitHub-only family. Venue split, not topic. |
| OpenID Foundation          | 11    | Final + draft OIDF specs.                              |
| Other Standards & Govt     | 7     | Kantara, W3C, NIST, EU AI Act, NSA MCP CSI.            |
| Academic Papers            | 12    | arXiv + IEEE.                                          |
| Industry & Implementations | 149   | Vendor blogs, reference impls, full Control Plane blog.|

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
  - **15 live individual I-Ds** on Datatracker (13 Active + 2 Expired; a 16th,
    `client-instance-assertion`, is Replaced). Verified by author-prefix
    enumeration 29 Sep 2026 — **the previously-recorded "18" was wrong.** They are:
    actor-profile, actor-proofs, actor-receipts, ai-agent-instance,
    client-attesters (new 28 Sep 2026), client-instance-id (re-slug of
    client-instance-assertion, 28 Sep 2026), domain-authorized-issuer,
    id-assertion-framework, id-continuation-assertion, insufficient-claims,
    mission, resource-token-resp (expired), rfc9728bis (expired),
    token-exchange-cnf, token-xchg-target-svc-disco.
  - `draft-mcguinness-oauth-actor-profile` — the Actor Profile itself, the anchor
    draft cited throughout this file. **Corrected 4 Sep 2026:** the 26 Aug sweep
    recorded this as "the most consequential single omission" its cross-check
    found, but it had been tracked all along under a URL pointing at the -00 HTML
    rendering (`.../doc/html/draft-mcguinness-oauth-actor-profile-00`), which the
    slug diff never matched. The 26 Aug addition created a **silent duplicate**;
    the two rows were merged 4 Sep 2026 onto the canonical Datatracker URL.
  - **The 47-draft Mission-Bound Authorization family** at
    `github.com/mcguinness/mission-bound-authorization` (34 on 26 Aug 2026,
    46 on 4 Sep, 47 on 29 Sep — **growth has slowed sharply**, +1 in
    twenty-five days against +12 in the preceding nine) — 46 are GitHub-only
    (marked "IETF (Pre-publication — GitHub)" in standards-org) and **now live
    in their own `Mission-Bound (Pre-pub)` tab** (split out 26 Aug 2026); only
    `draft-mcguinness-oauth-mission` is also on Datatracker, and that one
    deliberately stays in the Active IETF Drafts tab. The repo ships a
    machine-readable `family-manifest.json` — **use it as the source of truth**
    for this family rather than re-deriving structure. **Its schema changed
    between 26 Aug and 4 Sep 2026:** the per-draft fields are now `role`
    (core / adapter-binding / companion / guide), `spec_maturity` and
    `maintenance`, replacing the old `maturity` and `adoption_rung`; the top
    level also gained `verbs`, `maintenance_classes` and `reference_stacks`.
    Groups are now **ten**, with `core` gone: architecture, approval-time,
    lifecycle, runtime-enforcement, bindings-substrate, agent-runtime,
    sub-agents, cross-domain-projection, proof-portability, security-model.
    The manifest also carries a `known_non_family_refs` note warning that
    `oauth-id-continuation-assertion` is adjacent, not family — do not add a
    phantom manifest entry for it. **Re-checked 29 Sep 2026: schema unchanged
    since 4 Sep, no renames, one addition** (`mission-control-plane`, lifecycle /
    companion, and the first family member marked `lab-best-effort` — the
    weakest maintenance class in the manifest's vocabulary).
  - **1 OIDF profile** in OpenID Foundation tab: AuthZEN Access Request &
    Approval Profile (ARAP) — adopted as WG draft May 2026, Draft 1 published
    3 Jun 2026
  - **79 blog entries** at `notes.karlmcguinness.com` ("Control Plane"), all now
    in the Industry & Implementations tab — verified 26 Aug 2026 as complete
    coverage of the live site, with no dead links. Major arcs: Agent Control Points
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
  infix at -09; now at **-11, 29 Sep 2026**) is the principled OUTLIER —
  zero OAuth dependencies; argues PoP-by-default, resource-signed challenges,
  and AS-to-AS federation are architectural changes, not extensions. Flag
  any new draft that echoes those design choices.
  - **The OUTLIER is now a six-document family (29 Sep 2026).** Hardt filed
    `aauth-r3` (rich resource requests — vocabulary-based authorization, RAR's
    problem solved without RAR), `aauth-budgets` (a spending ceiling as a token
    claim, "structurally parallel to scope") and `aauth-events` all on
    28 Sep 2026, joining the already-tracked `aauth-bootstrap` and
    `aauth-headers`. **Update the OUTLIER tag's meaning, not the tag:** AAuth
    still depends on nothing, but it now has both an inbound composer
    (McGuinness's `mission-aauth` binding, noted 4 Sep 2026) and its own
    extension ecosystem. "Depends on nothing" no longer implies "nothing
    depends on it".

- **Larry Lewis**. `agent-trust-protocol/atp-core` (Industry tab, row 5).
  Acronym near-collision with `draft-sharif-attp` — different designs:
  discrete L0–L4 trust levels there, continuous 0.0–1.0 trust scoring here.

- **Heather Flanagan** (Spherical Cow Consulting; added 26 Aug 2026). Not a spec
  author here — an unusually well-connected industry observer, tracked as a
  bellwether. **36 of her 159 archive posts** are in the corpus; the rest is
  deliberately out of scope (standards process, geopolitics, wallets, conference
  craft). Threads worth watching: the four-part 2026 **discovery** series, which
  weighs DNS vs well-known URIs vs registries vs catalogs — the same design space
  DAWN, the `mcp://` URI drafts and the Zhao A2A DNS-SD/WebFinger pair each pick a
  corner of; a **non-human-identity arc running back to Apr 2024**, well before the
  agent draft wave; and "Authorization – the Next Big Thing" (Jun 2023), the oldest
  entry in the corpus from any blog source. She was already an indirect input once:
  commit `6cf83f7` added 89 lines of sources she pointed to, but none of her own
  writing until now.

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

- **Sharif**. A primary body of work as of 26 Aug 2026 — **14 drafts**, all
  tracked. `sharif-agent-trust-enforcement` (-00, 27 Aug 2026) was added on
  4 Sep 2026, the first addition made under the take-in-full rule for this
  author, and it was found by **author-prefix enumeration, not keyword search**.
  Note the acronym near-collision between `sharif-attp` (discrete L0–L4 trust
  levels) and Lewis's `atp-core` (continuous 0.0–1.0 scoring); the new
  enforcement draft continues the L0–L4 design into a Kubernetes admission path.
  Re-verified complete 29 Sep 2026 — still 14, no gaps.

- **Schrock** (person 163567, EMILIA Protocol, Inc.). Take-in-full.
  **Correction made 29 Sep 2026:** the 26 Aug sweep recorded
  `ferro-schrock-memory-projection-record` as a name-substring false positive —
  "a different author" — and dropped it alongside the genuine `enghardt` case.
  Datatracker's author records show Schrock as co-author, so it is family and
  was missing for two sweeps. It is now tracked. **Lesson: settle an
  is-this-the-same-author question from the `documentauthor` endpoint's person
  id, never from the slug.** The other five `schrock` absences are all Replaced
  drafts whose successors are tracked — re-verified 29 Sep 2026.

- **Tom Sato** (person 162704, MyAuberge K.K.). Take-in-full, tracked as the
  `sato-soos-*` family. **He now also files under a bare `sato-` prefix** —
  `sato-agent-accountability-refarch` (-01, 21 Sep 2026) was invisible to
  author-prefix enumeration on `sato-soos` and was found only by checking
  author person ids. **Enumerate on the surname, not the family prefix.**

- **Watts** (person 165940, Independent Researcher). **Not yet take-in-full —
  a candidate for next sweep.** Went from one tracked draft
  (`watts-ai-identity-conformance`, added 4 Sep 2026) to four in three weeks:
  authority-transition receipts, evidence-boundary receipts and OAuth
  revocation closure were all added 29 Sep 2026. The subject is coherent —
  every one is about what evidence survives an authority state change — which
  is the test the rule actually applies. `watts-scientific-admissibility-evidence`
  was dropped as research provenance; if the next sweep finds the agent-facing
  subset still growing, promote the author.

- **Drake** (person 160218, 1id.com). **A new four-draft agent-identity family,
  taken together, added 29 Sep 2026** — problem statement, DNS/RDAP resolution,
  multi-stakeholder governance, and an EPP mapping, all filed 25 Sep 2026 around
  an Agent Identity Registry System (AIRS) and an `aid` URN. Notable for two
  reasons: it is the only work here that treats **physical robots** as the same
  identity problem as software agents, and it is the only one that specifies the
  *governance authority* rather than leaving the operator question open. Note
  the `aid` URN adds to the AID name tangle — see COLLISION.

## Sweep sources

The recurring places to check on every sweep. Each carries its own curation rule —
**take-in-full** sources are primary bodies of work; **filtered** sources are
tracked for the subset that touches delegated authorization.

| Source | Fetch | Rule |
| ------ | ----- | ---- |
| IETF Datatracker | tastypie API via `curl` (never WebFetch); `name__contains=<kw>` + `time__gte=` to discover, `name__in=` batches of ~25 to refresh | Filtered — see the curation bar below |
| Karl McGuinness — Control Plane (`notes.karlmcguinness.com`) | `/index.xml` RSS **union** hrefs scraped from `/mission-handbook/` and `/mission-handbook/read/` — the handbook chapters are not in the feed | **Take in full** |
| Mission-Bound family (`github.com/mcguinness/mission-bound-authorization`) | `family-manifest.json` at repo root is the source of truth | **Take in full** |
| **Heather Flanagan — standards-tracker** (`github.com/hlflanagan/standards-tracker`) | Daily CSV+MD at `reports/YYYY-MM-DD-ietf-identity-ai-watch.csv`, raw from `raw.githubusercontent.com`. CC0. Runs 14:00 UTC daily via GitHub Actions. | **Cross-check, do not ingest.** Use it to find what our own sweeps missed |
| **Heather Flanagan — Spherical Cow Consulting** (`sphericalcowconsulting.com`) | `/feed/` returns the **complete archive** in one request — 163 posts back to 2019, no pagination needed. (`/index.xml` 404s; it is WordPress, not Hugo.) Strip the trailing `The post … appeared first on Spherical Cow Consulting.` boilerplate from every `description`. | **Filtered** — 36 of 163 tracked as of 29 Sep 2026 |

**On the standards-tracker (added 26 Aug 2026).** Heather's bot watches recent
IETF I-Ds and W3C specs and classifies them for identity/authz/AI relevance. Her
CSV columns are `base_name, status, bucket, category, relevance_score,
group_name, title, abstract, datatracker_url, date_seen`. Buckets are
`read_now` / `adjacent_watchlist` / `monitor` / `ignored_after_review`;
categories include `agent_identity`, `authorization`, `core_identity`,
`trust_infrastructure`, `verifiable_claims`.

**Use it as a recall check on our own discovery, not as a source to ingest.**
Union the `base_name` column across all daily reports and diff against the
corpus. The first run of this (26 Aug 2026, 45 reports back to 8 Jul 2026,
1,617 distinct documents) found **249 `read_now` documents the corpus did not
have** — including drafts from author families this corpus claims to track *in
full*. See the coverage-gap entry in the watch list.

**⚠ Why our sweeps missed them — fix the method, not just the gap.** Corpus
discovery has been using `name__contains=<topic-keyword>` against Datatracker.
That only matches the *draft name*, so any draft whose slug omits the keyword is
invisible no matter how on-topic its abstract is — `draft-lundholm-kaif`,
`draft-sato-soos-kia` and `draft-hardt-httpbis-signature-key` were all missed
that way. Two rules follow:

1. **For any author or family taken in full, enumerate by author prefix**
   (`name__contains=schrock`, `name__contains=morrison`, …) and diff against the
   corpus. Never assume a family is complete because the last sweep added some
   of it.
2. **Topic-keyword name search is a supplement, not the primary discovery
   mechanism.** Heather's classifier reads titles and abstracts, which is
   strictly better recall; treat her report as the discovery baseline and our
   keyword sweep as the delta on top.

**⚠ Correction to rule 2, made 29 Sep 2026 — neither source is a superset.**
The 26 Aug framing said the standards-tracker has "strictly better recall" and
our keyword sweep is only "the delta on top". That is wrong in both directions,
and this sweep measured it. Of the 20 in-scope drafts the keyword sweep found
that the tracker's candidate buckets did not, **19 were absent from the tracker
entirely** — not classified and ignored, simply never seen. Two structural
reasons, both permanent:

- **The tracker only begins on 8 Jul 2026.** It watches *recent* I-Ds, so a
  draft filed earlier and never revised is invisible to it forever. Six drafts
  added this sweep were filed in **March 2026** and expired in September without
  ever appearing in a report: `gudlab-agentid-protocol`,
  `kiliram-agent-trust-auth-framework`, `liu-agent-operation-authorization`,
  `nandakumar-agent-sd-jwt`, `nemethi-aid-agent-identity-discovery`,
  `yakung-oauth-agent-attestation`.
- **Its classifier has its own recall gaps** on current drafts —
  `jacobs-web4-delegated-authority` was seen and bucketed `ignored_after_review`
  with score 0, despite being signed, bounded, revocable authority mandates for
  agents.

**So run all three and union them: author-prefix enumeration, the tracker, and
the keyword sweep.** Each catches what the others structurally cannot. And when
a draft matters, settle authorship from the `documentauthor` endpoint's person
id — the `sato-` / `sato-soos-` case this sweep found shows a take-in-full
author can change their own slug prefix and vanish from prefix enumeration.

**On Heather Flanagan specifically.** She is exceptionally well connected across
the identity industry and worth following as a bellwether, but most of her output
is deliberately broader than this corpus: standards process, governance,
geopolitics, wallets, conference craft, freelancing. Track the delegated-authz and
agent slice, not the whole blog — roughly a fifth to a quarter of posts qualify.
Her weekly Tuesday cadence means a sweep should expect ~4 new posts a month, of
which typically one is in scope. Note she was *already* an input to this corpus
once, indirectly: commit `6cf83f7` (15 Jul 2026, "Incorporated findings from
Heather Flanagan") added 89 lines of sources she had pointed to — but none of her
own writing was tracked until now.

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
  date. Do NOT rely on absolute row numbers — the tab is 465 rows and they
  shift with every sweep; locate clusters by draft-name search instead. The
  early McGuinness cluster still sits near `draft-mw-oauth-actor-chain`, which
  is kept adjacent because it directly responds to his Actor Profile. Each
  sweep appends labelled blocks at the end of the tab, so the tail is now in
  sweep order: the Aug 2026 Mission-Bound and general blocks, then 4 Sep, then
  the two 29 Sep blocks (take-in-full families + WG adoptions, then the general
  Datatracker sweep, alphabetical within the block). New drafts from a tracked
  author go with the relevant block, not next to their cluster.
- **Industry & Implementations:** 5 reference implementations lead (rows 1–5),
  then the McGuinness Mission-Bound blog series (rows 7–10, publication order:
  MVP first as the substrate post), then blogs and analyst articles.
- **Mission-Bound (Pre-pub):** the 46 GitHub-only family drafts, in the order
  the Aug 2026 sweep generated them from `family-manifest.json`, with later
  sweeps' additions appended. This tab is a
  **venue** split, not a topic one — the test for belonging here is "lives only
  in the author's repo", not "is about missions". If one of these gets filed on
  Datatracker, move that row to Active IETF Drafts and update its standards-org,
  the way `draft-mcguinness-oauth-mission` already sits there.
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
- **COLLISION** — name conflict with another draft. Two live tangles:
  - **"AIP" — now six.** singla, prakash, aip-agent-identity-protocol,
    `fane-opena2a-aip` (-02, 6 Aug 2026), and as of 29 Sep 2026 the
    Sogomonian pair `aiip-core` and `aiip-aiid` (AI Internet Protocol —
    one extra `i`, which will not save anyone reading quickly). Note
    `fane-opena2a-aap` also collides acronym-wise with the unrelated
    `draft-aap-oauth-profile` (Agent Authorization Profile).
  - **"AID" — now three, two of them by the same author.**
    `nemethi-dawn-aid` (Agent Identity and Discovery, the DAWN one),
    `nemethi-aid-agent-identity-discovery` (the *same author's* earlier
    DNS-first `_agent.<domain>` TXT-record protocol, filed 16 Mar 2026,
    added 29 Sep 2026), and `watts-ai-identity-conformance`'s unrelated
    "AID-1". Drake's AIRS `aid` URN (added 29 Sep 2026) is a fourth use of
    the letters, in a different namespace. **Always name the full slug.**
- **SUPERSEDED** — replaced by a re-slug. `sharif-payment-trust` (replaced by
  `sharif-attp`), plus the six pairs resolved 26 Aug 2026. **Two shapes, two
  treatments** — check which one you have before editing:
  - *Successor not yet tracked* → rename the row in place (title, URL, summary
    from the new abstract) and record the old slug in comments so searches for
    it still land. Applied to `rosenberg-aiproto-framework` →
    `rosenberg-agentproto-usecases` and `schrock-agent-action-manifest` →
    `schrock-action-evidence-boundary`.
  - *Successor already tracked* → the old row is a **duplicate**, not a rename.
    Delete it and put a `SUPERSEDES <old-slug>` note on the successor's row.
    Applied to `meunier-webbotauth-httpsig-directory`,
    `ni-batch-authorization-delegation`, `schrock-ep-action-evidence-graph`,
    and `somoza-atn-agent-trust-negotiation` — four rows that had been sitting
    in the corpus as silent duplicates of drafts already tracked under their
    post-rename slugs.
  - **Three more resolved 29 Sep 2026.** Renamed in place (successor not
    tracked): `fletcher-transaction-token-chaining-profile` →
    `fletcher-oauth-txn-token-chaining-profile` (the maintainer's own draft; the
    slug gained an `oauth-` infix and shortened `transaction` to `txn`, and the
    revision counter restarted at -00), and
    `mcguinness-oauth-client-instance-assertion` →
    `mcguinness-oauth-client-instance-id`. Deleted as a duplicate (successor
    already tracked): `meunier-webbotauth-httpsig-protocol`, now Replaced by
    `ietf-webbotauth-httpsig-protocol`.
  - **⚠ A `replaces` relation that does not exist yet is not a negative result.**
    On 4 Sep 2026 this file recorded that Datatracker held **no** `replaces`
    relation between the individual and WG Web Bot Auth drafts despite identical
    titles, and kept both rows on that basis. The relation exists now. **Re-test
    the relation on every sweep for any freshly-adopted WG draft** — the filing
    lags the adoption.

## Pending watch list

**McGuinness watch list — RESOLVED as of the 11 Aug 2026 sweep.** All five
previously-pending drafts are now filed and in the corpus (two under shorter
slugs than originally watched: `domain-authorized-issuer`, `id-assertion-framework`).
Two further drafts appeared and were added: `token-exchange-cnf` (-00, 19 Jul 2026)
and `id-continuation-assertion` (-00, 3 Aug 2026).

Still worth periodic checking: whether any of the 46 GitHub-only Mission-Bound
family drafts get filed on Datatracker. Only `draft-mcguinness-oauth-mission`
has been so far — re-verified 29 Sep 2026 against all 47 manifest slugs. Re-check
with the family-manifest slugs.

**Graph — REBUILT 29 Sep 2026.** Now 725 nodes / 952 edges, in sync with the
workbook. `build_graph.py` derives it; adding a source no longer requires
touching that file. Edge provenance: 116 curated (the original hand-written
analysis, preserved and unchanged), 598 `composes` from the Mission-Bound family
manifest, 238 auto-derived `references` from bibliography text. Curated substrate
holds at 30 nodes and id collisions at 0; the curated overlay now applies to 43
nodes (was 42 — see the node-fork note below). Rebuild verified idempotent.

Notes for future graph work:

- 30 nodes are **curated substrate** (`in_workbook: false`) — foundational RFCs
  like 7519/7521/7523/9068/9334 that the bibliography cites but doesn't track as
  its own sources. They are preserved across rebuilds because curated edges hang
  off them. Don't "clean them up".
- **Adding a workbook tab means editing `build_graph.py` in two places** —
  `TAB_DEFAULT_TYPE` (line ~161) and `SPEC_TABS` (line ~188). Miss the first and
  every row on the new tab is typed `ext-*` instead of its real type; miss the
  second and node ids stop being derived from draft/RFC names, which breaks the
  curated overlay's ability to match them. Both were needed for the
  `Mission-Bound (Pre-pub)` tab on 26 Aug 2026.
- `MISSION_FAMILY` in `build_graph.py` mirrors the upstream `family-manifest.json`
  (**re-synced 29 Sep 2026: 47 drafts**, taking `composes` edges 587 → 598; the
  4 Sep re-sync was 46 drafts and took them 373 → 587). Re-sync it every sweep —
  regenerating the whole dict from the manifest is safer than patching it.
  **The upstream schema
  changed:** `maturity` and `adoption_rung` were replaced by `role`,
  `spec_maturity` and `maintenance`. The tuple in `build_graph.py` keeps its
  4-slot shape, so `maturity` now carries `spec_maturity` and `adoption_rung`
  now carries `role`. The 33 pre-4-Sep workbook rows still narrate the old
  vocabulary; the 12 new ones use the new one. Don't "fix" the mismatch by
  rewriting history — it records when upstream changed.
- The HTML shell's filter pills, `TYPE_COLOR`/`CAT_COLOR`, and `nodeRadius` maps
  are hand-maintained. **If you add a new node type or category, add a matching
  filter pill** — `applyFilters()` hides any node whose type has no checked pill,
  so a missing pill silently makes nodes invisible. (No change needed 29 Sep
  2026: the 86 additions produced no new type or category.)
- **The retitle-forks-a-node footgun fired again on 29 Sep 2026, exactly as
  predicted, and the substrate count is what caught it.** Renaming the
  `client-instance-assertion` row to `client-instance-id` left the old id alive
  as an orphaned curated substrate node — the same document twice — and the only
  visible symptom was substrate moving 30 → 31. The fix is the documented one:
  **before rebuilding**, retarget the stale node's curated edges onto the new id,
  port its curated `long_description` across (set `origin: "curated"` on the
  survivor, or the analysis is lost on the next rebuild), drop any self-loop the
  merge creates, and delete the stale node from the JSON. Note the two *other*
  renames in the same sweep caused no fork, because no curated edges hung off
  them — so a clean substrate count does not mean no rows were retitled.
  **Always diff node / edge / substrate counts against the previous build and
  explain any delta before committing.**

**Fixed 11 Aug 2026:** the two duplicate Industry rows from commit `612bb30`
(Defakto IETF 122, Rock Lambros RockCyber) were removed, keeping the richer
narration of each pair.

**29 Sep 2026 sweep — 609 → 695 sources (twenty-five-day window since 4 Sep):**

- **The largest single sweep so far (+86 net), and the first where the maturity
  events matter more than the count.** Two WG adoptions landed in the corpus's
  own subject: **`draft-ietf-oauth-deferred-token-response`** (-00, 16 Sep,
  `replaces draft-gerber-oauth-deferred-token-response`, which was already
  tracked) and **`draft-ietf-wimse-aims`** (-00, 15 Sep, `replaces
  draft-klrc-aiagent-auth`, also already tracked). Both individual drafts had
  been in the corpus for a full cycle before adoption, which is the first
  evidence that this bibliography's individual-draft tail is a leading
  indicator of WG work rather than just noise around it.
- **But still no Complex Delegation milestone.** `charter-ietf-oauth` is
  unchanged at rev 06 and the OAuth WG's three active milestones are still
  SD-JWT VC (**overdue since 31 Jul 2026**), OAuth 2.1 and Transaction Tokens
  (both 31 Dec 2026). The deferred-token-response adoption happened under the
  existing work program. **The standing watch item is unmoved:** a Complex
  Delegation milestone is still the signal to look for.
- **WIMSE is now the third chartered WG producing in-scope mechanisms**, with
  OAuth and Web Bot Auth. Note the downstream effect already visible:
  `gilda-wimse-agent-audit-record` profiles the seven minimum audit fields AIMS
  defines, twelve days after AIMS was adopted.
- **The OUTLIER doubled.** Hardt filed `aauth-r3`, `aauth-budgets` and
  `aauth-events` on 28 Sep 2026, taking AAuth from three documents to six, and
  revved the protocol to -11. See the Hardt entry above — the tag stays, its
  meaning narrows.
- **Take-in-full families were incomplete again, in two new ways.** Both were
  found by checking Datatracker's `documentauthor` person ids, not slugs:
  `ferro-schrock-memory-projection-record` was wrongly dismissed on 26 Aug as a
  different author (it is Schrock), and `sato-agent-accountability-refarch` is
  the `sato-soos` author filing under a shorter prefix. See the Schrock and Sato
  entries above.
- **The standards-tracker is not a discovery superset** — 19 of the 20 in-scope
  drafts our keyword sweep found were absent from it entirely, six of them filed
  in March 2026, before the tracker's 8 Jul 2026 start. This retires the 26 Aug
  claim that it has "strictly better recall". See the correction under Sweep
  sources; it changes the method, not just this sweep's numbers.
- **A new prolific-author tier, handled the same way as the `das-` case.**
  Take-in-full was **not** applied to any of them; drafts were picked on merit:
  `wang-` JEP family 4 of ~10 (the Delegation event verb, action mandates,
  receipts and the profile model; the cognition, evolution and time drafts
  dropped), `stone-` 6 of 14 (commerce, dispute resolution, escrow and the trust
  passport; the two SwarmScore reputation drafts and AIVS dropped), `cowles-`
  3 of 4 (AOCL, VOLT, WARD; the bare message envelope AEE dropped),
  `jovancevic-` 2 of 4. The `das-` family stays at 3 of ~40 — **and note it now
  files under non-`das-` slugs too** (`draft-agentic-ai-tool-execution-finality`
  is a DAS document), so prefix exclusion alone will not hold it out.
- **The discovery/registry corner is the most contested area in the corpus.**
  Five entrants arrived in one window — Drake's AIRS (DNS/RDAP + EPP + a
  governance authority), `sankarshan-agent-registry-protocol`,
  `tanase-ain-authoritative-resolution`, `vandemeent-ains-discovery` and two
  more DAWN framework drafts (`zhang-`, `yao-`) — joining `pioli-agent-discovery`
  and the `mcp://`/DAWN work. All four corners of Flanagan's 2026 discovery
  series (DNS, well-known URIs, registries, catalogs) now have multiple
  competing drafts.
- **The verifier side finally has a draft.** `jackson-wimse-evaluation` (-02,
  29 Sep) states what a verifier must do with a delegation chain, on the
  observation that two verifiers can check the same chain, both report success,
  and enforce different policy. Every chain draft the corpus tracks specifies
  the conveying side only. Read it against `asor-wimse-agent-delegation-chain`,
  `hamr-oauth-agent-delegation` and `mcguinness-oauth-mission-attenuation`.
- **The accountability axes keep multiplying.** Redress gained a mechanism
  (`pinto-cbap-1` binds contestation terms *before* execution) and dispute
  resolution arrived as a state machine (`stone-adrp`). New this sweep:
  **revocation closure** (`watts-oauth-agent-revocation-closure` — invalidating
  a credential does not close every path from revoked authority to effect) and
  **evidence adequacy** (`watts-agent-evidence-boundary`,
  `sergeev-claim-boundaries`, `wadkins-agentproto-action-determinability`).
  `sergeev-claim-boundaries` is the useful corrective: this corpus now holds
  more receipt formats than things they attest.
- **Budget arrived twice, independently** — `hardt-aauth-budgets` (28 Sep) and
  `effortel-pulse` (17 Sep). Spend ceilings are becoming a delegation
  constraint rather than an application concern.
- **Expiry churn continues, with a twist.** Six of the 86 additions were already
  expired when added, but unlike the 4 Sep pattern these were not
  filed-and-expired-fast — all six were filed in **March 2026** and expired in
  September, having sat untracked the whole time. Newly expired among
  previously-tracked drafts: `aip-agent-identity-protocol`,
  `serra-mcp-discovery-uri`. All tagged and kept per the standing rule.
- **Karl's blog: no new posts.** The RSS feed's newest item is still 10 Aug 2026
  and the handbook is unchanged; the corpus's 79 entries remain complete, and a
  **full link-liveness pass found all 79 live** (note: the site now 308-redirects
  every URL to a trailing slash — `urllib` does not follow 308, so use
  `curl -L` or the check reports every link dead).
- **Flanagan: four new posts, all out of scope.** Standards transparency
  (1 Sep), identity conferences (8 Sep), and a two-part verifier/credential
  acceptance arc (15 and 22 Sep). The last two are the closest call — they are
  about who accepts a credential and on what basis — but they sit in the
  wallets/VC slice her filter rule excludes, not delegated authority or agents.
  Worth noting she is running a *verifier-side* arc at the same moment the IETF
  tail produced its first verifier-side delegation draft; if she turns it toward
  agent authority, that is the post to track. Archive is now 163 posts, 36
  tracked.
- **Other watch items checked, all unmoved:** `identity-chaining` and
  `rfc7523bis` still in the RFC Editor queue with no RFC number;
  `rar-metadata-remediation` still -00; no Vauban supersession (no `replaces`
  relations, all six components still tracked); an audit of all tracked
  Datatracker drafts confirms **RFC 10017 is still the only one to have reached
  RFC status**.

**4 Sep 2026 sweep — 572 → 609 sources (nine-day window since 26 Aug):**

- **The Mission-Bound family grew 34 → 46 drafts upstream in nine days** (+12
  rows in the Mission-Bound tab, now 45). All 33 previously-tracked slugs are
  still in the manifest — clean growth, no upstream renames. The most
  structurally significant addition is **`draft-mcguinness-mission-gnap`**, an
  adapter-binding for GNAP: with the existing OAuth and AAuth bindings, the
  family now presents as a **substrate-neutral kernel with three bindings**
  rather than an OAuth extension. Note the AAuth binding means Karl's family now
  composes against Hardt's `aauth`, the draft this file tags as the OUTLIER with
  zero OAuth dependencies — the outlier has an inbound composer.
- **Still only `draft-mcguinness-oauth-mission` is filed on Datatracker**,
  re-verified against all 46 manifest slugs. The standing watch item is unmoved.
- **First WG-level Web Bot Auth document: `draft-ietf-webbotauth-httpsig-protocol`
  (-00, 1 Sep 2026).** Datatracker records **no `replaces` relation** to the
  individual `draft-meunier-webbotauth-httpsig-protocol` despite the identical
  title, so both are tracked. Web Bot Auth is now the second chartered WG (with
  OAuth) producing agent-identity mechanisms directly in scope here.
- **A duplicate-detection failure, mirror image of the 26 Aug one.** Merging the
  two `actor-profile` rows (see the McGuinness entry above) resolved the graph's
  one long-standing id collision. 26 Aug's lesson was "don't match topic keywords
  against draft *names*"; this one is **diff on normalised draft slugs, not on
  URLs** — a rev-suffixed or `/doc/html/` link hides a row that is already there.
- **A new prolific-author tier, and a deliberate decision not to take it in
  full.** Several authors are now filing at high volume: `das-` (23 drafts, 11 in
  this nine-day window), `reilly-` (29), `nandakumar-` (26), `stone-` (14),
  `dogru-` (5), `cowles-` (4), `jovancevic-` (4). The take-in-full rule was
  **not** applied to any of them. The clearest case is `das-`: a single
  "execution finality" argument replayed across ICS/OT actuation, LEO satellite
  RF, 6G handles, child-safety rendering and banking — volume, not a body of
  agent-authorization work. 3 of 23 are tracked (including
  `das-agentic-tool-binding`, which `hamr-oauth-agent-delegation` references
  normatively). **The take-in-full rule is for authors whose whole output is
  agent authority (McGuinness, Schrock, Morrison, Sharif), not for anyone with
  many drafts.** Revisit if an agent-facing subset develops independently.
- **Two competing attenuated-delegation chain profiles arrived in the same week**
  and are the sweep's most on-charter additions: `asor-wimse-agent-delegation-chain`
  (token profile — RAR in RFC 9068 JWTs, hop-linked, offline-verifiable) and
  `hamr-oauth-agent-delegation` (HTTP header field carrying the chain). Both make
  the same critique: RFC 8693's nested `act` claim is informational only and
  cannot enforce attenuation past depth two. Compare McGuinness's
  `oauth-mission-attenuation`, which solves the same AS-in-the-hot-path problem
  inside the Mission-Bound family. `hamr` **SUPERSEDES `hassan-oauth-agent-delegation`**
  (confirmed `replaces` relation; identical title and abstract, only `hamr` tracked).
- **A third accountability axis is appearing: redress.** The corpus already had
  evidence (what was authorized), receipts (that it was exercised) and outcome
  binding (what followed). `pinto-agent-authz-contestability` adds *where an
  affected party can contest it*, and `laxsharma-pact` adds liability and
  escrowed settlement, joining `singh-psi-agent`. Worth watching whether the
  Schrock evidence stack takes up the contestability binding.
- **A matched discovery/authorization pair:** `pioli-agent-discovery` (ARDP,
  registry corner) and `barney-caam`, which specifies the Post-Discovery
  Authorization Handshake explicitly composing with it. Discovery additions this
  sweep now cover three corners of the space Flanagan's 2026 series maps —
  DNS (`nemethi-dawn-aid`), registry (ARDP), and origin-as-authority
  (`zzn-dvs`). **New COLLISION:** "AID" is claimed both by `nemethi-dawn-aid`
  (Agent Identity and Discovery) and by `watts-ai-identity-conformance` ("AID-1"),
  added the same day for an unrelated conformance model.
- **Expiry churn is still fast.** Seven of the 26 new drafts were **already
  expired when added** — several with expiry dates equal to their publication
  date. All tagged and kept per the standing rule. Newly expired among tracked
  drafts: **`mcguinness-oauth-rfc9728bis`** (28 Aug — the first McGuinness draft
  to expire), `ni-a2a-ai-agent-security-requirements` and
  `ni-wimse-ai-agent-identity` (both 1 Sep).
- **Author-prefix enumeration confirmed the take-in-full families are complete**
  (mcguinness, sato-soos, morrison, ruvalcaba, kavian, hopley, vauban: zero gaps).
  Every apparent absence under `schrock`, `hardt` and `skyfire` was checked
  individually and is **deliberate**: `skyfire-kyapayprofile`,
  `schrock-ep-enforcement-point` and `schrock-authorization-evidence-challenge`
  are all marked Replaced by drafts already tracked. The 26 Aug claim that
  remaining absences were deliberate **holds**.
- **Watch items checked, all unmoved:** no Complex Delegation milestone (OAuth WG
  still has exactly three active milestones — SD-JWT VC, now **overdue** at
  31 Jul 2026, plus OAuth 2.1 and Transaction Tokens, both 31 Dec 2026);
  `identity-chaining` and `rfc7523bis` still in the RFC Editor queue with no RFC
  number; `rar-metadata-remediation` still -00. **No Vauban supersession** — no
  `replaces` relations exist, so all six components stay tracked, though
  `x402-consolidated` picked up the state "No Longer In Independent Submission
  Stream" on 3 Sep, which is worth watching.
- **Flanagan: one new post, ruled out of scope.** "Standards Transparency: Public
  Isn't the Same as Understandable" (1 Sep 2026) is a standards-process post,
  which her filter rule excludes. Karl's blog: **no new posts** — the RSS feed's
  newest item is still 10 Aug 2026, and the corpus's 79 entries remain complete.

**26 Aug 2026 sweep — findings that change the corpus's shape:**

- **`draft-ietf-oauth-browser-based-apps` became RFC 10017** (state flipped
  21 Aug 2026; `became_rfc` relation confirmed on Datatracker). **RESOLVED
  26 Aug 2026 — moved to the Published RFCs tab** (now 5) and annotated as
  peripheral to delegated authorization, tracked for OAuth WG completeness.
  A full audit of all 251 tracked Datatracker drafts confirmed it is the **only**
  one that has reached RFC status — no others were hiding.
  Graph note: the move changed the node id from `draft-ietf-oauth-browser-based-apps`
  to `rfc-10017`, which orphaned the old id as a curated substrate node and
  duplicated the document. Fixed by retargeting its one curated edge
  (`depends_on rfc-6749`) onto `rfc-10017` and deleting the stale node from the
  JSON before rebuilding. **Watch for this whenever a row's title changes shape:
  node ids are derived from titles, so a retitle silently forks the node.**
- **`draft-aap-oauth-profile` is now EXPIRED.** Kept, annotated. It is half of
  the AAP/AIP acronym tangle recorded under COLLISION.
- **`draft-ietf-oauth-transaction-tokens` advanced past WGLC** to
  "WG Consensus: Waiting for Write-Up" (21 Aug 2026). `identity-chaining` and
  `rfc7523bis` are both sitting in the RFC Editor queue; neither has an RFC
  number yet. `wimse-workload-identity-practices` reached IESG AD Evaluation.
- **Expired and replaced drafts — RESOLVED 26 Aug 2026.** All 17 expired drafts
  are **tagged in their comments and kept in the corpus** by maintainer decision:
  an expired draft is still evidence of what was proposed. Three of them expired
  during this very sweep — `berlinai-vera`, `chen-agent-decoupled-authorization-model`
  and `cui-dmsc-agent-cdi` were added and tagged expired on the same day, which is
  a useful signal about how fast this individual-draft tail turns over.
  The 6 replaced drafts were resolved two different ways (see SUPERSEDED above);
  **four of them turned out to be duplicates already in the corpus under their
  new slugs**, so the tab lost 4 rows. Re-run the expiry check on future sweeps —
  it is a cheap pass over the same Datatracker batch fetch.
- **The candidate decision/policy cluster is now seven drafts**, not six —
  `gazitt-oauth-authzen-claims` (a third Gazitt AuthZEN draft) and
  `li-oauth-policy-based-anonymous-tokens` joined; still no OAuth wiki cluster
  fits them. This strengthens the case for raising it upstream.
- **`draft-ietf-oauth-rar-metadata-remediation` is the first new WG-level draft
  in this space since the recharter.** RAR is the primitive the Mission-Bound
  family builds on, so this is the closest thing yet to Complex Delegation
  machinery arriving in chartered WG work. Watch it.

- **Author-family coverage gap — CLOSED 26 Aug 2026.** Cross-checking Heather
  Flanagan's standards-tracker exposed that families this corpus takes *in full*
  were substantially incomplete; **74 drafts were added** to close it. Final
  state, verified by author-prefix query (Datatracker / corpus):
  `schrock` 26/21, `sato-soos` 18/18, `morrison` 18/18, `ruvalcaba` 8/8,
  `kavian` 8/8, `hopley` 11/11, `sharif` 13/13, `hardt` 17/11, `ietf-wimse` 9/7,
  `skyfire` 7/6. **Every remaining absence is deliberate** — either the draft
  became an RFC, or Datatracker marks it Replaced and its successor is already
  tracked (all successors verified present), or the name-substring query caught a
  different author (`enghardt`, `ferro-schrock`).
  - The single most consequential omission was **`draft-mcguinness-oauth-actor-profile`**
    — the Actor Profile this file repeatedly names as the anchor draft, untracked
    while `actor-proofs` and `actor-receipts` were both in.
  - Corrections this forced: the "six-draft Morrison family" is **18**; NHE is a
    **six-draft family**, not the identity+authz pair recorded earlier the same day.
  - **New-author tier resolved 26 Aug 2026: 19 of 41 added.** The 22 dropped are
    "authorization" in a different sense or network management — RPKI/ASPA
    *route* authorization (`ietf-sidrops-aspa-profile`, `geng-sidrops-asra-profile`),
    ACE/OSCORE for constrained devices (4 drafts), EPP/RPP registry provisioning
    (`gould-regext-auth-token`, `wullink-rpp-oauth2-*`), plus MoQ, 6G, TLS service
    affinity and NMRG/OPSAWG network-management work. Kept the agent ones incl.
    `lundholm-kaif`, `burls-mtac`, `sabey-succession-receipts` (authority
    *succession*, a lifecycle stage nothing else here covers), `kondoju-evc`,
    `zagarella-autonomy-governor`, `pelov-bounded-agent-capabilities`,
    `bradleyb-audit-decision-records`, `singh-psi-agent` (names **liability** as a
    protocol concern), and the `ferro-*` ApertoID pair — DNS declaration plus HTTP
    signing, a competing design against WebBotAuth's HTTP Message Signatures.
    **Watch `lundholm-kaif`**: it is a full agent-identity *framework*, so it belongs
    in the AIP name-collision comparison rather than being read as a point mechanism.
  - **`draft-ietf-oauth-*` was deliberately excluded from this pass.** The prefix
    matches 52 drafts, but ~35 became RFCs years ago (`draft-ietf-oauth-v2` →
    RFC 6749, `dpop` → RFC 9449, `rar` → RFC 9396) and the corpus tracks the RFCs,
    not the drafts behind them. The OAuth WG is tracked *selectively*, unlike the
    author families — do not "complete" it. The live survivors worth a decision are
    `sd-jwt-vc`, `status-list` and `rfc8725bis`, all previously considered and left out.

**Other deferred items:**

- **Mission-Bound handbook chapters — RESOLVED 26 Aug 2026, all 29 added.**
  Industry went 84 → 113. The chapters each have their own `/notes/` URL but are
  **absent from the RSS feed**, which is why the 11 Aug sweep missed them.
  The initial framing — that they were a re-issued edition of material already
  tracked — **was wrong**, and the check that settled it is worth repeating on
  any similar call: a title diff found **zero** of the 24 matched an existing
  row, and fetching `/series/what-the-corporate-card-already-solved` showed
  **24 of its 30 member essays untracked while the series index itself was
  tracked.** The corpus held the table of contents without the chapters. Only
  the 3 chapters that were genuine re-slugs of pre-handbook posts were
  duplicates, and those were repointed rather than re-added.
  **General lesson: a tracked series index is not evidence its members are
  tracked.** Check members explicitly.

- **Vauban x402 — RESOLVED 26 Aug 2026, ruled IN.** Cryptographic proof systems
  are in scope when attached to agentic-payment receipts. **It was a seven-draft
  family, not the pair that was held**: `delegation-binding` was already tracked
  and six were added (`stark-receipts`, `pqc-receipts`, `vpsf-algebra`,
  `starknet-anchor`, `lifecycle-fsm`, `consolidated`).
  - `stark-receipts` is the family **hub** — four siblings reference it
    normatively, and `draft-dogru-cedulon` references it from the SCITT tail the
    corpus deliberately does not track, a rare inbound link from outside.
  - `x402-consolidated` (-00) folds format + PQC discipline + Starknet anchor into
    one document. Datatracker does **not** mark the components Replaced, so all six
    are tracked; **watch for supersession**, which would make the consolidated draft
    the survivor and the other three SUPERSEDED.
  - `starknet-anchor` is the most blockchain-specific document in the corpus and is
    the point where this cluster leaves protocol territory — kept for family
    completeness, flagged rather than pretended otherwise.
  - `lifecycle-fsm` is the most reusable of the six: an explicit payment-lifecycle
    FSM, the same shape of artifact as the seven-state Mission lifecycle.
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
Hopley x402 clusters were reinstated). **AIPREF is in scope as of 26 Aug 2026** —
the corpus already tracked the AIPREF WG charter, so dropping the WG's output was
inconsistent; `wallace-aipref-grant-binding` is the reason it matters, since a
party-scoped revocable grant that lifts a reservation is a delegation primitive.
**SCITT remains out of scope** unless a draft is about agent authority rather than
supply-chain transparency (`hawkins-scitt-attested-agent-payment` is the kind that
gets in). Primary/authored bodies of work — a single
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
